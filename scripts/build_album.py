#!/usr/bin/env python3
"""Build a polished, offline HTML photo album from a folder of images."""

from __future__ import annotations

import argparse
import base64
import html
import json
import re
import struct
import sys
from dataclasses import dataclass
from datetime import datetime
from io import BytesIO
from pathlib import Path
from typing import Any

try:
    from PIL import Image, ImageOps

    PIL_AVAILABLE = True
except ImportError:
    PIL_AVAILABLE = False


SUPPORTED = {".jpg", ".jpeg", ".png", ".webp", ".gif"}
UNSUPPORTED_PHONE_FORMATS = {".heic", ".heif"}
MIME_TYPES = {
    ".jpg": "image/jpeg",
    ".jpeg": "image/jpeg",
    ".png": "image/png",
    ".webp": "image/webp",
    ".gif": "image/gif",
}
SOF_MARKERS = {
    0xC0,
    0xC1,
    0xC2,
    0xC3,
    0xC5,
    0xC6,
    0xC7,
    0xC9,
    0xCA,
    0xCB,
    0xCD,
    0xCE,
    0xCF,
}


@dataclass
class Photo:
    path: Path
    relative_name: str
    width: int | None = None
    height: int | None = None
    taken_at: datetime | None = None
    caption: str = ""
    data_uri: str = ""

    @property
    def is_portrait(self) -> bool:
        return bool(self.width and self.height and self.height > self.width * 1.08)

    @property
    def is_landscape(self) -> bool:
        return bool(self.width and self.height and self.width > self.height * 1.16)

    @property
    def alt(self) -> str:
        return self.caption or self.path.stem.replace("_", " ").replace("-", " ")


def natural_key(value: str) -> list[Any]:
    return [int(part) if part.isdigit() else part.casefold() for part in re.split(r"(\d+)", value)]


def parse_datetime(value: Any) -> datetime | None:
    if not value:
        return None
    text = str(value).strip()
    for pattern in ("%Y:%m:%d %H:%M:%S", "%Y-%m-%d %H:%M:%S", "%Y-%m-%d", "%Y/%m/%d"):
        try:
            return datetime.strptime(text, pattern)
        except ValueError:
            continue
    return None


def jpeg_dimensions(path: Path) -> tuple[int | None, int | None]:
    with path.open("rb") as stream:
        if stream.read(2) != b"\xff\xd8":
            return None, None
        while True:
            byte = stream.read(1)
            if not byte:
                return None, None
            if byte != b"\xff":
                continue
            marker = stream.read(1)
            while marker == b"\xff":
                marker = stream.read(1)
            if not marker:
                return None, None
            marker_value = marker[0]
            if marker_value in {0xD8, 0xD9}:
                continue
            length_raw = stream.read(2)
            if len(length_raw) != 2:
                return None, None
            segment_length = struct.unpack(">H", length_raw)[0]
            if segment_length < 2:
                return None, None
            if marker_value in SOF_MARKERS:
                payload = stream.read(5)
                if len(payload) != 5:
                    return None, None
                height, width = struct.unpack(">HH", payload[1:5])
                return width, height
            stream.seek(segment_length - 2, 1)


def webp_dimensions(data: bytes) -> tuple[int | None, int | None]:
    if len(data) < 30 or data[:4] != b"RIFF" or data[8:12] != b"WEBP":
        return None, None
    chunk = data[12:16]
    if chunk == b"VP8X":
        width = 1 + int.from_bytes(data[24:27], "little")
        height = 1 + int.from_bytes(data[27:30], "little")
        return width, height
    if chunk == b"VP8L" and len(data) >= 25 and data[20] == 0x2F:
        bits = int.from_bytes(data[21:25], "little")
        return (bits & 0x3FFF) + 1, ((bits >> 14) & 0x3FFF) + 1
    if chunk == b"VP8 ":
        marker = data.find(b"\x9d\x01\x2a", 20, 40)
        if marker >= 0 and len(data) >= marker + 7:
            width, height = struct.unpack("<HH", data[marker + 3 : marker + 7])
            return width & 0x3FFF, height & 0x3FFF
    return None, None


