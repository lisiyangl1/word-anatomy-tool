# 单词解剖台 · Word Anatomy

> 一个单文件、纯前端的英文单词解析工具：把「音标 / 音节 / 词根词缀 / 释义例句 / 同义词」五层信息放进一屏，双击 HTML 就能用。

- 在线使用：<https://lisiyangl1.github.io/word-anatomy-tool/>（GitHub Pages 托管，无需下载）
- 交付文件：`word-anatomy.html`（约 2.3 MiB，词库已内嵌）
- 词库规模：**7536** 个词条，覆盖 CET-4 / CET-6 全部词汇
- 运行方式：无后端、无构建、无数据库，浏览器直接打开

---

## 1. 项目背景与解决的问题

背单词时最常见的问题不是「查不到」，而是「查到了也记不住」：只知道中文意思，不知道这个词为什么这么拼、怎么读、哪一部分承载核心语义，下次遇到同根词仍然认不出。

常见查词工具给出的是一份**结果**，本工具想给出的是一份**结构**：

| 痛点 | 本项目的做法 |
| --- | --- |
| 查词要联网、要账号、有广告 | 词库内嵌进 HTML，查询过程零网络请求（唯一外链是 Tailwind CDN 样式） |
| 只看到中文释义，记不住拼写 | 音节拆分（`in·for·ma·tion`）+ 音标，先会读再记形 |
| 不知道生词和已学词的关系 | 词根词缀拆解，同一词根下的词可以互相联想 |
| 想找近义词要再查一次 | 同义词是一排标签，点一下直接查那个词 |
| 四六级词表查不全，连 `run` / `think` 都查不到 | 四六级词书全量合并，另补高中/初中基础词兜底 |
| 有些词根本拆不开，工具却硬拆 | 拆不开就明确说「原生词、建议整体记忆」，其余模块照常展示 |

**明确不做的事**（避免误解）：

- 不是背单词 App：没有记忆曲线、生词本、打卡、账号体系。
- 不支持词组（`give up`、`look forward to` 这类不会解析）。
- 不是在线的剑桥/牛津词典：音标与例句来自公开词书数据，发音走浏览器系统 TTS 而非音频文件。

---

## 2. 主要功能与适用场景

### 2.1 功能清单

| 模块 | 实际实现 |
| --- | --- |
| 查词 | 输入英文单词，点「解析」或按 `Enter`；也支持 `?w=word` 直达、示例词、随机抽词 |
| 音标 | 英音 UK / 美音 US 分卡展示；点卡片调 `speechSynthesis` 朗读（无语音包则静默失败） |
| 音节 | 规则算法拆分，用间隔点展示，如 `un·be·liev·a·ble` |
| 词根词缀 | 前缀（蓝）/ 词根（红）/ 后缀（绿）/ 词干（灰）色块，每块下方给中文释义，底部附词源小注 |
| 释义例句 | 多条中文释义（带词性），每条配英文原句 + 中文译文，目标词自动高亮；同一例句被多条释义复用时标注「共用例句」 |
| 同义词 | 独立板块，标签可点击 → 自动填入输入框并触发查询 |
| 折叠 | 音标 / 音节 / 词根词缀 / 释义例句 / 同义词 五个模块均可折叠，`max-height` 平滑过渡 + 箭头旋转 |
| 一键复制 | 词头右上角「复制」，导出纯文本（音标/音节/词根词缀/释义例句/同义词），带 Toast 提示，剪贴板不可用时降级 `execCommand` |
| 查无此词 | 友好提示 + 基于编辑距离的 6 个候选词，点击即查 |
| 词形还原 | `studied → study`、`running → run`、`happier → happy`，命中后提示原形 |
| 交互反馈 | 输入框聚焦边框平滑变色、按钮波纹、加载骨架屏（最短 320 ms）、结果淡入上滑错开入场、释义卡 hover 上浮 |
| 快捷键 | `/` 聚焦输入框，`Esc` 清空输入 |
| 移动端 | ≤640px 单列布局，音标卡上下堆叠，标签自动换行 |

### 2.2 词库数据（构建产物实测）

| 指标 | 数量 |
| --- | --- |
| 词条总数 | 7536 |
| 带英式音标 | 7488 |
| 带例句（含译文） | 7399 |
| 带同义词 | 6696 |
| 人工精讲词条（`CURATED`） | 56 |

### 2.3 适用场景

