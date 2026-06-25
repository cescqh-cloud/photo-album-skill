# 主题预设

模板通过 `<body data-theme="...">` 设置初始主题，浏览者也可用底部按钮循环切换。

## warm · 暖日常（默认）

适合家人、朋友、宠物、旅行、食物和普通手机照片。

```css
--paper:#f4efe6;
--paper-2:#e9dfd1;
--ink:#201a16;
--muted:#766b61;
--accent:#b76545;
--dark:#171310;
--light:#fffaf1;
```

关键词：奶油纸、旧相册、自然、松弛。不要额外叠加强烈棕色滤镜。

## silver · 银盐

适合街拍、建筑、黑白、阴天和低饱和照片。

```css
--paper:#f1f1ef;
--paper-2:#dfdfdc;
--ink:#171819;
--muted:#6e7173;
--accent:#5c727f;
--dark:#111315;
--light:#f8f8f5;
```

关键词：清醒、克制、编辑感。

## night · 夜蓝

适合夜景、演出、聚会、霓虹和舞台照片。

```css
--paper:#141927;
--paper-2:#202a3c;
--ink:#eef0f7;
--muted:#aeb6c8;
--accent:#ff9f68;
--dark:#090c14;
--light:#f4f0e8;
```

关键词：夜色、微光、不过度赛博。

## 自动选择

- 人物、宠物、旅行、生活混拍：`warm`
- 黑白照片占多数，或建筑/街道为主：`silver`
- 夜景和暗光照片占多数：`night`

无法判断时使用 `warm`。