def basic_dimensions(path: Path) -> tuple[int | None, int | None]:
    suffix = path.suffix.lower()
    try:
        if suffix in {".jpg", ".jpeg"}:
            return jpeg_dimensions(path)
        data = path.read_bytes()[:64]
        if suffix == ".png" and data[:8] == b"\x89PNG\r\n\x1a\n":
            return struct.unpack(">II", data[16:24])
        if suffix == ".gif" and data[:6] in {b"GIF87a", b"GIF89a"}:
            return struct.unpack("<HH", data[6:10])
        if suffix == ".webp":
            return webp_dimensions(path.read_bytes()[:80])
    except (OSError, struct.error):
        pass
    return None, None


def inspect_photo(path: Path, source: Path) -> Photo:
    width: int | None = None
    height: int | None = None
    taken_at: datetime | None = None

    if PIL_AVAILABLE:
        try:
            with Image.open(path) as image:
                width, height = image.size
                exif = image.getexif()
                taken_at = parse_datetime(exif.get(36867) or exif.get(36868) or exif.get(306))
                orientation = exif.get(274)
                if orientation in {5, 6, 7, 8}:
                    width, height = height, width
        except Exception:
            width, height = basic_dimensions(path)
    else:
        width, height = basic_dimensions(path)

    return Photo(
        path=path,
        relative_name=path.relative_to(source).as_posix(),
        width=width,
        height=height,
        taken_at=taken_at,
    )


def discover_images(source: Path, recursive: bool) -> tuple[list[Path], list[Path]]:
    iterator = source.rglob("*") if recursive else source.iterdir()
    supported: list[Path] = []
    unsupported: list[Path] = []
    for path in iterator:
        if not path.is_file():
            continue
        suffix = path.suffix.lower()
        if suffix in SUPPORTED:
            supported.append(path)
        elif suffix in UNSUPPORTED_PHONE_FORMATS:
            unsupported.append(path)
    return supported, unsupported


def read_config(source: Path, config_path: Path | None) -> dict[str, Any]:
    candidate = config_path or (source / "album.json")
    if not candidate.exists():
        return {}
    try:
        data = json.loads(candidate.read_text(encoding="utf-8-sig"))
    except (OSError, json.JSONDecodeError) as exc:
        raise SystemExit(f"无法读取配置文件 {candidate}: {exc}") from exc
    if not isinstance(data, dict):
        raise SystemExit(f"配置文件必须是 JSON 对象: {candidate}")
    return data


def apply_config(photos: list[Photo], config: dict[str, Any]) -> list[Photo]:
    captions = config.get("captions", {})
    if isinstance(captions, dict):
        normalized = {str(key).replace("\\", "/"): str(value) for key, value in captions.items()}
        for photo in photos:
            photo.caption = normalized.get(photo.relative_name, normalized.get(photo.path.name, ""))

    order = config.get("order")
    if isinstance(order, list) and order:
        rank = {str(name).replace("\\", "/"): index for index, name in enumerate(order)}
        photos.sort(
            key=lambda photo: (
                rank.get(photo.relative_name, rank.get(photo.path.name, len(rank))),
                natural_key(photo.relative_name),
            )
        )
    return photos


def sort_photos(photos: list[Photo], method: str) -> list[Photo]:
    if method == "name":
        return sorted(photos, key=lambda photo: natural_key(photo.relative_name))
    if method == "time":
        return sorted(
            photos,
            key=lambda photo: (
                photo.taken_at or datetime.fromtimestamp(photo.path.stat().st_mtime),
                natural_key(photo.relative_name),
            ),
        )
    if photos and all(photo.taken_at for photo in photos):
        return sorted(photos, key=lambda photo: (photo.taken_at, natural_key(photo.relative_name)))
    return sorted(photos, key=lambda photo: natural_key(photo.relative_name))


def evenly_select(photos: list[Photo], limit: int) -> list[Photo]:
    if limit <= 0 or len(photos) <= limit:
        return photos
    if limit == 1:
        return [photos[0]]
    indexes = [round(index * (len(photos) - 1) / (limit - 1)) for index in range(limit)]
    return [photos[index] for index in dict.fromkeys(indexes)]


def encode_original(photo: Photo) -> str:
    mime = MIME_TYPES[photo.path.suffix.lower()]
    payload = base64.b64encode(photo.path.read_bytes()).decode("ascii")
    return f"data:{mime};base64,{payload}"


