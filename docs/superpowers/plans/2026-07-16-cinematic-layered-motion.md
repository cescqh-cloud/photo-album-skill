# Cinematic Layered Motion Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Add a continuous, performance-conscious layered motion system to generated photo albums, regenerate the private Jinjihe album with it, and publish the reusable Skill changes to GitHub.

**Architecture:** Keep page markup and generator interfaces unchanged. Implement motion as a template-level state machine that assigns five spatial page states, funnels every navigation source through one queued transition controller, and exposes pointer depth through CSS variables. CSS handles transforms and reduced-motion/export/print fallbacks; JavaScript owns page state, merged navigation requests, lightbox suspension, and progress updates.

**Tech Stack:** Standalone HTML, CSS transforms and custom properties, vanilla JavaScript, Python `unittest`, PowerShell verification, Git.

---

## File Map

- Modify `assets/template.html`: layered page states, motion CSS, navigation state machine, pointer depth, touch handling, reduced-motion and export/print fallbacks.
- Modify `tests/test_build_album.py`: template contract tests and generated-album regression assertions.
- Modify `README.md`: user-facing motion behavior and compatibility notes.
- Modify `SKILL.md`: agent workflow and acceptance rules for cinematic motion.
- Modify `references/design-principles.md`: motion restraint and accessibility rules.
- Use `scripts/build_album.py` unchanged to regenerate the Jinjihe deliverable.
- Create outside the repository: `C:\Users\cescq\Documents\Codex\2026-07-06\wo-d\outputs\jinjihe-2026-07-11-cinematic.html`.

### Task 1: Lock The Template Motion Contract

**Files:**
- Modify: `tests/test_build_album.py`
- Test: `tests/test_build_album.py`

- [ ] **Step 1: Add template loading and failing structural tests**

Add this near the module setup:

```python
TEMPLATE = (ROOT / "assets" / "template.html").read_text(encoding="utf-8")
```

Add the following test class:

```python
class CinematicMotionTemplateTests(unittest.TestCase):
    def test_template_declares_layered_motion_states(self) -> None:
        self.assertIn('data-motion="layered"', TEMPLATE)
        for state in ("is-before", "is-prev", "is-current", "is-next", "is-after"):
            self.assertIn(state, TEMPLATE)

    def test_template_merges_navigation_requests(self) -> None:
        self.assertIn("pendingTarget", TEMPLATE)
        self.assertIn("transitionTo", TEMPLATE)
        self.assertIn("finishTransition", TEMPLATE)

    def test_template_supports_depth_and_accessible_fallbacks(self) -> None:
        self.assertIn("--pointer-x", TEMPLATE)
        self.assertIn("requestAnimationFrame", TEMPLATE)
        self.assertIn("prefers-reduced-motion:reduce", TEMPLATE)
        self.assertIn('html[data-export]', TEMPLATE)
        self.assertIn("@media print", TEMPLATE)
```

- [ ] **Step 2: Run the tests and verify the new contract fails**

Run:

```powershell
$env:PYTHONUTF8='1'
python -m unittest discover -s tests -v
```

Expected: existing six tests pass; at least `data-motion="layered"`, `pendingTarget`, and `--pointer-x` assertions fail.

- [ ] **Step 3: Commit the failing tests**

```powershell
git add tests/test_build_album.py
git commit -m "test: define cinematic album motion contract"
```

### Task 2: Implement Layered CSS States

**Files:**
- Modify: `assets/template.html`
- Test: `tests/test_build_album.py`

- [ ] **Step 1: Mark the document with the default motion mode**

Change the root element to:

```html
<html lang="zh-CN" data-motion="layered">
```

- [ ] **Step 2: Replace the one-shot image-settle rules with spatial state rules**

Add root variables and a fixed album stage:

