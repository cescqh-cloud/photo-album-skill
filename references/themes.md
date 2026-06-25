# 画册主题色预设

两套主题，适配不同类型的摄影。

---

## 暖墨（Warm Ink）— 默认

**适合**：人物、旅行、日常记录、温暖的回忆
**调性**：米白底 + 深棕字，像牛皮纸笔记本或老照片

```css
--ink:#1a1612;
--ink-rgb:26,22,18;
--paper:#f5f0e8;
--paper-rgb:245,240,232;
--paper-tint:#ebe5d9;
--ink-tint:#2a2420;
--accent:#8b7355;
--accent-rgb:139,115,85;
```

---

## 银盐（Silver Halide）

**适合**：街拍、建筑、黑白摄影、艺术摄影、冷静的记录
**调性**：灰白底 + 深灰字，像暗房里的银盐相纸

```css
--ink:#1a1a1a;
--ink-rgb:26,26,26;
--paper:#f0f0f0;
--paper-rgb:240,240,240;
--paper-tint:#e5e5e5;
--ink-tint:#2a2a2a;
--accent:#666;
--accent-rgb:102,102,102;
```

---

## 切换方法

在 `<body>` 上加 class：

```html
<body>           <!-- 默认暖墨 -->
<body class="silver">  <!-- 银盐 -->
```
