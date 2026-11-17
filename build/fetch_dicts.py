# -*- coding: utf-8 -*-
"""下载词书数据（kajweb/dict 的 zip），解压到 build/.cache/books/。

用法：
    python build/fetch_dicts.py

说明：
- 只依赖标准库（urllib），无需 pip install。
- 已存在的 json 会跳过；删除 build/.cache 可强制重新下载。
- 若 jsdelivr 某个镜像不通，脚本会自动切换镜像重试。
"""
import os
import sys
import urllib.request
import zipfile

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
CACHE = os.path.join(BASE_DIR, ".cache")
ZIP_DIR = os.path.join(CACHE, "zip")
BOOK_DIR = os.path.join(CACHE, "books")

# 词书 zip 文件名，json 名称即去掉前缀与扩展名后的部分
BOOKS = [
    "1521164649209_CET4_1.zip",
    "1521164635506_CET4_2.zip",
    "1521164643060_CET4_3.zip",
    "1521164668667_CET6_1.zip",
    "1524052554766_CET6_2.zip",
    "1521164633851_CET6_3.zip",
    "1521164675301_GaoZhong_2.zip",
    "1521164679263_GaoZhong_3.zip",
    "1521164647926_ChuZhong_2.zip",
    "1521164652700_ChuZhong_3.zip",
]

MIRRORS = ["cdn.jsdelivr.net", "gcore.jsdelivr.net", "fastly.jsdelivr.net"]
PATH_TPL = "https://{host}/gh/kajweb/dict@master/book/{name}"


def download(name):
    """下载单个 zip，成功返回本地路径，失败返回 None。"""
    dest = os.path.join(ZIP_DIR, name)
    if os.path.exists(dest) and os.path.getsize(dest) > 10000:
        return dest
    for host in MIRRORS:
        url = PATH_TPL.format(host=host, name=name)
        try:
            req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0"})
            with urllib.request.urlopen(req, timeout=90) as resp, open(dest, "wb") as f:
                f.write(resp.read())
            if os.path.getsize(dest) > 10000:
                print("  download ok:", host, name)
                return dest
        except Exception as exc:                      # 换镜像继续
            print("  mirror failed:", host, name, type(exc).__name__)
    return None


def main():
    os.makedirs(ZIP_DIR, exist_ok=True)
    os.makedirs(BOOK_DIR, exist_ok=True)
    missing = []
    for name in BOOKS:
        json_name = name.split("_", 1)[1].replace(".zip", ".json")
        target = os.path.join(BOOK_DIR, json_name)
        if os.path.exists(target):
            print("skip existing:", json_name)
            continue
        print("fetch:", name)
        zip_path = download(name)
        if not zip_path:
            missing.append(name)
            continue
        with zipfile.ZipFile(zip_path) as zf:
            members = [m for m in zf.namelist() if m.lower().endswith(".json")]
            if not members:
                missing.append(name)
                continue
            with zf.open(members[0]) as src, open(target, "wb") as dst:
                dst.write(src.read())
        print("  extracted:", json_name)

    if missing:
        print("\n以下词书获取失败，请稍后重试或手动下载：")
        for m in missing:
            print("  -", PATH_TPL.format(host=MIRRORS[0], name=m))
        return 1
    print("\n全部词书就绪：", BOOK_DIR)
    return 0


if __name__ == "__main__":
    sys.exit(main())
