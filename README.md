# photo-album-skill

把一批照片做成真正愿意翻完的画册。

## 写在前面

又不是参加比赛，没人去对你的照片评头论足点评好坏。你是你生活或者照片的唯一主体。

摄影其实是一种转译——把你看到的记录下来，也许可以让别人解读。一张照片在手机屏幕上看，和真正变成一本书来翻阅，体验大不相同。把记忆从数据流里打捞出来，捧在手心里。

这个 skill 不会替你表达。它帮你排版、分类、引导，但文字和照片都是你自己的。AI 的文字一定不能参与感过强，包括幻觉。你是唯一的主体。

## 设计来源

- **阿兰·德波顿《旅行的艺术》**：旅行的意义不在于目的地，而在于途中的观察。好的画册不是照片集合，而是一个有节奏的叙事。
- **狂阿弥画册经验**：先想象再动手，找对标，选图留余地，排序比排版更重要。并置、旋转、前后呼应、大小节奏——这些排版技巧普通人也能用。
- **歸藏 guizang 设计语言**：衬线标题 + 非衬线正文 + 等宽元数据，杂志感排版，留白即呼吸。
- **ponytail 原则**：能一行不写两行，删减优于添加，最少的代码才不会出错。

## 快速开始

### 环境要求

- Python 3.8+（仅标准库，零依赖）
- 可选：Pillow（自动纠正 EXIF 方向、压缩大图）

### 生成画册

```powershell
# 最简用法：指定照片目录
python scripts/build_album.py "D:/Photos/周末散步"

# 指定标题和主题
python scripts/build_album.py "D:/Photos/周末散步" --title "周末散步" --theme warm

# 银盐主题（适合街拍、建筑、黑白）
python scripts/build_album.py "D:/Photos/街拍" --theme silver

# 夜景主题
python scripts/build_album.py "D:/Photos/酒吧" --theme night

# 按文件名排序（默认按拍摄时间）
python scripts/build_album.py "D:/Photos/旅行" --sort name

# 限制照片数量
python scripts/build_album.py "D:/Photos/旅行" --max-photos 60

# 递归扫描子目录
python scripts/build_album.py "D:/Photos/2024" --recursive

# 指定输出路径
python scripts/build_album.py "D:/Photos/旅行" -o "D:/output/album.html"
```

### 在 Claude Code 中使用

直接说：

> "帮我把 D:/Photos/周末散步 做成画册"

Claude 会：
1. 扫描目录中的照片和文字素材
2. 按拍摄时间排序
3. 自动生成一本可翻阅的 HTML 画册
4. 告诉你文件路径和可以调整的方向

## 三种使用方式

### 1. 快速日常版（默认）

扔一个照片目录进去，直接出成品。适合"先出一版看看"的心态。

```powershell
python scripts/build_album.py "照片目录"
```

生成器自动完成：
- 读取 JPG/PNG/WEBP/GIF
- 按拍摄时间排序（读不到 EXIF 则按文件名）
- 自动组合封面、单图、双图、网格页面
- 图片内嵌为 data URI，单文件离线可用
- 自带翻页、键盘导航、主题切换、图片放大、打印样式

### 2. 叙事精排版

适合"想认真做一本"的场景。在 Claude Code 中说：

> "帮我把这些照片做成一本画册，想讲一个故事"

Claude 会：
- 批量查看照片，识别时间、场景、人物
- 删除重复和失焦照片（但保留有纪念意义的"不完美"）
- 选择叙事线（时间/空间/情绪/主题）
- 按 4 段节奏排版：开场 → 展开 → 重音 → 收束
- 使用 `references/layouts.md` 中的布局精调

### 3. AI 引导版

不知道写什么？Claude 会问你具体问题：

> "拍这张照片的时候，你在想什么？"
> "是什么让你停下来举起相机？"
> "如果用一个词形容当时的感受，是什么？"

你的回答会直接进入画册，不会被改写成"美文"。

## 主题

| 主题 | 适合 | 调性 |
|---|---|---|
| `warm`（默认） | 人物、旅行、日常、宠物 | 柔和米白 + 墨色文字 |
| `silver` | 街拍、建筑、黑白、艺术 | 灰白底 + 深灰字 |
| `night` | 夜景、演出、聚会、霓虹 | 深底 + 低亮度文字 |

切换主题：
```powershell
python scripts/build_album.py "照片目录" --theme silver
```

## 素材规则

- **图片**：`.jpg` `.jpeg` `.png` `.webp` `.gif`（HEIC 需先转换）
- **文字**：同目录的 `.txt` `.md` 文件会自动读取
- **排序**：优先 EXIF 拍摄时间，其次文件名自然排序
- **原则**：不移动、不重命名、不改写原照片

## 文字处理

| 情况 | 做法 |
|---|---|
| 用户有文字 | 轻量校对，保留原口吻 |
| 用户没有文字 | 只用日期、地点、文件夹名、画面可见事实 |
| 需要情绪文字 | 先问一个具体问题，根据回答整理，不编造 |

标题像相册标签，不像命题作文。用"时间 + 地点/动作/人物"，不用"美好时光""难忘旅程"。

## 排版技巧

来自狂阿弥画册经验，普通人也能用：

- **并置**：左右放两张不相关的照片，产生新意义
- **旋转**：竖构图变横放，打破方向感
- **前后呼应**：前页远景 → 后页特写
- **相似元素串联**：圆形 → 圆形，自然过渡
- **大小节奏**：大图 → 小图 → 文字 → 大图，像音乐

## 文件结构

```
photo-album-skill/
├── SKILL.md                    ← 技能定义（Claude 读取）
├── README.md                   ← 你在读的这个
├── scripts/
│   └── build_album.py          ← 零依赖生成器
├── assets/
│   └── template.html           ← HTML 画册模板
└── references/
    ├── layouts.md              ← 10 种页面布局
    ├── themes.md               ← 3 套主题色
    ├── prompts.md              ← 提示词配置（可调整）
    └── design-principles.md    ← 设计原则
```

## 质量原则

- 照片优先，装饰退后
- 保留"不完美但有记忆"的照片
- 一页只保留一个视觉重心
- 没有真实文字时宁可留白
- 单文件离线可用，不依赖外部资源

## 安装为 Claude Code Skill

```powershell
git clone https://github.com/cescqh-cloud/photo-album-skill.git ~/.claude/skills/photo-album-skill
```

或复制到项目目录的 `.claude/skills/` 下。

## License

MIT
