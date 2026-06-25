#!/usr/bin/env node

import { execFile } from "node:child_process";
import fs from "node:fs/promises";
import os from "node:os";
import path from "node:path";
import { promisify } from "node:util";
import { pathToFileURL } from "node:url";

const execFileAsync = promisify(execFile);

const PRESETS = {
  xhs: { width: 1080, height: 1440, label: "小红书 3:4", query: "xhs" },
  moments: { width: 1080, height: 1080, label: "微信朋友圈 1:1", query: "moments" },
  portrait: { width: 1080, height: 1440, label: "通用竖版 3:4", query: "portrait" },
};

function usage() {
  console.log(`
把 HTML 画册逐页导出为社交平台图片。

用法：
  node scripts/export_social.mjs album.html --preset xhs
  node scripts/export_social.mjs album.html --preset moments --out social/moments

参数：
  --preset xhs|moments|portrait   导出预设，默认 xhs
  --out DIR                       输出目录，默认 <html名>-<preset>
  --format png|jpg                图片格式，默认 png；JPG 需要 Playwright Core
  --quality 40-100                JPG 质量，默认 92
  --width PX --height PX          自定义尺寸；同时提供时覆盖预设尺寸
  --browser PATH                  指定 Chromium / Chrome / Edge 可执行文件
  --help                          显示帮助
`);
}

function parseArgs(argv) {
  const result = {
    input: null,
    preset: "xhs",
    output: null,
    format: "png",
    quality: 92,
    width: null,
    height: null,
    browser: null,
  };

  for (let index = 0; index < argv.length; index += 1) {
    const value = argv[index];
    if (!value.startsWith("-") && !result.input) {
      result.input = value;
    } else if (value === "--preset") {
      result.preset = argv[++index];
    } else if (value === "--out" || value === "-o") {
      result.output = argv[++index];
    } else if (value === "--format") {
      result.format = argv[++index];
    } else if (value === "--quality") {
      result.quality = Number(argv[++index]);
    } else if (value === "--width") {
      result.width = Number(argv[++index]);
    } else if (value === "--height") {
      result.height = Number(argv[++index]);
    } else if (value === "--browser") {
      result.browser = argv[++index];
    } else if (value === "--help" || value === "-h") {
      usage();
      process.exit(0);
    } else {
      throw new Error(`未知参数：${value}`);
    }
  }
  return result;
}

async function exists(filePath) {
  try {
    await fs.access(filePath);
    return true;
  } catch {
    return false;
  }
}

async function loadPlaywright() {
  for (const packageName of ["playwright-core", "playwright"]) {
    try {
      return await import(packageName);
    } catch {
      // 继续查找 Codex 或用户显式提供的模块路径。
    }
  }

  const candidates = [
    process.env.PLAYWRIGHT_MODULE,
    path.join(
      os.homedir(),
      ".cache",
      "codex-runtimes",
      "codex-primary-runtime",
      "dependencies",
      "node",
      "node_modules",
      "playwright-core",
      "index.mjs",
    ),
    path.join(
      os.homedir(),
      ".cache",
      "codex-runtimes",
      "codex-primary-runtime",
      "dependencies",
      "node",
      "node_modules",
      "playwright",
      "index.mjs",
    ),
  ].filter(Boolean);

  for (const candidate of candidates) {
    if (!(await exists(candidate))) continue;
    try {
      return await import(pathToFileURL(candidate).href);
    } catch {
      // 某些运行时只有不完整的 playwright 包，继续使用浏览器命令行回退。
    }
  }
  return null;
}

async function findBrowser(explicitPath) {
  if (explicitPath) {
    const resolved = path.resolve(explicitPath);
    if (!(await exists(resolved))) throw new Error(`浏览器不存在：${resolved}`);
    return resolved;
  }

  const candidates =
    process.platform === "win32"
      ? [
          "C:\\Program Files (x86)\\Microsoft\\Edge\\Application\\msedge.exe",
          "C:\\Program Files\\Microsoft\\Edge\\Application\\msedge.exe",
          path.join(
            os.homedir(),
            "AppData",
            "Local",
            "Google",
            "Chrome",
            "Application",
            "chrome.exe",
          ),
        ]
      : process.platform === "darwin"
        ? [
            "/Applications/Google Chrome.app/Contents/MacOS/Google Chrome",
            "/Applications/Microsoft Edge.app/Contents/MacOS/Microsoft Edge",
          ]
        : ["/usr/bin/google-chrome", "/usr/bin/chromium", "/usr/bin/chromium-browser"];

  for (const candidate of candidates) {
    if (await exists(candidate)) return candidate;
  }
  return null;
}