- **四六级备考**：覆盖 CET-4 / CET-6 全部词，可当离线查词器用。
- **精读拆长难词**：`extraordinary`、`biotechnology`、`unfortunately` 这类词直接看到构词逻辑。
- **教学备课**：讲构词法时投屏演示，色块区分前后缀比板书直观。
- **前端样例**：单文件、零依赖（除样式 CDN）、无构建，适合当「工具型网页」的参考实现。

---

## 3. 安装方法与环境依赖

### 3.1 只是使用（推荐，零安装）

1. 拿到 `word-anatomy.html`。
2. 双击，或用浏览器打开（Chrome / Edge / Firefox / Safari 均可）。

运行时要求：

| 依赖 | 说明 | 是否必需 |
| --- | --- | --- |
| 现代浏览器 | 需要 CSS 变量、Flex/Grid、`URLSearchParams`、`navigator.clipboard`（不支持时自动降级） | 必需 |
| `https://cdn.tailwindcss.com/3.4.16` | Tailwind CSS v3 的 CDN 版，只负责布局与间距；配色/动效是页面内自定义 CSS | 联网更佳，离线时版式退化但功能正常 |
| 系统语音包 | 点击音标卡朗读用 `speechSynthesis` | 可选 |

> 完全离线也不想退化版式：把 CDN `<script>` 换成本地 `tailwindcss@3` 的浏览器构建文件即可。

### 3.2 想重建数据 / 改代码

| 依赖 | 版本要求 | 用途 | 是否必需 |
| --- | --- | --- | --- |
| Python | 3.8+，仅用标准库 | 抓词书、抽取词条、注入模板 | 重建数据必需 |
| Node.js | 14+（开发时使用 v22） | 跑算法自测与 DOM 测试 | 仅测试需要 |
| jsdom | ^31（仅 `domtest.js`） | 在 Node 里模拟浏览器跑页面 | 仅 DOM 测试需要 |

无需 `pip install`；`npm install` 只在跑 DOM 测试时用一次。

---

## 4. 使用方法和常用命令

### 4.1 直接使用

```text
1. 打开 word-anatomy.html
2. 输入单词（如 unbelievable），回车或点「解析」
3. 点标题行可折叠/展开任意模块
4. 点同义词标签 → 自动查该词
5. 点词头右上「复制」→ 导出完整文本解析
```

小技巧：

- 地址栏加 `?w=computer` 可直达结果页，适合做收藏或分享链接。
- `/` 聚焦输入框，`Esc` 清空；输入框右侧 `×` 也可清空。
- 「随机」按钮从 7536 个词里抽一个，适合随手翻。

### 4.2 重建词库与页面

```bash
# 1) 下载词书（10 个 zip，解压到 build/.cache/books/，存在则跳过）
python build/fetch_dicts.py          # macOS/Linux 若命令不同用 python3

# 2) 抽取精简词条 → build/.cache/words.json
python build/build_dict.py

# 3) 注入模板 → 仓库根目录 word-anatomy.html
python build/build_html.py
```

实测输出：

```text
$ python build/build_dict.py
unique: 7533
size KB: 2327.9 gzip KB: 942.8

$ python build/build_html.py
words: 7536
html KB: 2394.8
out: .../word-anatomy.html
```

说明：

- `build_dict.py` 输出 7533 条；`build_html.py` 再用 `SUPPLEMENT` 补 3 条词书里没有的精讲词，最终 **7536** 条。
- 中间数据落在 `build/.cache/`（约 50 MB），已写入 `.gitignore`，不入库；删掉即可重新下载。
- 词书来自 `kajweb/dict` 仓库，脚本按 `cdn.jsdelivr.net → gcore → fastly` 顺序切换镜像并重试；全部失败时会打印可直接手动下载的 URL。
- 想完全离线重建：把 zip 放到 `build/.cache/zip/<原名>.zip`，再跑第 2、3 步。

### 4.3 测试

```bash
# 算法自测：音节拆分 / 词根词缀 / 词形还原 / 纠错（无需装依赖）
node build/test.js

# DOM 冒烟测试：渲染、折叠、同义词跳转、复制、查无此词（需 jsdom）
cd build && npm install && node domtest.js
```

`domtest.js` 覆盖 20 项断言，全部输出 `PASS`、`--- 运行期错误 ---` 下为空即通过。

### 4.4 定制与扩展（都是改 `word-anatomy.html` 里的常量）

