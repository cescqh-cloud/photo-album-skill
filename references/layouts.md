# 页面布局

所有页面使用 `<section class="spread">`。模板会自动补页码、动画、导航和灯箱。

## 封面

优先使用横图。标题短，副标题可只写照片数量或时间。

```html
<section class="spread hero dark">
  <img class="photo hero-img" src="DATA_URI" alt="封面照片">
  <div class="cover">
    <p class="meta" data-anim>PHOTO ALBUM</p>
    <h1 class="h-hero" data-anim>周末散步</h1>
    <p class="lead" data-anim>24 张照片</p>
  </div>
</section>
```

## focus · 单图

竖图、重要照片和节奏停顿使用。背景自动取同图做模糊色场，主体保持完整。

```html
<section class="spread dark focus-page">
  <div class="focus-haze" aria-hidden="true"></div>
  <p class="kicker" data-anim>02</p>
  <div class="focus-shell">
    <img class="photo" src="DATA_URI" alt="照片说明">
  </div>
  <p class="caption" data-anim>用户提供的原话，可省略。</p>
</section>
```

## duo · 双图

适合动作前后、远景与特写、两个人或两个相似物件。

```html
<section class="spread">
  <p class="kicker" data-anim>03</p>
  <div class="duo">
    <div class="photo-card"><img class="photo" src="DATA_URI" alt=""></div>
    <div class="photo-card"><img class="photo" src="DATA_URI" alt=""></div>
  </div>
</section>
```

## triptych · 一主两辅

一张环境或人物主图，加两张动作/物件细节。

```html
<section class="spread">
  <p class="kicker" data-anim>04</p>
  <div class="triptych">
    <div class="photo-card"><img class="photo" src="DATA_URI" alt=""></div>
    <div class="photo-card"><img class="photo" src="DATA_URI" alt=""></div>
    <div class="photo-card"><img class="photo" src="DATA_URI" alt=""></div>
  </div>
</section>
```

第一张会占左侧大区域。确保它比另外两张更适合作主图。

## grid · 四图碎片

适合同一地点、同一活动或一组生活细节。不要把完全不相关的照片硬放在一起。

```html
<section class="spread">
  <p class="kicker" data-anim>05</p>
  <div class="grid-2x2">
    <div class="photo-card"><img class="photo" src="DATA_URI" alt=""></div>
    <div class="photo-card"><img class="photo" src="DATA_URI" alt=""></div>
    <div class="photo-card"><img class="photo" src="DATA_URI" alt=""></div>
    <div class="photo-card"><img class="photo" src="DATA_URI" alt=""></div>
  </div>
</section>
```

## story · 照片与原话

只有用户提供真实文字时使用。加 `reverse` 可交换左右。

```html
<section class="spread">
  <div class="story reverse">
    <div class="story-copy">
      <p class="kicker" data-anim>记一笔</p>
      <h2 class="h-xl" data-anim>到家之前</h2>
      <div class="rule" data-anim></div>
      <p class="body-zh" data-anim>用户自己的文字。</p>
    </div>
    <div class="photo-card"><img class="photo" src="DATA_URI" alt=""></div>
  </div>
</section>
```

## 尾页

```html
<section class="spread end-page">
  <div class="end-mark" data-anim>·</div>
  <p class="meta" data-anim>周末散步</p>
  <h2 class="h-xl" data-anim>共 24 张照片</h2>
</section>
```

## 按照片数量组织

| 照片数 | 建议 |
|---|---|
| 1–6 | 封面 + 2–4 个 focus/duo + 尾页 |
| 7–20 | focus、duo、triptych 小循环 |
| 21–50 | 每 4–6 页加入 grid，避免全是大图 |
| 50+ | 先去重和选图；不要靠堆页面解决 |

快速生成器会自动使用这些布局。精排时优先调整照片分组和主次，不要先加装饰。