function safeLayoutName(value) {
  return (
    (value || "page")
      .toLowerCase()
      .replace(/[^a-z0-9-]+/g, "-")
      .replace(/^-+|-+$/g, "") || "page"
  );
}

function readLayouts(source) {
  const tags = [...source.matchAll(/<section\b([^>]*\bclass="[^"]*\bspread\b[^"]*"[^>]*)>/gi)];
  return tags.map(match => {
    const layout = match[1].match(/\bdata-layout="([^"]+)"/i)?.[1];
    return safeLayoutName(layout);
  });
}

async function exportWithBrowserCli({
  executablePath,
  input,
  output,
  preset,
  width,
  height,
  layouts,
}) {
  const profile = await fs.mkdtemp(path.join(os.tmpdir(), "photo-album-export-"));
  const source = await fs.readFile(input, "utf8");
  const files = [];
  try {
    for (let index = 0; index < layouts.length; index += 1) {
      const filename = `${String(index + 1).padStart(2, "0")}-${layouts[index]}.png`;
      const target = path.join(output, filename);
      const pageHtml = source
        .replace(
          /<html([^>]*)>/i,
          `<html$1 data-export="${preset.query}">`,
        )
        .replace(
          "</head>",
          `<style>
            main#album > .spread{display:none!important}
            main#album > .spread:nth-of-type(${index + 1}){display:flex!important}
          </style></head>`,
        );
      const pagePath = path.join(profile, `page-${index + 1}.html`);
      await fs.writeFile(pagePath, pageHtml, "utf8");
      const url = pathToFileURL(pagePath);
      const browserArgs = [
        "--headless=new",
        "--disable-gpu",
        "--hide-scrollbars",
        "--run-all-compositor-stages-before-draw",
        "--virtual-time-budget=1800",
        `--window-size=${width},${height}`,
        "--force-device-scale-factor=1",
        `--user-data-dir=${profile}`,
        `--screenshot=${target}`,
        url.href,
      ];
      await execFileAsync(executablePath, browserArgs, {
        windowsHide: true,
        timeout: 30000,
        maxBuffer: 1024 * 1024,
      });
      if (!(await exists(target))) throw new Error(`浏览器没有生成图片：${filename}`);
      files.push(filename);
      console.log(`[${String(index + 1).padStart(2, " ")}/${layouts.length}] ${filename}`);
    }
    return files;
  } finally {
    await fs.rm(profile, { recursive: true, force: true });
  }
}

async function exportWithPlaywright({
  playwright,
  executablePath,
  input,
  output,
  preset,
  width,
  height,
  format,
  quality,
}) {
  const launchOptions = { headless: true };
  if (executablePath) launchOptions.executablePath = executablePath;
  const browser = await playwright.chromium.launch(launchOptions);
  try {
    const context = await browser.newContext({
      viewport: { width, height },
      deviceScaleFactor: 1,
      colorScheme: "light",
    });
    const page = await context.newPage();
    const url = pathToFileURL(input);
    url.hash = `export=${preset.query}`;
    await page.goto(url.href, { waitUntil: "load" });
    await page.emulateMedia({ reducedMotion: "reduce", media: "screen" });
    await page.evaluate(async () => {
      document.querySelectorAll("img").forEach(image => {
        image.loading = "eager";
      });
      if (document.fonts?.ready) await document.fonts.ready;
      await Promise.all(
        [...document.images].map(
          image =>
            image.complete ||
            new Promise(resolve => {
              image.addEventListener("load", resolve, { once: true });
              image.addEventListener("error", resolve, { once: true });
            }),
        ),
      );
    });

    const spreads = page.locator(".spread");
    const count = await spreads.count();
    if (!count) throw new Error("HTML 中没有找到 .spread 页面");

    const files = [];
    for (let index = 0; index < count; index += 1) {
      const spread = spreads.nth(index);
      await spread.scrollIntoViewIfNeeded();
      const layout = safeLayoutName(await spread.getAttribute("data-layout"));
      const extension = format === "png" ? "png" : "jpg";
      const filename = `${String(index + 1).padStart(2, "0")}-${layout}.${extension}`;
      const screenshotOptions = {
        path: path.join(output, filename),
        type: format === "png" ? "png" : "jpeg",
        animations: "disabled",
      };
      if (format === "jpg") screenshotOptions.quality = Math.round(quality);
      await spread.screenshot(screenshotOptions);
      files.push(filename);
      console.log(`[${String(index + 1).padStart(2, " ")}/${count}] ${filename}`);
    }
    await context.close();
    return files;
  } finally {
    await browser.close();
  }
}