def encode_optimized(photo: Photo, max_edge: int, quality: int) -> str:
    if not PIL_AVAILABLE or photo.path.suffix.lower() == ".gif":
        return encode_original(photo)

    try:
        with Image.open(photo.path) as source:
            image = ImageOps.exif_transpose(source)
            image.thumbnail((max_edge, max_edge))
            buffer = BytesIO()
            suffix = photo.path.suffix.lower()

            if suffix == ".png":
                image.save(buffer, format="PNG", optimize=True)
                mime = "image/png"
            elif suffix == ".webp":
                image.save(buffer, format="WEBP", quality=quality, method=6)
                mime = "image/webp"
            else:
                if image.mode not in {"RGB", "L"}:
                    background = Image.new("RGB", image.size, "white")
                    if "A" in image.getbands():
                        background.paste(image, mask=image.getchannel("A"))
                    else:
                        background.paste(image)
                    image = background
                elif image.mode == "L":
                    image = image.convert("RGB")
                image.save(buffer, format="JPEG", quality=quality, optimize=True, progressive=True)
                mime = "image/jpeg"

            photo.width, photo.height = image.size
            payload = base64.b64encode(buffer.getvalue()).decode("ascii")
            return f"data:{mime};base64,{payload}"
    except Exception as exc:
        print(f"警告：压缩失败，使用原图 {photo.path.name}: {exc}", file=sys.stderr)
        return encode_original(photo)


def esc(value: Any) -> str:
    return html.escape(str(value), quote=True)


def image_tag(photo: Photo, extra_class: str = "") -> str:
    classes = "photo" + (f" {extra_class}" if extra_class else "")
    return f'<img class="{classes}" src="{photo.data_uri}" alt="{esc(photo.alt)}">'


def page_kicker(page_number: int, label: str = "") -> str:
    suffix = f" · {esc(label)}" if label else ""
    return f'<p class="kicker" data-anim>{page_number:02d}{suffix}</p>'


def caption_block(photo: Photo) -> str:
    if not photo.caption:
        return ""
    return f'<p class="caption" data-anim>{esc(photo.caption)}</p>'


def cover_page(photo: Photo, title: str, subtitle: str) -> str:
    return f"""
<section class="spread hero dark" data-layout="cover">
  {image_tag(photo, "hero-img")}
  <div class="cover">
    <p class="meta" data-anim>PHOTO ALBUM</p>
    <h1 class="h-hero" data-anim>{esc(title)}</h1>
    <p class="lead" data-anim>{esc(subtitle)}</p>
  </div>
</section>"""


def focus_page(photo: Photo, page_number: int) -> str:
    return f"""
<section class="spread dark focus-page" data-layout="focus">
  <div class="focus-haze" aria-hidden="true"></div>
  {page_kicker(page_number)}
  <div class="focus-shell">{image_tag(photo)}</div>
  {caption_block(photo)}
</section>"""


def story_page(photo: Photo, page_number: int, reverse: bool) -> str:
    direction = " reverse" if reverse else ""
    return f"""
<section class="spread" data-layout="story">
  <div class="story{direction}">
    <div class="story-copy">
      {page_kicker(page_number, "记一笔")}
      <div class="rule" data-anim></div>
      <p class="lead" data-anim>{esc(photo.caption)}</p>
    </div>
    <div class="photo-card">{image_tag(photo)}</div>
  </div>
</section>"""


def photo_note_page(photo: Photo, page_number: int, reverse: bool) -> str:
    direction = " reverse" if reverse else ""
    return f"""
<section class="spread" data-layout="photo-note">
  <div class="photo-note{direction}">
    <div class="photo-card">{image_tag(photo)}</div>
    <div class="photo-note-copy">
      {page_kicker(page_number, "旁注")}
      <p class="lead" data-anim>{esc(photo.caption)}</p>
    </div>
  </div>
</section>"""


def duo_page(photos: list[Photo], page_number: int) -> str:
    cards = "\n".join(f'    <div class="photo-card">{image_tag(photo)}</div>' for photo in photos)
    if len(photos) == 2 and all(photo.is_portrait for photo in photos):
        variant = " portrait-pair"
    elif len(photos) == 2 and photos[0].is_landscape != photos[1].is_landscape:
        variant = " mixed"
    else:
        variant = " equal"
    return f"""
<section class="spread" data-layout="duo">
  {page_kicker(page_number)}
  <div class="duo{variant}">
{cards}
  </div>
</section>"""


