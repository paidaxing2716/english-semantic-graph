"""按词族重排待派池子，修掉三个路由缺陷。

问题（本脚本要解决的）：
1. root_backlog_from_67.txt 的 111 词不在任何池里，永远派不到，而它们是唯一带
   已核过词根名的词。
2. 同族词散落在 backlog / latin_remaining / germanic_remaining / rchunk41-46
   四处。派发规则是「凑不到 3 个成员的族不值得开根」，代理只看到残缺的族，会
   把该开根的词按 germanic 写掉，之后又得靠 migrate_germanic_to_root.py 回收
   （HANDOFF 三·1 的盲点，此处是排池方式主动制造的）。
3. 顺带：radius 这类拉丁词被错分进 germanic 池——归族后自然纠正。

族成员从 backlog 说明文字里的斜杠串抽取（「该族在词表内有 lease/release/relax
/relay/relish 五词」），不做拼写聚类——那个判不出词族，项目已栽过两次。

用法：python scripts/regroup_pools_by_family.py
"""
import json
import re
from pathlib import Path
from collections import defaultdict

ROOT = Path(__file__).resolve().parent.parent
D = ROOT / "drafts"
N_CHUNKS = 6  # 6 片并行 × 60 词是实测规模


def load_json(p):
    return json.loads((ROOT / p).read_text(encoding="utf-8"))


def pool(name):
    """始终从 .orig 基线读，脚本因此可重复跑。

    首次跑时把原文件复制成 .orig；之后每次都以 .orig 为输入重算，否则第二次跑
    会从已摘除的池子里找族成员，族会越跑越小。
    """
    f = D / name
    if not f.exists():
        return []
    base = f.with_suffix("") if f.suffix == ".txt" else f
    orig = D / f"{base.name}.orig.txt"
    if orig.exists():
        f = orig
    return [l.strip() for l in f.read_text(encoding="utf-8").splitlines() if l.strip()]


SEL_LOGIC = "se-（分开）+ legere（拾取）→ 从一堆里分开拾出"