async function writeManifest({ output, input, presetName, preset, width, height, files }) {
  const orderLines = [
    `${preset.label} · ${width}×${height}`,
    `来源：${path.basename(input)}`,
    "",
    ...files.map((file, index) => `${String(index + 1).padStart(2, "0")}. ${file}`),
    "",
    "按文件名前的两位序号依次上传。",
  ];
  await fs.writeFile(path.join(output, "upload-order.txt"), orderLines.join("\n"), "utf8");
  await fs.writeFile(
    path.join(output, "manifest.json"),
    JSON.stringify(
      {
        preset: presetName,
        label: preset.label,
        width,
        height,
        format: files[0]?.endsWith(".jpg") ? "jpg" : "png",
        source: input,
        pages: files,
      },
      null,
      2,
    ),
    "utf8",
  );
}

async function main() {
  let args;
  try {
    args = parseArgs(process.argv.slice(2));
  } catch (error) {
    console.error(`错误：${error.message}`);
    usage();
    process.exitCode = 2;
    return;
  }

  if (!args.input) {
    usage();
    process.exitCode = 2;
    return;
  }
  if (!PRESETS[args.preset]) throw new Error(`不支持的预设：${args.preset}`);
  if (!["jpg", "png"].includes(args.format)) throw new Error("--format 只支持 jpg 或 png");
  if (!Number.isFinite(args.quality) || args.quality < 40 || args.quality > 100) {
    throw new Error("--quality 需要是 40–100 的数字");
  }

  const input = path.resolve(args.input);
  if (!(await exists(input))) throw new Error(`HTML 不存在：${input}`);

  const preset = PRESETS[args.preset];
  const customSize = Number.isFinite(args.width) && Number.isFinite(args.height);
  const width = customSize ? args.width : preset.width;
  const height = customSize ? args.height : preset.height;
  if (width < 320 || height < 320) throw new Error("导出尺寸不能小于 320×320");

  const parsed = path.parse(input);
  const output = path.resolve(args.output || `${path.join(parsed.dir, parsed.name)}-${args.preset}`);
  await fs.mkdir(output, { recursive: true });

  const source = await fs.readFile(input, "utf8");
  const layouts = readLayouts(source);
  if (!layouts.length) throw new Error("HTML 中没有找到 .spread 页面");

  const executablePath = await findBrowser(args.browser);
  const playwright = await loadPlaywright();
  let files;
  if (playwright) {
    files = await exportWithPlaywright({
      playwright,
      executablePath,
      input,
      output,
      preset,
      width,
      height,
      format: args.format,
      quality: args.quality,
    });
  } else {
    if (args.format !== "png") {
      throw new Error("导出 JPG 需要 `npm install playwright-core`；无需依赖时请使用默认 PNG。");
    }
    if (!executablePath) {
      throw new Error("未找到 Edge、Chrome 或 Chromium；请用 --browser 指定浏览器路径。");
    }
    files = await exportWithBrowserCli({
      executablePath,
      input,
      output,
      preset,
      width,
      height,
      layouts,
    });
  }

  await writeManifest({
    output,
    input,
    presetName: args.preset,
    preset,
    width,
    height,
    files,
  });
  console.log(`\n完成：${output}`);
  console.log(`图片：${files.length} 张 · 尺寸：${width}×${height} · 顺序：upload-order.txt`);
}

main().catch(error => {
  console.error(`错误：${error.message}`);
  process.exitCode = 1;
});