def triptych_page(photos: list[Photo], page_number: int) -> str:
    cards = "\n".join(f'    <div class="photo-card">{image_tag(photo)}</div>' for photo in photos)
    variant = " top-lead" if photos[0].is_landscape else ""
    return f"""
<section class="spread" data-layout="triptych">
  {page_kicker(page_number)}
  <div class="triptych{variant}">
{cards}
  </div>
</section>"""


def grid_page(photos: list[Photo], page_number: int) -> str:
    cards = "\n".join(f'    <div class="photo-card">{image_tag(photo)}</div>' for photo in photos)
    return f"""
<section class="spread" data-layout="grid">
  {page_kicker(page_number)}
  <div class="grid-2x2">
{cards}
  </div>
</section>"""


def end_page(title: str, count: int) -> str:
    return f"""
<section class="spread end-page" data-layout="end">
  <div class="end-mark" data-anim>·</div>
  <p class="meta" data-anim>{esc(title)}</p>
  <h2 class="h-xl" data-anim>共 {count} 张照片</h2>
  <p class="body-zh" data-anim>照片已经收进这一册。</p>
</section>"""


def choose_cover(photos: list[Photo], configured_cover: Any) -> Photo:
    if configured_cover:
        target = str(configured_cover).replace("\\", "/")
        for photo in photos:
            if photo.relative_name == target or photo.path.name == target:
                return photo
    for photo in photos[:12]:
        if photo.width and photo.height and photo.width >= photo.height * 1.18:
            return photo
    return photos[0]


def build_spreads(
    photos: list[Photo],
    title: str,
    subtitle: str,
    config: dict[str, Any],
    composition: str,
) -> str:
    cover = choose_cover(photos, config.get("cover"))
    remaining = [photo for photo in photos if photo is not cover]
    pages = [cover_page(cover, title, subtitle)]
    page_number = 2
    pattern_index = 0
    patterns_by_composition = {
        "auto": ("duo", "focus", "triptych", "grid", "focus"),
        "editorial": ("focus", "duo", "focus", "triptych"),
        "gallery": ("duo", "triptych", "grid", "focus"),
    }
    patterns = patterns_by_composition[composition]

    while remaining:
        if remaining[0].caption and len(remaining[0].caption) >= 28:
            photo = remaining.pop(0)
            pages.append(story_page(photo, page_number, reverse=page_number % 2 == 0))
        elif remaining[0].caption:
            photo = remaining.pop(0)
            pages.append(photo_note_page(photo, page_number, reverse=page_number % 2 == 1))
        else:
            pattern = patterns[pattern_index % len(patterns)]
            pattern_index += 1
            if len(remaining) == 1 or pattern == "focus":
                pages.append(focus_page(remaining.pop(0), page_number))
            elif pattern == "grid" and len(remaining) >= 4 and not any(photo.caption for photo in remaining[:4]):
                pages.append(grid_page(remaining[:4], page_number))
                del remaining[:4]
            elif pattern == "triptych" and len(remaining) >= 3 and not any(
                photo.caption for photo in remaining[:3]
            ):
                pages.append(triptych_page(remaining[:3], page_number))
                del remaining[:3]
            else:
                take = min(2, len(remaining))
                pages.append(duo_page(remaining[:take], page_number))
                del remaining[:take]
        page_number += 1

    pages.append(end_page(title, len(photos)))
    return "\n".join(pages)


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description="把照片目录生成为可离线翻阅的单文件 HTML 画册。",
        formatter_class=argparse.ArgumentDefaultsHelpFormatter,
    )
    parser.add_argument("source", type=Path, help="照片目录")
    parser.add_argument("-o", "--output", type=Path, default=Path("album.html"), help="输出 HTML")
    parser.add_argument("--title", help="画册标题；默认使用目录名")
    parser.add_argument("--subtitle", help="封面副标题；默认显示照片数量")
    parser.add_argument("--theme", choices=("warm", "silver", "night"), default=None, help="初始主题")
    parser.add_argument(
        "--composition",
        choices=("auto", "editorial", "gallery"),
        default=None,
        help="页面编排倾向：自动、图文编辑或图片排列",
    )
    parser.add_argument("--sort", choices=("auto", "time", "name"), default="auto", help="照片顺序")
    parser.add_argument("--recursive", action="store_true", help="递归扫描子目录")
    parser.add_argument("--max-photos", type=int, default=80, help="最多使用的照片数；0 表示全部")
    parser.add_argument("--config", type=Path, help="可选 album.json 路径")
    parser.add_argument("--template", type=Path, help="自定义模板路径")
    parser.add_argument("--max-edge", type=int, default=2200, help="安装 Pillow 时的图片最长边")
    parser.add_argument("--quality", type=int, default=86, help="安装 Pillow 时的 JPEG/WEBP 质量")
    parser.add_argument("--no-optimize", action="store_true", help="即使安装 Pillow 也不压缩图片")
    return parser


