# 画册页面布局库

所有布局基于 `<section class="spread ...">` 结构。图片用 base64 内嵌或相对路径。

---

## L01 · 封面（Cover）

全屏照片 + 标题叠加在底部。

```html
<section class="spread hero dark">
  <img class="photo hero-img" src="data:image/jpeg;base64,..." alt="">
  <div class="cover">
    <div class="meta" data-anim>2024 · 夏</div>
    <h1 class="h-hero" data-anim>一个人的旅行</h1>
    <p class="lead" data-anim>从城市到海边，三天两夜</p>
  </div>
</section>
```

---

## L02 · 全屏照片（Full Bleed）

照片铺满整个页面，可选底部文字叠加。

```html
<section class="spread hero">
  <div class="full-photo">
    <img class="photo" src="..." alt="">
    <div class="overlay" data-anim>
      <p class="lead">海边的日落，空气里有盐的味道。</p>
    </div>
  </div>
</section>
```

不带文字的纯照片版：

```html
<section class="spread hero">
  <img class="photo hero-img" src="..." alt="">
</section>
```

---

## L03 · 双页并置（Duo）

两张照片左右并排，产生对比或呼应。

```html
<section class="spread">
  <div class="kicker" data-anim>路上</div>
  <div class="duo tall" style="flex:1; margin-top:2vh">
    <img class="photo" src="..." alt="">
    <img class="photo" src="..." alt="">
  </div>
  <div class="caption" data-anim>左边是出发，右边是到达。</div>
  <span class="page-num">03</span>
</section>
```

---

## L04 · 左文右图（Text + Photo）

文字在左，照片在右。适合叙述性段落。

```html
<section class="spread">
  <div class="text-photo" style="flex:1">
    <div class="text-col">
      <div class="kicker" data-anim>第一天</div>
      <h2 class="h-xl" data-anim>到达</h2>
      <div class="rule" data-anim></div>
      <p class="body-zh" data-anim>
        下午三点的阳光斜斜地照进来，把行李箱的影子拉得很长。
        放下背包的第一件事，是打开窗户。
      </p>
    </div>
    <figure>
      <img class="photo" src="..." alt="">
      <figcaption class="caption">窗外的景色</figcaption>
    </figure>
  </div>
  <span class="page-num">04</span>
</section>
```

---

## L05a · 图片网格 2x2

四张照片均匀排列。适合同主题多图展示。

```html
<section class="spread">
  <div class="kicker" data-anim>细节</div>
  <h2 class="h-md" data-anim>路边的小东西</h2>
  <div class="grid-2x2" style="margin-top:3vh">
    <div class="grid-item"><img class="photo" src="..." alt=""></div>
    <div class="grid-item"><img class="photo" src="..." alt=""></div>
    <div class="grid-item"><img class="photo" src="..." alt=""></div>
    <div class="grid-item"><img class="photo" src="..." alt=""></div>
  </div>
  <span class="page-num">05</span>
</section>
```

---

## L05b · 图片网格 3x3

九张照片密集排列。适合街拍、快照风格。

```html
<section class="spread">
  <div class="kicker" data-anim>碎片</div>
  <div class="grid-3x3" style="flex:1; margin-top:2vh">
    <div class="grid-item"><img class="photo" src="..." alt=""></div>
    <!-- 重复 9 张 -->
  </div>
  <span class="page-num">06</span>
</section>
```

---

## L05c · 图片网格 2x3

六张照片，三列两行。适合旅行记录。

```html
<section class="spread">
  <div class="kicker" data-anim>沿途</div>
  <div class="grid-2x3" style="flex:1; margin-top:2vh">
    <div class="grid-item"><img class="photo" src="..." alt=""></div>
    <!-- 重复 6 张 -->
  </div>
  <span class="page-num">07</span>
</section>
```

---

## L06 · 大字引言（Quote）

纯文字，居中，适合用户的心情记录或金句。

