# 图文与图片编排

所有页面使用 `<section class="spread" data-layout="...">`。先判断信息层级，再选择布局。

## 选择顺序

1. 先找主图：这一页第一眼必须看哪张？
2. 再找关系：其他照片是在补充环境、动作、人物还是细节？
3. 最后决定文字：它是否提供画面中没有的信息？

如果无法回答第 2 或第 3 个问题，就减少照片或删掉文字。

## 图文布局

### story · 长文字 + 单图

适合 28–100 个汉字的用户原话。文字与图片左右排列，导出 3:4 时自动改为上文下图。

```html
<section class="spread" data-layout="story">
  <div class="story reverse">
    <div class="story-copy">
      <p class="kicker" data-anim>记一笔</p>
      <div class="rule" data-anim></div>
      <p class="lead" data-anim>用户自己的文字。</p>
    </div>
    <div class="photo-card"><img class="photo" src="DATA_URI" alt=""></div>
  </div>
</section>
```

规则：

- 一页只放一段话，不超过 100 个汉字。
- 文字不要逐字描述照片，应补充时间、动作前后或用户记忆。
- 人像注视方向朝左时，文字优先放左侧；朝右时反过来。

### photo-note · 短文字旁注

适合 8–28 个汉字。照片占约 2/3，文字是旁注，不做大标题。

```html
<section class="spread" data-layout="photo-note">
  <div class="photo-note">
    <div class="photo-card"><img class="photo" src="DATA_URI" alt=""></div>
    <div class="photo-note-copy">
      <p class="kicker" data-anim>旁注</p>
      <p class="lead" data-anim>回家前，又绕去看了一眼海。</p>
    </div>
  </div>
</section>
```

### bleed-note · 图上短文

只用于主体区域明确、存在大块留白的横图。文字卡片压在留白处，不覆盖人脸。

```html
<section class="spread bleed-note dark" data-layout="bleed-note">
  <img class="photo" src="DATA_URI" alt="">
  <div class="bleed-note-copy">
    <p class="kicker">傍晚</p>
    <p class="lead">风停下来的那几分钟。</p>
  </div>
</section>
```

主体位置不确定时不要使用。

## 图片布局

### focus · 单图停顿

用于高潮、收束、合照和需要完整构图的竖图。宁可留黑边，也不要切掉重要人物。

```html
<section class="spread dark focus-page" data-layout="focus">
  <div class="focus-haze" aria-hidden="true"></div>
  <div class="focus-shell"><img class="photo" src="DATA_URI" alt=""></div>
</section>
```

### duo · 双图并置

只有存在明确关系时才并置：

- 动作前后。
- 远景与特写。
- 相同颜色、形状或视线方向。
- 两个人物或两个地点的对照。

变体：

- `duo portrait-pair`：两张竖图等宽完整展示。
- `duo mixed`：一张横图为主，一张竖图为辅。
- `duo equal`：两张同方向、同权重图片。

```html
<section class="spread" data-layout="duo">
  <div class="duo portrait-pair">
    <div class="photo-card"><img class="photo" src="DATA_URI" alt=""></div>
    <div class="photo-card"><img class="photo" src="DATA_URI" alt=""></div>
  </div>
</section>
```

### triptych · 一主两辅

主图交代环境或人物，辅图补充动作和细节。三张图不能同权。

```html
<section class="spread" data-layout="triptych">
  <div class="triptych top-lead">
    <div class="photo-card"><img class="photo" src="DATA_URI" alt="主图"></div>
    <div class="photo-card"><img class="photo" src="DATA_URI" alt="细节一"></div>
    <div class="photo-card"><img class="photo" src="DATA_URI" alt="细节二"></div>
  </div>
</section>
```

第一张必须是主图。横向主图使用 `top-lead`；竖向主图使用默认左主右辅结构。

### grid · 四图碎片

适合同一场景、同一时间段或同一动作的四个碎片。

```html
<section class="spread" data-layout="grid">
  <div class="grid-2x2">
    <div class="photo-card"><img class="photo" src="DATA_URI" alt=""></div>
    <div class="photo-card"><img class="photo" src="DATA_URI" alt=""></div>
    <div class="photo-card"><img class="photo" src="DATA_URI" alt=""></div>
    <div class="photo-card"><img class="photo" src="DATA_URI" alt=""></div>
  </div>
</section>
```

网格页之后安排 `focus` 或留白较多的图文页，让节奏重新变松。

## 封面与尾页

- 封面只保留标题、副标题和一张主图。
- 小红书首图要在中央区域保持清晰焦点，标题不要贴近上下边缘。
- 尾页不要塞总结；一行时间、地点或照片数量已经足够。

## 自动编排判断

| 素材 | 优先布局 |
|---|---|
| 有 28–100 字真实文字 | `story` |
| 有 8–28 字真实文字 | `photo-note` |
| 一张重要竖图或合照 | `focus` |
| 两张相关照片 | `duo` |
| 一张主图 + 两张细节 | `triptych` |
| 四张同场景碎片 | `grid` |

不要为了填满模板，把没有关系的照片放在同一页。

## 节奏示例

```text
封面
→ focus（建立气氛）
→ duo（动作或人物关系）
→ photo-note（用户原话）
→ triptych（环境 + 细节）
→ focus（重音）
→ grid（生活碎片）
→ story（收束文字）
→ 尾页
```

连续不超过两页同一种密度。每 3–5 页至少出现一次单图停顿。