```css
html{
  --pointer-x:0;
  --pointer-y:0;
  --motion-direction:1;
  --motion-duration:820ms;
}
html.js:not([data-export]) body{height:100svh;overflow:hidden}
html.js:not([data-export]) #album{
  position:relative;
  width:100%;
  height:100svh;
  perspective:1200px;
  transform-style:preserve-3d;
  overflow:hidden;
}
html.js:not([data-export]) .spread{
  position:absolute;
  inset:0;
  min-height:100svh;
  opacity:0;
  visibility:hidden;
  pointer-events:none;
  transform-origin:50% 50%;
  transition:
    transform var(--motion-duration) cubic-bezier(.62,0,.18,1),
    opacity calc(var(--motion-duration) * .72) ease,
    visibility 0s linear var(--motion-duration);
}
```

Define deterministic layers:

```css
html.js:not([data-export]) .spread.is-before{transform:translate3d(-7vw,0,180px) rotateY(2deg)}
html.js:not([data-export]) .spread.is-prev{transform:translate3d(-3vw,0,90px) rotateY(1deg)}
html.js:not([data-export]) .spread.is-current{
  z-index:3;
  opacity:1;
  visibility:visible;
  pointer-events:auto;
  transform:translate3d(0,0,0);
  transition-delay:0s;
}
html.js:not([data-export]) .spread.is-next{transform:translate3d(3vw,0,-120px) rotateY(-1deg)}
html.js:not([data-export]) .spread.is-after{transform:translate3d(7vw,0,-220px) rotateY(-2deg)}
html.js:not([data-export]) .spread.is-prev,
html.js:not([data-export]) .spread.is-next{
  visibility:visible;
  z-index:2;
}
```

- [ ] **Step 3: Add restrained depth and breathing motion**

Use a nested-content selector so existing layout transforms are not overwritten:

```css
html.js:not([data-export]) .is-current > :not(.page-num){
  transform:translate3d(
    calc(var(--pointer-x) * 5px),
    calc(var(--pointer-y) * 4px),
    0
  );
}
html.js:not([data-export]) .is-current .photo{
  animation:cinematic-breathe 16s ease-in-out infinite alternate;
}
html.js:not([data-export]) .is-current .photo.fit-contain{animation-name:cinematic-breathe-contain}
@keyframes cinematic-breathe{
  from{transform:scale(1.006)}
  to{transform:scale(1.018)}
}
@keyframes cinematic-breathe-contain{
  from{transform:translate3d(0,0,0) scale(1)}
  to{transform:translate3d(0,-.35%,0) scale(1.006)}
}
```

- [ ] **Step 4: Add mobile, reduced-motion, export, and print overrides**

```css
@media (max-width:720px){
  html{--motion-duration:680ms}
  html.js:not([data-export]) .spread.is-before{transform:translate3d(-3vw,0,80px)}
  html.js:not([data-export]) .spread.is-after{transform:translate3d(3vw,0,-110px)}
  html.js:not([data-export]) .is-current > :not(.page-num){transform:none}
}
@media (prefers-reduced-motion:reduce){
  html.js:not([data-export]) .spread{
    transform:none!important;
    transition:opacity 160ms linear!important;
  }
  html.js:not([data-export]) .is-current .photo{animation:none!important}
}
html[data-export] .spread,
html[data-export] .spread *{animation:none!important;transform:none!important}
@media print{
  .spread,.spread *{animation:none!important;transform:none!important;visibility:visible!important;opacity:1!important}
}
```

- [ ] **Step 5: Run the template tests**

Run:

```powershell
$env:PYTHONUTF8='1'
python -m unittest discover -s tests -v
```

Expected: state and fallback assertions pass; navigation contract may still fail until Task 3.

- [ ] **Step 6: Commit CSS motion states**

```powershell
git add assets/template.html
git commit -m "feat: add layered cinematic album states"
```

### Task 3: Implement Unified Navigation And Pointer Depth

**Files:**
- Modify: `assets/template.html`
- Test: `tests/test_build_album.py`

- [ ] **Step 1: Replace `update` and `go` with a spatial state renderer**

Implement these functions inside the template script:

