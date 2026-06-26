#!/usr/bin/env python3
"""Shrink data-URI images inside an existing standalone HTML album."""

from __future__ import annotations

import argparse
import base64
import re
import sys
from dataclasses import dataclass
from io import BytesIO
from pathlib import Path

try:
    from PIL import Image, ImageOps
except ImportError as exc:
    raise SystemExit("错误：compress_standalone.py 需要 Pillow。请先运行：python -m pip install Pillow") from exc


DATA_URI_RE = re.compile(
    r"data:(image/(?:jpeg|jpg|png|webp));base64,([A-Za-z0-9+/=\r\n]+)",
    re.IGNORECASE,
)


@dataclass
class ImageResult:
    index: int
    mime: str
    before_bytes: int
    after_bytes: int
    width: int
    height: int
    replaced: bool
    reason: str = ""


def mb(value: int) -> str:
    return f"{value / 1024 / 1024:.2f} MB"


def default_output(input_path: Path) -> Path:
    return input_path.with_name(f"{input_path.stem}_small{input_path.suffix}")


def optimize_image(
    mime: str,
    payload: str,
    index: int,
    *,
    max_edge: int,
    quality: int,
    keep_larger: bool,
) -> tuple[str, ImageResult]:
    original = base64.b64decode(payload)
    before = len(original)
    with Image.open(BytesIO(original)) as source:
        image = ImageOps.exif_transpose(source)
        image.thumbnail((max_edge, max_edge), Image.Resampling.LANCZOS)
        if image.mode not in {"RGB", "L"}:
            background = Image.new("RGB", image.size, "white")
            if "A" in image.getbands():
                background.paste(image, mask=image.getchannel("A"))
            else:
                background.paste(image)
            image = background
        elif image.mode == "L":
            image = image.convert("RGB")

        buffer = BytesIO()
        image.save(buffer, format="JPEG", quality=quality, optimize=True, progressive=True)
        optimized = buffer.getvalue()
        width, height = image.size

    after = len(optimized)
    if keep_larger and after >= before:
        return (
            f"data:{mime};base64,{payload}",
            ImageResult(index, mime, before, before, width, height, False, "kept original because optimized was larger"),
        )

    return (
        "data:image/jpeg;base64," + base64.b64encode(optimized).decode("ascii"),
        ImageResult(index, mime, before, after, width, height, True),
    )


def compress_html(
    html_text: str,
    *,
    max_edge: int,
    quality: int,
    keep_larger: bool,
) -> tuple[str, list[ImageResult]]:
    results: list[ImageResult] = []
    count = 0

    def replace(match: re.Match[str]) -> str:
        nonlocal count
        count += 1
        replacement, result = optimize_image(
            match.group(1).lower(),
            match.group(2),
            count,
            max_edge=max_edge,
            quality=quality,
            keep_larger=keep_larger,
        )
        results.append(result)
        return replacement

    return DATA_URI_RE.sub(replace, html_text), results


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description="压缩已有单文件 HTML 里内嵌的 base64 图片，输出更适合离线阅读的小文件。",
        formatter_class=argparse.ArgumentDefaultsHelpFormatter,
    )
    parser.add_argument("input", type=Path, help="已有的 standalone HTML")
    parser.add_argument("-o", "--output", type=Path, help="输出 HTML；默认在原文件名后加 _small")
    parser.add_argument("--max-edge", type=int, default=1800, help="图片最长边")
    parser.add_argument("--quality", type=int, default=82, help="输出 JPEG 质量，40-95")
    parser.add_argument(
        "--replace-larger",
        action="store_true",
        help="即使压缩后比原图更大也替换；默认保留更小的原图",
    )
    return parser


def main() -> int:
    args = build_parser().parse_args()
    input_path = args.input.expanduser().resolve()
    if not input_path.is_file():
        print(f"错误：HTML 不存在：{input_path}", file=sys.stderr)
        return 2
    if input_path.suffix.lower() not in {".html", ".htm"}:
        print(f"错误：输入文件需要是 HTML：{input_path}", file=sys.stderr)
        return 2

    quality = max(40, min(args.quality, 95))
    max_edge = max(640, args.max_edge)
    output_path = (args.output or default_output(input_path)).expanduser().resolve()
    if output_path == input_path:
        print("错误：输出路径不能覆盖原 HTML。", file=sys.stderr)
        return 2

    html_text = input_path.read_text(encoding="utf-8", errors="ignore")
    compressed, results = compress_html(
        html_text,
        max_edge=max_edge,
        quality=quality,
        keep_larger=not args.replace_larger,
    )
    if not results:
        print("提示：没有找到 data:image/...;base64 内嵌图片。", file=sys.stderr)

    output_path.parent.mkdir(parents=True, exist_ok=True)
    output_path.write_text(compressed, encoding="utf-8")

    before_size = input_path.stat().st_size
    after_size = output_path.stat().st_size
    print(f"输入：{input_path}")
    print(f"输出：{output_path}")
    print(f"文件：{mb(before_size)} -> {mb(after_size)}")
    print(f"图片：{len(results)} 张")
    for result in results:
        status = "替换" if result.replaced else "保留"
        note = f" · {result.reason}" if result.reason else ""
        print(
            f"[{result.index:02d}] {status} {result.mime} "
            f"{mb(result.before_bytes)} -> {mb(result.after_bytes)} "
            f"({result.width}x{result.height}){note}"
        )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
