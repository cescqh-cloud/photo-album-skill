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

## 适合谁用

- 旅行回来，照片很多，但不知道怎么整理成一条线。
- 想把家人、朋友、爱人、宠物或普通日常做成一本能回看的相册。
- 想发小红书、朋友圈、公众号，但不想一张张手动排版。
- 有很多散落照片，想让它们重新成为一个完整的故事。
- 想把已有的超大 HTML 相册压小一点，方便离线阅读和分享。

## 怎么用

在 Codex 或 Claude Code 里直接说：

```text
帮我把 D:\Photos\周末散步 做成一本日常画册。
```

想认真选图和组织故事，可以说：

```text
做成叙事精排版，保留真实的小细节，不要写模板化文案。
```

想让文案更贴近回忆，可以加一句：

```text
重点帮我想清楚：这些照片当时为什么会被拍下来。
```

想发小红书或朋友圈：

```text
做成画册，再导出小红书图片组。
```

## 安装

如果你在 Codex 中使用，可以把仓库放到本地 skills 目录：

```powershell
git clone https://github.com/cescqh-cloud/photo-album-skill.git `
  "$env:USERPROFILE\.codex\skills\photo-album-skill"
```

也可以作为普通命令行工具使用：

```powershell
git clone https://github.com/cescqh-cloud/photo-album-skill.git
cd photo-album-skill
```

需要 Python 3.8+。基础 HTML 画册生成功能零依赖。安装 Pillow 后可以自动修正 EXIF 方向并压缩大图：

```powershell
python -m pip install Pillow
```

## 快速开始

```powershell
python scripts/build_album.py "D:\Photos\周末散步"
```

默认输出当前目录下的 `album.html`。

常用写法：

```powershell
# 指定标题与输出位置
python scripts/build_album.py "D:\Photos\周末散步" `
  --title "周末散步" `
  -o "D:\Photos\周末散步.html"

# 扫描子目录，并限制成品照片数量
python scripts/build_album.py "D:\Photos\2026" --recursive --max-photos 60

# 更偏图文编辑排版
python scripts/build_album.py "D:\Photos\周末" --composition editorial

# 更偏图片组合与排列
python scripts/build_album.py "D:\Photos\周末" --composition gallery

# 街拍 / 黑白
python scripts/build_album.py "D:\Photos\街拍" --theme silver

# 夜景 / 演出 / 聚会
python scripts/build_album.py "D:\Photos\夜晚" --theme night
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
