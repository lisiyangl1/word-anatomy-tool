# -*- coding: utf-8 -*-
"""把词库 JSON 注入模板，产出单文件 HTML。

用法：
    python build/build_html.py

输入：build/template.html + build/.cache/words.json
输出：word-anatomy.html（仓库根目录）
"""
import json, io, os

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(BASE_DIR)
TMPL = os.path.join(BASE_DIR, "template.html")
DATA = os.path.join(BASE_DIR, ".cache", "words.json")
OUT = os.path.join(ROOT, "word-anatomy.html")

if not os.path.exists(DATA):
    raise SystemExit("缺少 %s\n请先运行 python build/fetch_dicts.py && python build/build_dict.py" % DATA)

words = json.load(open(DATA, encoding="utf-8"))

# 精讲词条中不在四六级词书里的词，补齐基础数据（音标 / 释义 / 例句 / 同义词）
SUPPLEMENT = [
    {"w":"unbelievable","lv":["扩展"],"uk":"ˌʌnbɪˈliːvəbl","us":"ˌʌnbɪˈliːvəbl",
     "tr":[["adj","难以置信的；极好的"]],
     "ex":[["The view from the top of the mountain was unbelievable.","从山顶望去的景色令人难以置信。"]],
     "sy":["incredible","astonishing","amazing","implausible"]},
    {"w":"television","lv":["扩展"],"uk":"ˈtelɪvɪʒn","us":"ˈteləvɪʒn",
     "tr":[["n","电视；电视机"]],
     "ex":[["She switched on the television to watch the evening news.","她打开电视看晚间新闻。"]],
     "sy":["TV","telly","broadcast"]},
    {"w":"telephone","lv":["扩展"],"uk":"ˈtelɪfəʊn","us":"ˈtelɪfoʊn",
     "tr":[["n","电话；电话机"],["v","打电话给…"]],
     "ex":[["He telephoned his mother every Sunday evening.","他每周日晚上都给母亲打电话。"]],
     "sy":["phone","call","ring"]},
    {"w":"telegraph","lv":["扩展"],"uk":"ˈtelɪɡrɑːf","us":"ˈtelɪɡræf",
     "tr":[["n","电报；电报机"],["v","电告；打电报"]],
     "ex":[["The news reached the village by telegraph.","消息通过电报传到村里。"]],
     "sy":["wire","telegraphy","cable"]},
    {"w":"autobiography","lv":["扩展"],"uk":"ˌɔːtəbaɪˈɒɡrəfi","us":"ˌɔːtəbaɪˈɑːɡrəfi",
     "tr":[["n","自传；自传体文学"]],
     "ex":[["Her autobiography became an instant bestseller.","她的自传一出版就成了畅销书。"]],
     "sy":["memoir","journal","diary"]},
    {"w":"antibiotic","lv":["扩展"],"uk":"ˌæntibaɪˈɒtɪk","us":"ˌæntibaɪˈɑːtɪk",
     "tr":[["n","抗生素；抗菌素"],["adj","抗生的；抗菌的"]],
     "ex":[["This antibiotic is effective against a wide range of bacteria.","这种抗生素对多种细菌有效。"]],
     "sy":["antibacterial","antimicrobial","penicillin"]},
    {"w":"unhappy","lv":["扩展"],"uk":"ʌnˈhæpi","us":"ʌnˈhæpi",
     "tr":[["adj","不快乐的；不满意的"]],
     "ex":[["She was deeply unhappy in her first job.","她的第一份工作让她很不快乐。"]],
     "sy":["sad","miserable","displeased","upset"]},
    {"w":"multinational","lv":["扩展"],"uk":"ˌmʌltiˈnæʃnəl","us":"ˌmʌltiˈnæʃnəl",
     "tr":[["adj","跨国的；多国的"],["n","跨国公司"]],
     "ex":[["He works for a multinational company based in Shanghai.","他在一家总部位于上海的跨国公司工作。"]],
     "sy":["transnational","global","international"]},
    {"w":"window","lv":["扩展"],"uk":"ˈwɪndəʊ","us":"ˈwɪndoʊ",
     "tr":[["n","窗；窗户"],["n","（计算机）窗口"]],
     "ex":[["She opened the window to let in some fresh air.","她打开窗户让新鲜空气进来。"]],
     "sy":["pane","opening","casement"]},
]

idx = {x["w"].lower(): x for x in words}
for sup in SUPPLEMENT:
    k = sup["w"].lower()
    if k in idx:
        # 已存在（基础词表）→ 用精讲的例句与同义词覆盖，等级标记保留
        old = idx[k]
        old["tr"] = sup["tr"] or old["tr"]
        old["ex"] = sup["ex"] or old["ex"]
        old["sy"] = sup["sy"] or old["sy"]
        old["uk"] = sup["uk"] or old["uk"]
        old["us"] = sup["us"] or old["us"]
        for lv in sup["lv"]:
            if lv not in old["lv"]:
                old["lv"].append(lv)
    else:
        words.append(sup)

words.sort(key=lambda x: x["w"].lower())

js = json.dumps(words, ensure_ascii=False, separators=(",", ":"))

tpl = io.open(TMPL, encoding="utf-8").read()
assert "__WORDS_JSON__" in tpl
html = tpl.replace("__WORDS_JSON__", js)

io.open(OUT, "w", encoding="utf-8", newline="\n").write(html)
print("words:", len(words))
print("html KB:", round(len(html.encode()) / 1024, 1))
print("out:", OUT)