```javascript
const reducedMotion = matchMedia("(prefers-reduced-motion: reduce)");
const transitionMs = reducedMotion.matches ? 170 : 820;
let current = 0;
let pendingTarget = null;
let transitionTimer = 0;
let isTransitioning = false;

const pageState = (index, active) => {
  if (index < active - 1) return "is-before";
  if (index === active - 1) return "is-prev";
  if (index === active) return "is-current";
  if (index === active + 1) return "is-next";
  return "is-after";
};

const renderState = active => {
  spreads.forEach((spread, index) => {
    spread.classList.remove("is-before", "is-prev", "is-current", "is-next", "is-after");
    spread.classList.add(pageState(index, active));
    spread.setAttribute("aria-hidden", String(index !== active));
  });
  indicator.textContent = `${active + 1} / ${spreads.length}`;
  progressBar.style.width = `${((active + 1) / spreads.length) * 100}%`;
};
```

- [ ] **Step 2: Add merged transition requests**

```javascript
const finishTransition = () => {
  clearTimeout(transitionTimer);
  isTransitioning = false;
  if (pendingTarget !== null && pendingTarget !== current) {
    const target = pendingTarget;
    pendingTarget = null;
    transitionTo(target);
  }
};

const transitionTo = index => {
  const target = Math.max(0, Math.min(index, spreads.length - 1));
  if (lightbox.classList.contains("is-open") || target === current) return;
  if (isTransitioning) {
    pendingTarget = target;
    return;
  }
  isTransitioning = true;
  document.documentElement.style.setProperty("--motion-direction", target > current ? "1" : "-1");
  current = target;
  renderState(current);
  transitionTimer = window.setTimeout(finishTransition, transitionMs);
};

const go = index => transitionTo(index);
```

Remove the `IntersectionObserver` because the album is now a fixed spatial stage rather than a scroll container.

- [ ] **Step 3: Add touch navigation**

```javascript
let touchStartX = 0;
let touchStartY = 0;
album.addEventListener("touchstart", event => {
  const touch = event.changedTouches[0];
  touchStartX = touch.clientX;
  touchStartY = touch.clientY;
}, {passive:true});
album.addEventListener("touchend", event => {
  if (lightbox.classList.contains("is-open")) return;
  const touch = event.changedTouches[0];
  const dx = touch.clientX - touchStartX;
  const dy = touch.clientY - touchStartY;
  if (Math.abs(dx) < 44 || Math.abs(dx) < Math.abs(dy)) return;
  go(current + (dx < 0 ? 1 : -1));
}, {passive:true});
```

- [ ] **Step 4: Add requestAnimationFrame pointer depth**

```javascript
let pointerFrame = 0;
const setPointerDepth = event => {
  if (reducedMotion.matches || matchMedia("(pointer: coarse)").matches || lightbox.classList.contains("is-open")) return;
  const x = event.clientX / innerWidth * 2 - 1;
  const y = event.clientY / innerHeight * 2 - 1;
  cancelAnimationFrame(pointerFrame);
  pointerFrame = requestAnimationFrame(() => {
    document.documentElement.style.setProperty("--pointer-x", x.toFixed(3));
    document.documentElement.style.setProperty("--pointer-y", y.toFixed(3));
  });
};
window.addEventListener("pointermove", setPointerDepth, {passive:true});
document.documentElement.addEventListener("mouseleave", () => {
  document.documentElement.style.setProperty("--pointer-x", "0");
  document.documentElement.style.setProperty("--pointer-y", "0");
});
```

- [ ] **Step 5: Integrate lightbox and initialization**

When opening the lightbox, reset pointer variables. In `closeLightbox`, leave `current` unchanged. Initialize with:

```javascript
current = Math.max(0, Math.min(exportPage > 0 ? exportPage - 1 : 0, spreads.length - 1));
renderState(current);
```

- [ ] **Step 6: Run all unit tests**

```powershell
$env:PYTHONUTF8='1'
python -m unittest discover -s tests -v
```

Expected: all tests pass.

- [ ] **Step 7: Commit navigation and depth behavior**

```powershell
git add assets/template.html tests/test_build_album.py
git commit -m "feat: add cinematic navigation and pointer depth"
```

### Task 4: Document The Motion Behavior

**Files:**
- Modify: `README.md`
- Modify: `SKILL.md`
- Modify: `references/design-principles.md`

- [ ] **Step 1: Update README feature and usage descriptions**

