# photo-album-skill

不让照片发霉。

很多照片不是没价值，只是太分散。它们躺在手机相册、聊天记录、硬盘文件夹里，时间久了就变成一堆没有上下文的文件。`photo-album-skill` 想做的事很简单：把这些散落的照片整理成一本有顺序、有呼吸、能反复翻看的画册。

它不是把照片塞进模板，也不是用漂亮话包装生活。它会反复问一个问题：

> 当时为什么按下快门？

答案可能很小：一个人回头的样子、一顿饭、一段路、一片云、一个普通下午忽然变得值得留下。整理照片不是收尾工作，它本身就是回忆的一部分。时不时翻出来看一下，照片就不会只躺在硬盘里慢慢发霉。

## 为什么做这个

因为大多数照片不是缺少滤镜，而是缺少整理。单张照片也许很好看，但散落太久，就会失去时间、地点和关系。画册的意义不是把生活修饰得更高级，而是把这些照片重新放回一个可以被翻阅的秩序里。

整理的过程会逼你重新看见很多东西：当时为什么停车、为什么回头、为什么拍下那顿饭、为什么那张有点糊的照片反而舍不得删。你不是在管理文件，而是在给记忆重新装订。

## 你会得到什么

- 一本单文件 HTML 画册：可离线打开、翻页、全屏、打印，不依赖外部资源。
- 一组社交图片：可导出小红书 3:4、朋友圈方图或竖图，按序号直接上传。
- 一份更小的离线相册：可压缩其他软件生成的超大 standalone HTML。
- 一套写作和选图规则：围绕真实细节和“为什么拍下”，避免模板化文案。

## 项目亮点

- **Agent 优先**：更适合交给 Codex、Claude Code、Trae 这类 Agent 操作，由它们读素材、选图、写文案、导出并检查页面。
- **叙事精排版**：不是把照片平均铺开，而是按时间线、人物关系、情绪转折和视觉节奏组织成一本能翻完的画册。
- **真实小细节优先**：保留手抖、路牌、背影、聊天截图、桌面、天气变化这些有记忆价值的细节，不只挑“最好看”的照片。
- **文案不模板化**：核心问题是“当时为什么按下快门？”，文案围绕真实原因写，能留白就不硬抒情。
- **单文件离线阅读**：HTML 内嵌图片和样式，适合保存、转发、归档，也可以继续导出 PDF。
- **社交发布友好**：支持逐页导出小红书、朋友圈图片组，文件名按顺序编号，方便直接上传。
- **能处理大文件相册**：已有 standalone HTML 太大时，可以压缩内嵌 base64 图片，生成适合离线阅读的小版。

## 适合谁用

- 旅行回来，照片很多，但不知道怎么整理成一条线。
- 想把家人、朋友、爱人、宠物或普通日常做成一本能回看的相册。
- 想发小红书、朋友圈、公众号，但不想一张张手动排版。
- 有很多散落照片，想让它们重新成为一个完整的故事。
- 想把已有的超大 HTML 相册压小一点，方便离线阅读和分享。

## 示例

这里放了一个真实示例：杉谷咖啡叙事画册。

- [HTML 画册](examples/shangu-cafe/杉谷咖啡-叙事画册.html)
- [PDF 画册](examples/shangu-cafe/杉谷咖啡-叙事画册.pdf)

如果 GitHub 不能直接预览 HTML，下载后本地打开即可。

## 使用方式

更推荐用 Agent 来操作，比如 Codex、Claude Code、Trae 这类能读文件、跑脚本、打开浏览器检查结果的工具。

### 推荐：用 Agent

先把仓库放到本地：

```powershell
git clone https://github.com/cescqh-cloud/photo-album-skill.git
```

如果你用 Codex，可以直接安装成 skill：

```powershell
git clone https://github.com/cescqh-cloud/photo-album-skill.git `
  "$env:USERPROFILE\.codex\skills\photo-album-skill"
```

然后把照片文件夹路径发给 Agent，说清楚你想要什么：

```text
使用 photo-album-skill，把 D:\Photos\周末散步 做成一本日常画册。
```

想认真整理，就这样说：

```text
做成叙事精排版，保留真实的小细节，不要写模板化文案。
重点帮我想清楚：这些照片当时为什么会被拍下来。
```

想要发布版本：

```text
做成画册，同时导出小红书图片组。
```

Agent 更适合做这些事：帮你选图、读同目录的 txt/md、整理时间线、写克制的文案、导出 HTML/PDF/社交图片，并检查页面有没有溢出或裁切。

### 不用 Agent：命令行

只想自己跑工具，也可以直接命令行生成：

```powershell
git clone https://github.com/cescqh-cloud/photo-album-skill.git
cd photo-album-skill
python scripts/build_album.py "D:\Photos\周末散步"
```

默认输出当前目录下的 `album.html`。

需要更认真一点的图文排版：

```powershell
python scripts/build_album.py "D:\Photos\周末散步" --composition editorial
```

想扫描子目录并限制照片数量：

```powershell
python scripts/build_album.py "D:\Photos\2026" --recursive --max-photos 60
```

可选安装 Pillow，用来修正 EXIF 方向并压缩大图：

```powershell
python -m pip install Pillow
```

生成器会自动：

- 扫描 JPG、JPEG、PNG、WEBP、GIF。
- 优先按 EXIF 拍摄时间排序，读不到时按文件名自然排序。
- 根据横竖比例、文字长度和前后照片自动组合页面。
- 将图片内嵌为 data URI，输出单个离线 HTML。
- 加入翻页按钮、键盘导航、进度、主题切换、图片放大和打印样式。

HEIC / HEIF 需先转换为浏览器支持的 JPG、PNG 或 WEBP。

## 用 album.json 指定细节

在照片目录放一个 `album.json`，可以指定标题、封面、说明和顺序：

```json
{
  "title": "平常的一天",
  "subtitle": "2026 · 初夏",
  "theme": "warm",
  "composition": "editorial",
  "cover": "IMG_1024.jpg",
  "captions": {
    "IMG_1027.jpg": "下午走到窗边，光刚好落在桌面上。",
    "小狗/IMG_1031.jpg": "它每次听见钥匙声，都会先跑到门口。"
  },
  "order": [
    "IMG_1024.jpg",
    "IMG_1027.jpg",
    "小狗/IMG_1031.jpg"
  ]
}
```

- `title`、`subtitle`、`theme`、`cover` 都可省略。
- `composition` 可用 `auto`、`editorial` 或 `gallery`。
- `captions` 的键可用文件名或相对路径。
- `order` 中未列出的照片会按自然文件名顺序接在后面。
- JSON 可使用 UTF-8 或 UTF-8 BOM。

## 导出小红书和朋友圈图片

```powershell
# 小红书 3:4，1080×1440
node scripts/export_social.mjs "album.html" --preset xhs