| 想做的事 | 改哪里 | 格式 |
| --- | --- | --- |
| 新增普通词条 | `const WORDS` | `{"w":"单词","lv":["CET4"],"uk":"音标","us":"音标","tr":[["词性","中文"]],"ex":[["English.","中文"]],"sy":["同义词"]}` |
| 给难词写人工拆解 | `const CURATED` | `word:{ syl:'音节', segs:[['un','pre','不'],['belie','root','相信']], note:'词源小注' }`，`segs` 拼接须等于原词 |
| 补同义词 | `const SYN_EXTRA` | `word:['a','b','c']`，词条自带同义词少于 3 个时并入 |
| 修正音节拆分 | `SYL_EXCEPTIONS` | `word:'sy·lla·ble'` |
| 调整前缀/后缀/词根表 | `PREFIXES` / `SUFFIXES` / `ROOTS` | `['前缀','释义']`；数组在建表后按长度降序排序，保证最长匹配 |

---

## 5. 输入与输出示例

### 5.1 正常查词：`unbelievable`

页面输出（对应五个折叠区）：

```text
unbelievable                         [基础词] [扩展词条]        [复制]

音标        英音 /ˌʌnbɪˈliːvəbl/      美音 /ˌʌnbɪˈliːvəbl/
音节拆分    un·be·liev·a·ble          （5 个音节）
词根词缀    un(前缀：不；非) + believ(词根：相信) + able(后缀：可…的)
            注：un- + believe + -able，字面「不可被相信的」，引申为「难以置信的」。
释义例句    1. [adj] 难以置信的；极好的
               例：The view from the top of the mountain was unbelievable.
               译：从山顶望去的景色令人难以置信。
同义词      incredible / astonishing / amazing / implausible（可点击）
```

### 5.2 拆不开的词：`abandon`

```text
词根词缀拆解（不可拆分）
  [无法拆分]  该词是原生词 / 单根词
  abandon 在词源上已不可再切分，不含常见前缀、词根或后缀，建议整体记忆。
  其余模块（音标、音节、释义、同义词）不受影响，正常查看即可。
```

此时音标 `/ə'bænd(ə)n/`、音节 `a·ban·don`、释义、例句、同义词照常显示。

### 5.3 词形变化：`studied`

```text
study                                   [词形还原]
按词形变化匹配到原形「study」
```

（原词头被替换为原形，上方补一行匹配说明；释义、例句、同义词均为 `study` 的内容。）

### 5.4 查无此词：`beleive`

```text
词库里暂时没有「beleive」
可能是拼写有误，或该词不在四六级词表内。换个拼写试试，或从下面挑一个：
[believe] [beehive] [deceive] [receive] [be] [beach]
提示：一次只查一个单词；动词、名词的变形会自动还原为原形。
```

### 5.5 「一键复制」导出的文本（真实输出）

```text
【computer】
等级：CET4 / 基础
英音：/kəm'pjuːtə/
美音：/kəm'pjutɚ/
音节：com·put·er

【词根词缀】
com（前缀：共同；加强） + put（词根：计算；思考） + er（后缀：人；物）
注：com-(共同/加强) + put(计算/思考) + -er(物)。

【释义与例句】
1. [n] 计算机，电脑
   例：a huge global computer network
   译：巨大的全球计算机网络

【同义词】PC、workstation、laptop、machine

— 由「单词解剖台」生成
```

### 5.6 词条数据结构（内嵌 JSON 的真实片段）

```json
{
  "w": "computer",
  "lv": ["CET4", "基础"],
  "uk": "kəm'pjuːtə",
  "us": "kəm'pjutɚ",
  "tr": [["n", "计算机，电脑"]],
  "ex": [["a huge global computer network", "巨大的全球计算机网络"],
         ["the latest computer software", "最新的计算机软件"]],
  "sy": ["PC", "workstation", "laptop", "machine"]
}
```

---

## 6. 项目结构

```text
.
├── index.html                 # Pages 入口页：秒跳转到 word-anatomy.html，保留 ?w= 参数
├── word-anatomy.html          # 交付主文件：词库内嵌，双击即用（约 2.3 MiB）
├── word-anatomy-说明.txt       # 面向使用者的中文说明（功能、扩展方式、限制）
├── README.md                  # 本文件：面向开发者/维护者
├── LICENSE                    # MIT 许可证（仅覆盖代码，词库数据除外）
└── build/
    ├── template.html          # 页面模板，内含占位符 __WORDS_JSON__
    ├── fetch_dicts.py         # 下载 10 本词书 → build/.cache/books/（仅标准库）
    ├── build_dict.py          # 词书 JSONL → 精简词条 build/.cache/words.json
    ├── build_html.py          # 模板 + 词条 → 根目录 word-anatomy.html
    ├── test.js                # 算法自测（Node，无依赖）
    ├── domtest.js             # DOM 冒烟测试（Node + jsdom，20 项断言）
    ├── package.json           # 仅声明 jsdom devDependency
    └── .cache/                # 下载与中间产物（约 50 MB，已忽略，可删）
```