Add a project-highlight bullet explaining continuous layered motion, offline operation, reduced-motion support, and mobile performance. Update the generator behavior list to mention unified keyboard/button/touch navigation.

- [ ] **Step 2: Update Skill generation and acceptance rules**

In `SKILL.md`, document that generated albums default to `data-motion="layered"`, that motion must remain subordinate to photography, and that browser acceptance includes rapid input and reduced-motion checks.

- [ ] **Step 3: Add motion restraint rules to design principles**

Add a section requiring a shared motion system, transform/opacity-only animation, restrained breathing, no persistent blur or particles, and mandatory reduced-motion behavior.

- [ ] **Step 4: Check documentation for contradictions**

```powershell
rg -n "PPT|动效|动画|翻页|reduced|data-motion" README.md SKILL.md references/design-principles.md
```

Expected: new motion language is present and no statement says pages only use a one-shot entrance animation.

- [ ] **Step 5: Commit documentation**

```powershell
git add README.md SKILL.md references/design-principles.md
git commit -m "docs: describe cinematic album motion"
```

### Task 5: Regenerate And Verify Jinjihe

**Files:**
- Read: `C:\Users\cescq\Documents\Codex\2026-07-06\wo-d\work\jinjihe-selected\album.json`
- Create: `C:\Users\cescq\Documents\Codex\2026-07-06\wo-d\outputs\jinjihe-2026-07-11-cinematic.html`
- Test: `tests/test_build_album.py`

- [ ] **Step 1: Generate the cinematic album with the repository version**

```powershell
$env:PYTHONUTF8='1'
python scripts/build_album.py `
  'C:\Users\cescq\Documents\Codex\2026-07-06\wo-d\work\jinjihe-selected' `
  -o 'C:\Users\cescq\Documents\Codex\2026-07-06\wo-d\outputs\jinjihe-2026-07-11-cinematic.html' `
  --theme night --composition editorial --profile balanced --sort name
```

Expected: 22 pages, 33 photos, approximately 6.2 MB.

- [ ] **Step 2: Run static integrity checks**

Verify the generated file contains:

```powershell
$html = Get-Content -Raw -Encoding UTF8 'C:\Users\cescq\Documents\Codex\2026-07-06\wo-d\outputs\jinjihe-2026-07-11-cinematic.html'
@{
  Pages = ([regex]::Matches($html, '<section class="spread')).Count
  Photos = ([regex]::Matches($html, 'src="data:image/')).Count
  Layered = $html.Contains('data-motion="layered"')
  Pending = $html.Contains('pendingTarget')
  BrokenUtf8 = ([regex]::Matches($html, [char]0xfffd)).Count
}
```

Expected: `Pages=22`, `Photos=33`, `Layered=True`, `Pending=True`, `BrokenUtf8=0`.

- [ ] **Step 3: Serve the output locally and perform browser acceptance**

Use a local HTTP server because automated browsers block `file://` URLs:

```powershell
python -m http.server 8765 --directory 'C:\Users\cescq\Documents\Codex\2026-07-06\wo-d\outputs'
```

Check desktop and 390 px viewport: cover, lake-to-blue-hour transition, Milky Way climax, final page, rapid next/previous input, lightbox, theme, touch emulation, and reduced-motion behavior. Confirm no horizontal overflow, blank canvas, clipped `fit-contain` images, or console errors.

- [ ] **Step 4: Run full Skill verification**

```powershell
$env:PYTHONUTF8='1'
python -m unittest discover -s tests -v
python -m py_compile scripts/build_album.py scripts/compress_standalone.py
python 'C:\Users\cescq\.codex\skills\.system\skill-creator\scripts\quick_validate.py' .
git diff --check
git status --short
```

Expected: all tests pass, compile succeeds, Skill is valid, diff check is clean, and only intended files are changed.

- [ ] **Step 5: Push the reviewed commits to GitHub**

```powershell
git log --oneline origin/master..master
git push origin master
git ls-remote origin refs/heads/master
```

Expected: the remote `master` hash matches the local `HEAD`. Do not add the Jinjihe source directory or cinematic HTML to the repository.