def save_json(name, obj):
    (ROOT / "data" / name).write_text(
        json.dumps(obj, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def fix_select():
    """select 标着 root_pending（词根未建模），但 legere 根现在有了。

    四处都要同步：words / 根的 word_ids / 概念的 word_ids / relations 的边。
    只改 words.json 会被 validate 的 Q9 挡下（我第一版就漏了后三处）。写法照
    migrate_germanic_to_root.py。幂等：逐处判断，允许半完成态续上。
    """
    wf = load_json("data/words.json")
    rf = load_json("data/roots.json")
    cf = load_json("data/concepts.json")
    lf = load_json("data/relations.json")
    roots, concepts = rf["roots"], cf["concepts"]
    rels = lf["relations"]
    if not any(r["id"] == "legere" for r in roots):
        return "legere 根不存在，跳过 select"

    w = next((x for x in wf["words"] if x["id"] == "select"), None)
    if w is None:
        return "无 select 词条"
    done = []
    if w.get("decomposable") == "root_pending":
        w["decomposable"] = "root"
        w["root_ids"] = ["legere"]
        w["root_logic"] = SEL_LOGIC
        w.pop("decomposable_note", None)
        save_json("words.json", wf)
        done.append("words")
    if "legere" not in (w.get("root_ids") or []):
        return "select 已挂到别的根，不动"

    for r in roots:
        if r["id"] == "legere" and "select" not in (r.get("word_ids") or []):
            r.setdefault("word_ids", []).append("select")
            r["word_ids"].sort()
            save_json("roots.json", rf)
            done.append("roots")
    for c in concepts:
        if "legere" in (c.get("root_ids") or []) and "select" not in (c.get("word_ids") or []):
            c.setdefault("word_ids", []).append("select")
            c["word_ids"].sort()
            save_json("concepts.json", cf)
            done.append(f"concepts({c['id']})")
    if not any(x.get("from") == "legere" and x.get("to") == "select" for x in rels):
        rels.append({"from": "legere", "to": "select", "type": "root",
                     "note": SEL_LOGIC[:60]})
        save_json("relations.json", lf)
        done.append("relations")
    return ("select → legere，已补：" + "、".join(done)) if done else "select 已同步，无需改"


def main():
    words = load_json("data/words.json")["words"]
    roots = load_json("data/roots.json")["roots"]
    ids = {w["id"] for w in words}
    rids = {r["id"] for r in roots}
    origins = {r["id"]: r.get("origin", "") for r in roots}

    # ---- backlog：词 -> 已核过的词根名 + 原始说明 ----
    backlog, notes = {}, {}
    for line in (D / "root_backlog_from_67.txt").read_text(encoding="utf-8").splitlines():
        if "\t" not in line:
            continue
        word, rest = line.split("\t", 1)
        backlog[word.strip()] = rest.split("（")[0].strip()
        notes[word.strip()] = rest.strip()

    # ---- 其余池 ----
    src = {n: pool(f"{n}.txt") for n in ("germanic_remaining", "latin_remaining")}
    for i in range(41, 47):
        src[f"rchunk{i}"] = pool(f"rchunk{i}.txt")
    located = {w: n for n, ws in src.items() for w in ws}

    # ---- 归族：backlog 成员 + 说明里斜杠串提到的同族词 ----
    fam = defaultdict(set)

    def add(root, name):
        if name in located and name not in ids:
            fam[root].add(name)

    for word, root in backlog.items():
        fam[root].add(word)
        for run in re.findall(r"[a-z]{2,}(?:/[a-z]{2,})+", notes[word]):
            for m in run.split("/"):
                add(root, m)

    # 第二个来源：root_batch_notes.txt，格式 `根<TAB>成员/成员 —— 说明`。
    # 这些族是历史遗留的待接项（NEXT.md「顺带可做」列的就是它们），与 backlog
    # 同样散在各池里。不接进来的话 medius/esse/mirari/metiri 会一直散着。
    nf = D / "root_batch_notes.txt"
    if nf.exists():
        for line in nf.read_text(encoding="utf-8").splitlines():
            if "\t" not in line:
                continue
            root, rest = line.split("\t", 1)
            for m in re.findall(r"[a-z]{2,}", rest.split("——")[0]):
                add(root.strip(), m)

    # ---- 已建模的根 -> 补词而非新根（这类误报已发生六七次）----
    # 两种强度分开报：id 精确相同是确定的；origin 里提到词形只是候选，因为
    # origin 常写「与 X 不同根」这类排除关系（ligare 的 origin 就明写与 lex、
    # legere 不同根），子串命中的含义正好相反。带排除措辞的降级为「需核」。
    CONTRAST = ("不同根", "不同源", "不计入", "不合并", "非同", "不属", "而不")

    def existing(root):
        if root in rids:
            return ("exact", [root])
        hits = []
        for rid, o in origins.items():
            for m in re.finditer(r"(?<![a-zA-Z])" + re.escape(root) + r"(?![a-zA-Z])", o):
                w = o[max(0, m.start() - 40):m.end() + 40]
                hits.append((rid, any(c in w for c in CONTRAST)))
                break
        pos = sorted(r for r, c in hits if not c)
        neg = sorted(r for r, c in hits if c)
        if pos:
            return ("mention", pos)
        if neg:
            return ("excluded", neg)
        return ("new", [])

    # ---- 一词被两族同时收：只派一次，竞争方标在行内 ----
    # 这多半不是抽取错误，而是真的双属：universe ← unus + vertere；regime/
    # region/royalty 的 rex 又出自 regere（即 rect 根）；payment ← pacare ← pax。
    # 归属由代理按词源定夺，此处只保证不重复派发——同一个词被两个代理各写一份，
    # 合并时必冲突。规则：归成员更多的那族（上下文更全），另一族记进 rival。
    owner, rival = {}, defaultdict(list)
    for word in {w for ms in fam.values() for w in ms}:
        claims = sorted((r for r, ms in fam.items() if word in ms),
                        key=lambda r: (-len(fam[r]), r))
        owner[word] = claims[0]
        for r in claims[1:]:
            rival[word].append(r)
    for root in list(fam):
        fam[root] = {w for w in fam[root] if owner[w] == root}
        if not fam[root]:
            del fam[root]

    # ---- 打包成片：族整体不跨片，按词数均分到 N_CHUNKS 片 ----
    groups = sorted(fam.items(), key=lambda kv: (-len(kv[1]), kv[0]))
    status = {root: existing(root) for root, _ in groups}
    bins = [[] for _ in range(N_CHUNKS)]
    sizes = [0] * N_CHUNKS
    for root, members in groups:
        i = sizes.index(min(sizes))
        bins[i].append((root, sorted(members)))
        sizes[i] += len(members)

    TAG = {
        "exact": "补词——同名根已存在，按补词写，勿新建",
        "mention": "疑补词——已有根的 origin 提到该词形，先按规格查 origin 再定",
        "excluded": "新根，但注意已有根明写与之不同根（勿并入）",
        "new": "新根候选",
    }
    pulled = {w for _, ms in groups for w in ms}
    written = []
    for n, chunk in enumerate(bins, start=51):
        lines = []
        for root, members in sorted(chunk, key=lambda kv: (-len(kv[1]), kv[0])):
            kind, ex = status[root]
            tag = TAG[kind] + (f"（{'/'.join(ex)}）" if ex else "")
            lines.append(f"# {root}\t{len(members)} 词\t{tag}")
            for m in members:
                lines.append(f"{m}\t# 也可属 {'/'.join(rival[m])}，按词源定夺"
                             if rival[m] else m)
        f = D / f"rt_chunk{n}.txt"
        f.write_text("\n".join(lines) + "\n", encoding="utf-8")
        written.append((f.name, sum(len(m) for _, m in chunk), len(chunk)))

    # ---- 从各池摘掉已归族的词，原文件留 .orig 备份 ----
    stripped = {}
    for name, ws in src.items():
        keep = [w for w in ws if w not in pulled and w not in ids]
        if len(keep) != len(ws):
            f = D / f"{name}.txt"
            b = D / f"{name}.orig.txt"
            if not b.exists():
                b.write_text(f.read_text(encoding="utf-8"), encoding="utf-8")
            f.write_text("\n".join(keep) + "\n", encoding="utf-8")
        stripped[name] = (len(ws), len(keep))

    sel = fix_select()

    # ---- 报告 ----
    print(f"归族 {len(groups)} 族 / {len(pulled)} 词，切 {len(bins)} 片")
    for name, nw, nf in written:
        print(f"  {name}: {nw} 词 / {nf} 族")
    print("\n池子摘除后：")
    for name, (before, after) in stripped.items():
        if before != after:
            print(f"  {name}: {before} → {after}（-{before - after}）")
    by_kind = defaultdict(list)
    for root, (kind, ex) in status.items():
        by_kind[kind].append((root, ex))
    print(f"\n族按建模状态分（{len(groups)} 族）：")
    for kind in ("new", "exact", "mention", "excluded"):
        items = sorted(by_kind[kind])
        print(f"  {kind:9} {len(items):3} —— {TAG[kind]}")
        if kind in ("exact", "mention", "excluded"):
            for r, ex in items:
                print(f"      {r} → {'/'.join(ex)}")
    print(f"\n{sel}")


if __name__ == "__main__":
    main()
