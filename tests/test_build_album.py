from __future__ import annotations

import importlib.util
import sys
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
SPEC = importlib.util.spec_from_file_location("build_album", ROOT / "scripts" / "build_album.py")
assert SPEC and SPEC.loader
build_album = importlib.util.module_from_spec(SPEC)
sys.modules[SPEC.name] = build_album
SPEC.loader.exec_module(build_album)
TEMPLATE = (ROOT / "assets" / "template.html").read_text(encoding="utf-8")


def make_photo(
    name: str,
    *,
    width: int = 1600,
    height: int = 1000,
    caption: str = "",
) -> build_album.Photo:
    return build_album.Photo(
        path=Path(name),
        relative_name=name,
        width=width,
        height=height,
        caption=caption,
        data_uri="data:image/jpeg;base64,AAA",
    )


class ImageMarkupTests(unittest.TestCase):
    def test_image_tag_defaults_to_safe_contain_with_dimensions(self) -> None:
        photo = make_photo("portrait.jpg", width=1000, height=1800)

        markup = build_album.image_tag(photo)

        self.assertIn("fit-contain", markup)
        self.assertIn("aspect-portrait", markup)
        self.assertIn('width="1000"', markup)
        self.assertIn('height="1800"', markup)
        self.assertNotIn('loading="lazy"', markup)
        self.assertNotIn("fit-cover", markup)

    def test_cover_image_is_eager_and_cover_fitted(self) -> None:
        photo = make_photo("cover.jpg", width=2400, height=1400)

        markup = build_album.cover_page(photo, "天湖", "云海")

        self.assertIn("hero-img", markup)
        self.assertIn("fit-cover", markup)
        self.assertIn('loading="eager"', markup)
        self.assertIn('fetchpriority="high"', markup)


class ImageSettingsTests(unittest.TestCase):
    def test_balanced_profile_uses_smaller_default_images(self) -> None:
        max_edge, quality = build_album.resolve_image_settings("balanced", None, None)

        self.assertEqual(max_edge, 1600)
        self.assertEqual(quality, 80)

    def test_explicit_image_settings_override_profile(self) -> None:
        max_edge, quality = build_album.resolve_image_settings("fast", 2200, 90)

        self.assertEqual(max_edge, 2200)
        self.assertEqual(quality, 90)


class LayoutSelectionTests(unittest.TestCase):
    def test_panoramic_photo_gets_panorama_layout(self) -> None:
        photos = [
            make_photo("cover.jpg", width=1800, height=1200),
            make_photo("pano.jpg", width=2600, height=900),
        ]

        spreads = build_album.build_spreads(photos, "天湖", "2 张照片", {}, "auto")

        self.assertIn('data-layout="panorama"', spreads)

    def test_long_captioned_landscapes_do_not_all_become_story_pages(self) -> None:
        caption = "云从山谷里翻上来，刚才还看不清的山脊忽然露出一点线条，于是决定再等一会儿。"
        photos = [make_photo("cover.jpg", width=1800, height=1200)]
        photos.extend(
            make_photo(f"landscape-{index}.jpg", width=1800, height=1100, caption=caption)
            for index in range(6)
        )

        spreads = build_album.build_spreads(photos, "天湖", "7 张照片", {}, "auto")

        self.assertLessEqual(spreads.count('data-layout="story"'), 2)
        self.assertGreaterEqual(spreads.count('data-layout="photo-note"'), 2)


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


if __name__ == "__main__":
    unittest.main()
