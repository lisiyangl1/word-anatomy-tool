# -*- coding: utf-8 -*-
"""从 kajweb/dict 词书抽取精简词条，输出 build/.cache/words.json。

用法：
    python build/fetch_dicts.py    # 先下载词书到 build/.cache/books/
    python build/build_dict.py     # 再抽取精简词条

主词库：CET4_1..3 + CET6_1..3（四六级全量）
补充：高中/初中词书，仅收录四六级之外的基础词（避免出现查不到 run/think 这类情况）
"""
import json, os, re, html, gzip

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
BOOK_DIR = os.path.join(BASE_DIR, ".cache", "books")
OUT_FILE = os.path.join(BASE_DIR, ".cache", "words.json")

SRC = [
    ("CET4_1.json", "CET4"),
    ("CET4_2.json", "CET4"),
    ("CET4_3.json", "CET4"),
    ("CET6_1.json", "CET6"),
    ("CET6_2.json", "CET6"),
    ("CET6_3.json", "CET6"),
    ("GaoZhong_2.json", "BASE"),
    ("GaoZhong_3.json", "BASE"),
    ("ChuZhong_2.json", "BASE"),
    ("ChuZhong_3.json", "BASE"),
]


def clean(s):
    if not s:
        return ""
    s = re.sub(r"<[^>]+>", "", s)
    return html.unescape(s).strip()


def parse(path):
    for line in open(path, encoding="utf-8"):
        line = line.strip()
        if not line:
            continue
        try:
            yield json.loads(line)
        except Exception:
            continue


def extract(obj):
    w = clean(obj.get("headWord") or "")
    if not w or " " in w or not re.fullmatch(r"[A-Za-z][A-Za-z'\-]*", w):
        return None
    c = (obj.get("content") or {}).get("word", {}).get("content", {}) or {}
    trans = []
    for t in c.get("trans") or []:
        cn = clean(t.get("tranCn"))
        pos = (t.get("pos") or "").strip()
        if cn:
            trans.append([pos, cn])
    ex = []
    for s in ((c.get("sentence") or {}).get("sentences") or [])[:3]:
        en, cn = clean(s.get("sContent")), clean(s.get("sCn"))
        if en:
            ex.append([en, cn])
    syn = []
    for g in (c.get("syno") or {}).get("synos") or []:
        for h in g.get("hwds") or []:
            sw = clean(h.get("w"))
            if sw and " " not in sw and sw.lower() != w.lower() and sw.lower() not in [x.lower() for x in syn]:
                syn.append(sw)
    if not trans:
        return None
    return {"w": w, "uk": clean(c.get("ukphone")), "us": clean(c.get("usphone")),
            "tr": trans[:4], "ex": ex[:2], "sy": syn[:5]}


out, order = {}, []

for name, lv in SRC:
    path = os.path.join(BOOK_DIR, name)
    if not os.path.exists(path):
        raise SystemExit("缺少词书文件：%s\n请先运行 python build/fetch_dicts.py" % path)
    for obj in parse(path):
        r = extract(obj)
        if not r:
            continue
        k = r["w"].lower()
        if k in out:
            old = out[k]
            tag = "基础" if lv == "BASE" else lv
            if tag not in old["lv"]:
                old["lv"].append(tag)
            if len(r["tr"]) > len(old["tr"]):
                old["tr"] = r["tr"]
            old["uk"] = old["uk"] or r["uk"]
            old["us"] = old["us"] or r["us"]
            if len(r["ex"]) > len(old["ex"]):
                old["ex"] = r["ex"][:2]
            if len(r["sy"]) > len(old["sy"]):
                old["sy"] = r["sy"][:5]
        else:
            if lv == "BASE":
                # 基础词只补四六级没有的，且必须有例句或音标
                if not (r["ex"] or r["uk"]):
                    continue
                r["lv"] = ["基础"]
            else:
                r["lv"] = [lv]
            out[k] = r
            order.append(k)

compact = [{"w": out[k]["w"], "lv": out[k]["lv"], "uk": out[k]["uk"], "us": out[k]["us"],
            "tr": out[k]["tr"], "ex": out[k]["ex"], "sy": out[k]["sy"]} for k in order]
compact.sort(key=lambda x: x["w"].lower())

js = json.dumps(compact, ensure_ascii=False, separators=(",", ":"))
os.makedirs(os.path.dirname(OUT_FILE), exist_ok=True)
open(OUT_FILE, "w", encoding="utf-8").write(js)
print("unique:", len(compact))
print("size KB:", round(len(js.encode()) / 1024, 1), "gzip KB:", round(len(gzip.compress(js.encode())) / 1024, 1))
