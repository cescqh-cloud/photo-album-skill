# 社交平台图片导出

## 默认预设

| 预设 | 尺寸 | 用途 |
|---|---:|---|
| `xhs` | 1080×1440，3:4 | 小红书图文笔记封面与连续配图 |
| `moments` | 1080×1080，1:1 | 微信朋友圈多图与九宫格预览 |
| `portrait` | 1080×1440，3:4 | 朋友圈竖版图文或其他平台 |

平台展示规则可能变化。比例比像素值更重要；如用户有明确渠道规范，使用 `--width` 与 `--height` 覆盖预设。

## 导出命令

```powershell
node scripts/export_social.mjs "album.html" --preset xhs
node scripts/export_social.mjs "album.html" --preset moments
node scripts/export_social.mjs "album.html" --preset portrait
```

自定义：

```powershell
node scripts/export_social.mjs "album.html" `
  --preset xhs `
  --width 1242 `
  --height 1660 `
  --format png `
  --out "social\custom"
```

默认 PNG 导出只需要 Node.js 和系统已有的 Edge、Chrome 或 Chromium。脚本会自动查找浏览器。

需要 JPG 时安装 Playwright Core：

```powershell
npm install playwright-core
node scripts/export_social.mjs "album.html" --preset xhs --format jpg
```

脚本优先使用系统已有的 Edge、Chrome 或 Chromium，避免额外下载浏览器。也可显式指定：

```powershell
node scripts/export_social.mjs "album.html" `
  --preset xhs `
  --browser "C:\Program Files (x86)\Microsoft\Edge\Application\msedge.exe"
```

## 输出内容

```text
album-xhs/
├── 01-cover.png
├── 02-focus.png
├── 03-duo.png
├── ...
├── upload-order.txt
└── manifest.json
```

文件名前两位数字就是上传顺序。不要让用户再手工重命名。

## 小红书版式

- 全组统一使用 3:4，不混入横图或方图画布。
- 首图保留中央焦点；标题不贴近顶部、底部和左右边缘。
- 横图放进竖版画布时优先留白、上下排版或作为主图加细节，不强行裁成竖图。
- 图文页使用上文下图，文字宽度短、字号足够大。
- 一组图片的主题、底色和圆角保持一致。

## 朋友圈版式

- 多图默认导出方形，降低九宫格缩略预览的不确定裁切。
- 人脸、标题和主要物体不要贴边。
- 九张以上仍连续编号；用户按当前客户端允许的数量分批上传。
- 用户明确更在意单张展开效果时，改用 `portrait`。

## 导出验收

1. 用图片尺寸检查工具确认全部同宽同高。
2. 打开第 1、2、中间、最后一张，检查文字没有溢出。
3. 确认 `upload-order.txt` 与文件名顺序一致。
4. 检查横图没有被裁掉人物，竖图没有被错误横切。
5. PNG 适合细字和图文卡片；需要较小文件时使用 JPG，默认质量 92。
