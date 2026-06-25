# photo-album-skill

把照片和文字做成自然、好翻的 HTML 画册，也能逐页导出成小红书或朋友圈图片组。

默认体验很简单：给一个目录，先出一版；标题、主题和叙事之后再改。

## 快速开始

需要 Python 3.8+，基础功能零依赖。

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

# 街拍 / 黑白
python scripts/build_album.py "D:\Photos\街拍" --theme silver

# 夜景 / 演出 / 聚会
python scripts/build_album.py "D:\Photos\夜晚" --theme night

# 扫描子目录，并限制成品照片数量
python scripts/build_album.py "D:\Photos\2026" --recursive --max-photos 60

# 更偏图文编辑排版
python scripts/build_album.py "D:\Photos\周末" --composition editorial

# 更偏图片组合与排列
python scripts/build_album.py "D:\Photos\周末" --composition gallery
```

生成器会自动：

- 扫描 JPG、JPEG、PNG、WEBP、GIF。
- 优先按 EXIF 拍摄时间排序，读不到时按文件名自然排序。
- 根据横竖比例、文字长度和前后照片自动组合页面。
- 将图片内嵌为 data URI，输出单个离线 HTML。
- 自动加入翻页按钮、键盘导航、进度、主题切换、图片放大和打印样式。

如环境安装 Pillow，生成器会自动纠正 EXIF 方向并压缩大图；没有 Pillow 也可正常生成，只是文件更大。HEIC/HEIF 需先转换为浏览器支持的格式。

## 导出小红书和朋友圈图片

```powershell
# 小红书 3:4，1080×1440
node scripts/export_social.mjs "album.html" --preset xhs

# 朋友圈方图，1080×1080
node scripts/export_social.mjs "album.html" --preset moments

# 导出 JPG（需要 playwright-core）
npm install playwright-core
node scripts/export_social.mjs "album.html" --preset xhs --format jpg --quality 88
```

输出目录会包含：

- `01-cover.png`、`02-focus.png` 等连续编号图片。
- `upload-order.txt`：按这个顺序上传。
- `manifest.json`：记录尺寸和全部文件。

默认 PNG 导出只需要系统已有的 Edge、Chrome 或 Chromium。需要 JPG 时安装 Playwright Core 并加 `--format jpg`。

没有自动找到浏览器时，可用 `--browser` 指定路径。

## 加标题、说明和指定封面

在照片目录放一个 `album.json`：

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

## 浏览器快捷键

- 方向键、空格、Page Up / Page Down：翻页
- Home / End：第一页 / 最后一页
- `T`：切换主题
- `F`：全屏
- `Esc`：关闭大图

## 在 Claude Code 中使用

直接说：

> 帮我把 `D:\Photos\周末散步` 做成一本日常画册。

默认会先做"暖日常"版本。想认真选图和组织故事时，可以补一句：

> 做成叙事精排版，保留真实的小细节，不要写模板化文案。

想发小红书：

> 做成画册，再导出小红书图片组。

## 三套主题

| 主题 | 适合 |
|---|---|
| `warm` | 家人、朋友、宠物、旅行、普通生活 |
| `silver` | 街拍、建筑、黑白、低饱和照片 |
| `night` | 夜景、演出、聚会、霓虹 |

相册打开后也可用底部按钮实时切换。

## 图片大小

没有 Pillow 时，生成器直接内嵌原图，功能不受影响，但 HTML 可能较大。

可选安装 Pillow：

```powershell
python -m pip install Pillow
```

安装后会自动：

- 修正手机照片的 EXIF 方向。
- 将大图最长边缩到 2200px。
- 对 JPEG / WEBP 做适度压缩。

生成器不修改原照片。HEIC / HEIF 需先转换为 JPG、PNG 或 WEBP。

## 设计原则

不以技术好坏为标准，以"意义"和"人情味"为核心。选图时依次考察：

1. **刺点（Punctum）**：画面中是否有能像箭一样射中你的细节——一个眼神、一只手、一个旧物件
2. **凡俗真实（Vernacular Authenticity）**：是否捕捉到了未加粉饰的、随性甚至略带笨拙的真实瞬间
3. **此曾在（Ça-a-été）**：是否温柔地对抗了时间的流逝，证明某种珍贵事物确实存在过
4. **叙事与羁绊（Narrative Power & Social Bond）**：是否记录了人与人之间的连接，是否具备超越私人范畴的普遍共鸣
5. **灵魂投射（Identity Projection）**：是否映照出拍摄者独特的生命体验与情感体温

一张因为手抖而模糊、但定格了爱人最开怀大笑的快照，其意义远超完美但冰冷的风光明信片。

其他原则：

- 照片优先，装饰退后；一页只保留一个视觉重心
- 没有真实文字时宁可留白
- 单文件离线可用，不依赖外部资源

## 项目结构

```text
photo-album-skill/
├── README.md
├── SKILL.md
├── .gitignore
├── scripts/
│   ├── build_album.py          ← 零依赖 HTML 画册生成器
│   └── export_social.mjs       ← 小红书/朋友圈图片导出
├── assets/
│   └── template.html           ← HTML 模板（warm/silver/night）
└── references/
    ├── design-principles.md    ← 日常画册设计原则
    ├── layouts.md              ← 页面布局参考
    ├── prompts.md              ← 可调整的提示词
    └── themes.md               ← 三套主题色
```

## License

MIT