# 朋友圈方图，1080×1080
node scripts/export_social.mjs "album.html" --preset moments

# 竖版图文
node scripts/export_social.mjs "album.html" --preset portrait
```

输出目录会包含：

- `01-cover.png`、`02-focus.png` 等连续编号图片。
- `upload-order.txt`：按这个顺序上传。
- `manifest.json`：记录尺寸和全部文件。

默认 PNG 导出只需要系统已有的 Edge、Chrome 或 Chromium。需要 JPG 时安装 Playwright Core 并加 `--format jpg`：

```powershell
npm install playwright-core
node scripts/export_social.mjs "album.html" --preset xhs --format jpg --quality 88
```

没有自动找到浏览器时，可用 `--browser` 指定路径。

## 压缩已有单文件 HTML

如果相册是其他软件生成的 standalone HTML，图片以内嵌 base64 形式塞进文件里，文件可能会非常大。可以直接压缩内嵌图片，生成一个更适合离线阅读的小版 HTML，不改原文件：

```powershell
python scripts/compress_standalone.py "D:\Photos\贵阳\album_standalone.html"

# 指定输出位置
python scripts/compress_standalone.py "D:\Photos\贵阳\album_standalone.html" `
  -o "D:\Photos\贵阳\album_standalone_small.html"

# 调整尺寸和质量
python scripts/compress_standalone.py "album_standalone.html" --max-edge 1800 --quality 82
```

默认行为：

- 扫描 `data:image/...;base64` 内嵌图片。
- 将图片最长边缩到 1800px，并转成适合离线阅读的 JPEG。
- 输出 `_small.html`，不覆盖原 HTML。
- 某张小图压完反而更大时，保留原图。

压缩后建议打开小版 HTML 检查封面、中间页和尾页；需要 PDF 时，再从小版 HTML 打印或导出 PDF。

## 浏览器快捷键

- 方向键、空格、Page Up / Page Down：翻页
- Home / End：第一页 / 最后一页
- `T`：切换主题
- `F`：全屏
- `Esc`：关闭大图

## 三套主题

| 主题 | 适合 |
|---|---|
| `warm` | 家人、朋友、宠物、旅行、普通生活 |
| `silver` | 街拍、建筑、黑白、低饱和照片 |
| `night` | 夜景、演出、聚会、霓虹 |

相册打开后也可用底部按钮实时切换。

## 设计原则

不以技术好坏为标准，以“意义”和“人情味”为核心。所有照片先问一句：

> 当时为什么按下快门？

如果一张照片能回答这个问题，即使它有点糊、有点歪、构图不完美，也可能值得留下。如果回答不了，哪怕它很漂亮，也要谨慎使用。

选图时依次考察：

1. **快门理由**：为什么当时要拍下这一张，能否从素材或画面中找到答案。
2. **刺点**：画面中是否有能像箭一样射中你的细节，例如一个眼神、一只手、一个旧物件。
3. **凡俗真实**：是否捕捉到了未加粉饰、随性甚至略带笨拙的真实瞬间。
4. **此曾在**：是否温柔地对抗了时间的流逝，证明某种珍贵事物确实存在过。
5. **叙事与羁绊**：是否记录了人与人之间的连接，是否具备超越私人范畴的共鸣。
6. **灵魂投射**：是否映照出拍摄者独特的生命体验与情感体温。

一张因为手抖而模糊、但定格了爱人最开怀大笑的快照，其意义远超完美但冰冷的风光明信片。

其他原则：

- 照片优先，装饰退后；一页只保留一个视觉重心。
- 文案解释“为什么拍下”，不重复描述“画面里有什么”。
- 用户原话优先于 AI 文案。
- 没有真实文字时宁可留白。
- 单文件离线可用，不依赖外部资源。

## 项目结构

```text
photo-album-skill/
├── README.md
├── SKILL.md
├── examples/
│   └── shangu-cafe/            ← 示例画册
├── scripts/
│   ├── build_album.py          ← 零依赖 HTML 画册生成器
│   ├── compress_standalone.py  ← 压缩已有单文件 HTML 的内嵌图片
│   └── export_social.mjs       ← 小红书/朋友圈图片导出
├── assets/
│   └── template.html           ← HTML 模板
└── references/
    ├── design-principles.md    ← 日常画册设计原则
    ├── layouts.md              ← 页面布局参考
    ├── prompts.md              ← 可调整的提示词
    ├── social-export.md        ← 社交图片导出规则
    └── themes.md               ← 三套主题色
```

## License

MIT