def main() -> int:
    args = build_parser().parse_args()
    source = args.source.expanduser().resolve()
    if not source.is_dir():
        print(f"错误：照片目录不存在：{source}", file=sys.stderr)
        return 2

    paths, unsupported = discover_images(source, args.recursive)
    if unsupported:
        names = "、".join(path.name for path in unsupported[:5])
        more = "…" if len(unsupported) > 5 else ""
        print(f"提示：跳过浏览器不直接支持的 HEIC/HEIF：{names}{more}", file=sys.stderr)
    if not paths:
        print(f"错误：目录中没有支持的图片：{source}", file=sys.stderr)
        return 2

    config = read_config(source, args.config.expanduser().resolve() if args.config else None)
    photos = [inspect_photo(path, source) for path in paths]
    photos = sort_photos(photos, args.sort)
    photos = apply_config(photos, config)

    original_count = len(photos)
    photos = evenly_select(photos, args.max_photos)
    if len(photos) < original_count:
        print(f"提示：从 {original_count} 张照片中均匀选取 {len(photos)} 张。", file=sys.stderr)

    optimize = PIL_AVAILABLE and not args.no_optimize
    if not PIL_AVAILABLE and not args.no_optimize:
        print("提示：未安装 Pillow，将内嵌原图；安装 Pillow 后可自动旋转并压缩大图。", file=sys.stderr)

    for index, photo in enumerate(photos, start=1):
        print(f"[{index:>3}/{len(photos)}] {photo.relative_name}")
        photo.data_uri = (
            encode_optimized(photo, max(640, args.max_edge), max(40, min(args.quality, 95)))
            if optimize
            else encode_original(photo)
        )

    title = args.title or config.get("title") or source.name.replace("_", " ").replace("-", " ")
    subtitle = args.subtitle or config.get("subtitle") or f"{len(photos)} 张照片"
    theme = args.theme or config.get("theme") or "warm"
    if theme not in {"warm", "silver", "night"}:
        theme = "warm"
    composition = args.composition or config.get("composition") or "auto"
    if composition not in {"auto", "editorial", "gallery"}:
        composition = "auto"

    template_path = args.template or (Path(__file__).resolve().parents[1] / "assets" / "template.html")
    try:
        template = template_path.read_text(encoding="utf-8")
    except OSError as exc:
        print(f"错误：无法读取模板 {template_path}: {exc}", file=sys.stderr)
        return 2
    if "<!-- SPREADS_HERE -->" not in template:
        print("错误：模板缺少 <!-- SPREADS_HERE --> 插入标记。", file=sys.stderr)
        return 2

    output = args.output.expanduser().resolve()
    output.parent.mkdir(parents=True, exist_ok=True)
    rendered = template.replace("[画册标题]", esc(title))
    rendered = rendered.replace('body data-theme="warm"', f'body data-theme="{theme}"', 1)
    rendered = rendered.replace(
        "<!-- SPREADS_HERE -->",
        build_spreads(photos, title, subtitle, config, composition),
    )
    output.write_text(rendered, encoding="utf-8")

    size_mb = output.stat().st_size / (1024 * 1024)
    print(f"\n完成：{output}")
    print(f"页面：{rendered.count('<section class=\"spread')} · 照片：{len(photos)} · 文件：{size_mb:.1f} MB")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