```html
<section class="spread dark">
  <div class="quote-page">
    <div>
      <div class="kicker" data-anim>写在出发前</div>
      <div class="rule center" data-anim></div>
      <p class="q-text" data-anim>
        "不需要去很远的地方，<br>
        只需要离开现在的位置。"
      </p>
      <div class="q-cite" data-anim>— 手机备忘录 · 凌晨两点</div>
    </div>
  </div>
  <span class="page-num">08</span>
</section>
```

---

## L07 · 章节分隔（Chapter Divider）

大标题 + 可选引言，标记叙事转折。

```html
<section class="spread dark">
  <div class="chapter">
    <div class="meta" data-anim>第二章</div>
    <div class="rule center" data-anim></div>
    <h1 class="h-hero" data-anim>海边</h1>
    <p class="lead" data-anim style="max-width:50vw; text-align:center">
      四个小时的车程，换一片海。
    </p>
  </div>
  <span class="page-num">09</span>
</section>
```

---

## L08 · 照片 + 说明（Photo + Caption）

单张照片配详细说明。适合有故事的照片。

```html
<section class="spread">
  <div class="kicker" data-anim>那个下午</div>
  <figure style="flex:1; display:flex; flex-direction:column; margin-top:2vh">
    <img class="photo" src="..." alt="" style="flex:1; object-fit:contain">
    <figcaption style="margin-top:2vh">
      <p class="body-zh" data-anim>
        渔船靠岸的时候，天已经开始暗了。
        渔民把网收起来，动作很慢，像是在和大海做一个缓慢的告别。
      </p>
    </figcaption>
  </figure>
  <span class="page-num">10</span>
</section>
```

---

## L09 · 时间线（Timeline）

按时间排列的照片和文字。适合旅程记录。

```html
<section class="spread">
  <div class="kicker" data-anim>行程</div>
  <h2 class="h-xl" data-anim>三天两夜</h2>
  <div class="timeline">
    <div class="tl-item" data-anim>
      <div class="tl-date">Day 1</div>
      <div class="tl-content">
        <h3 class="h-md">出发</h3>
        <p class="body-zh">早上七点的高铁，窗外的田野从绿色变成黄色。</p>
      </div>
    </div>
    <div class="tl-item" data-anim>
      <div class="tl-date">Day 2</div>
      <div class="tl-content">
        <h3 class="h-md">海边</h3>
        <p class="body-zh">租了一辆电动车，沿着海岸线骑了一下午。</p>
      </div>
    </div>
    <!-- 更多时间节点 -->
  </div>
  <span class="page-num">11</span>
</section>
```

---

## L10 · 尾页（Colophon）

简洁的结束页，画册信息。

```html
<section class="spread">
  <div class="colophon">
    <div class="meta">THE END</div>
    <div class="rule center"></div>
    <p class="lead" style="max-width:40vw; text-align:center">
      这些照片拍于 2024 年夏天，<br>
      从一座城市到一片海。
    </p>
    <div class="rule center"></div>
    <div class="meta">2024 · 6 月</div>
  </div>
</section>
```

---

## 组合建议

一本 20 页画册的推荐结构：

| 页 | 布局 | 内容 |
|---|---|---|
| 1 | L01 封面 | 主图 + 标题 |
| 2 | L06 引言 | 写在前面的话 |
| 3 | L07 章节 | 第一章标题 |
| 4 | L02 全屏 | 开场大图 |
| 5 | L04 左文右图 | 叙述 + 照片 |
| 6 | L05a 网格 2x2 | 细节照片 |
| 7 | L03 并置 | 对比两张 |
| 8 | L02 全屏 | 过渡大图 |
| 9 | L07 章节 | 第二章标题 |
| 10 | L04 左文右图 | 叙述 + 照片 |
| 11 | L05b 网格 3x3 | 碎片快照 |
| 12 | L08 照片说明 | 有故事的照片 |
| 13 | L06 引言 | 心情记录 |
| 14 | L03 并置 | 呼应两张 |
| 15 | L02 全屏 | 高潮大图 |
| 16 | L05a 网格 2x2 | 收尾细节 |
| 17 | L09 时间线 | 行程回顾 |
| 18 | L04 左文右图 | 最后的叙述 |
| 19 | L06 引言 | 结尾金句 |
| 20 | L10 尾页 | 画册信息 |