页面内部结构（`word-anatomy.html` 单文件）：

| 层 | 内容 |
| --- | --- |
| 数据层 | `WORDS`（7536 词条）、`CURATED`（56 条精讲）、`PREFIXES`(90) / `SUFFIXES`(89) / `ROOTS`(124)、`SYL_EXCEPTIONS`(24)、`SYN_EXTRA`(12) |
| 算法层 | `syllabify()` 音节、`decompose()` 词根词缀、`lemmaCandidates()` 词形还原、`suggest()` 编辑距离纠错 |
| 渲染层 | `renderWord()` / `section()` / `renderSegments()` / `renderMeanings()` / `renderSynonyms()` / `makeCollapsible()` |
| 交互层 | `query()`、波纹、Toast、复制、朗读、`?w=` 直达 |

---

## 7. 数据来源与合规

- 词条数据抽取自开源词书仓库 [`kajweb/dict`](https://github.com/kajweb/dict)，通过 jsDelivr 获取；只保留 `headWord / ukphone / usphone / trans / sentence / syno` 这几个字段并做精简。
- 词书原始内容版权归原出版方/整理者，本项目仅用于个人学习与技术演示；如需商用或再分发词库数据，请自行确认授权。
- **许可证范围**：本仓库代码以 MIT 发布（见 [LICENSE](LICENSE)）；内嵌的词库数据（释义、例句等）**不在** MIT 授权范围内，沿用上游词书的版权约定。
- 页面页脚与源码 `WORDS` 定义处均已标注该来源与版权归属，二次分发时请一并保留。
- 页面内除 Tailwind CDN 外不请求任何外部资源，不收集任何用户数据，不使用 cookie 或 localStorage。

---

## 8. 已知限制

1. **仅单词级**：输入含空格会被判定为查不到（提示一次查一个词）。
2. **拆解是规则算法**：前缀/后缀/词根表匹配 + 多重校验（长度、元音边界、剩余部分成词性），能挡住 `ab-andon`、`col-or` 这类误拆，但个别词的词源判断仍可能与词源学结论不同；页面会在自动拆解下方标注该提示。追求准确可写成 `CURATED` 精讲。
3. **音节拆分同样是规则**：元音核 + 合法音节首分配，个别词会切得生硬，可用 `SYL_EXCEPTIONS` 覆盖。
4. **同义词偶有语义偏移**：部分继承自词书原始数据（例如 `abandon` 带 `mania`），未做人工清洗。
5. **朗读依赖系统语音包**：无 `en-US`/`en-GB` 语音时不发声，也不报错。
6. **Tailwind 走 CDN**：无网络时版式退化（查询、折叠、复制等功能仍正常）。
7. **构建需要外部数据**：`build_dict.py` 不能脱离 `build/.cache/books/` 运行，需先执行 `fetch_dicts.py`；词书下载源为第三方 CDN，不可用时会打印手动下载地址。
8. **无 CI / 无版本标签**：测试靠本地 `node build/test.js`、`node build/domtest.js` 手动执行；仓库当前不是 git 仓库。

---

## 9. 可复现性记录

本次交付前做过的校验（可与上面的命令逐条对照复现）：

- 用改造后的脚本链 `fetch_dicts.py → build_dict.py → build_html.py` 重新构建，产物与既有 `word-anatomy.html` **逐字节一致**（`cmp` 无差异）。
- `node build/test.js`：音节/拆解/词形还原/纠错抽测正常（如 `unbelievable → un·be·liev·a·ble`、`abandon → 不可拆分`）。
- `node build/domtest.js`：20 项断言全部 `PASS`，无运行期错误（渲染、五个折叠模块、同义词跳转、复制、查无此词、随机、波纹）。

---

## 10. 许可证

本项目代码采用 [MIT License](LICENSE) 发布：

```text
MIT License
Copyright (c) 2026 lisiyangl1
```

意思是你可以自由使用、修改、分发、商用这份代码，只需保留版权声明与许可声明；软件按「原样」提供，不含担保。

需要注意两点：

1. **词库数据不在 MIT 范围内**。`word-anatomy.html` 内嵌的释义、例句、同义词来自上游词书（见第 7 节），其版权与使用限制由原出版方/整理者决定。
2. 若你二次分发，建议同时保留第 7 节的来源说明，方便他人追溯数据出处。

修改版权人：直接编辑 `LICENSE` 第一行 `Copyright (c) 2026 lisiyangl1` 即可。

