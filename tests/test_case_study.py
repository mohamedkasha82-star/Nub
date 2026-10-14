"""Zero-cost regression checks for the NŪB editorial case study."""
from pathlib import Path
import unittest

ROOT = Path(__file__).resolve().parents[1]


class CaseStudyTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.page = (ROOT / "case-study.html").read_text(encoding="utf-8")
        cls.home = (ROOT / "index.html").read_text(encoding="utf-8")
        cls.readme = (ROOT / "README.md").read_text(encoding="utf-8")

    def test_case_study_is_bilingual_and_responsive(self):
        self.assertIn('<html lang="ar" dir="rtl">', self.page)
        self.assertIn('data-lang="en"', self.page)
        self.assertIn('name="viewport"', self.page)
        self.assertIn("@media(max-width:560px)", self.page)

    def test_case_study_discloses_research_limits_and_synthetic_sound(self):
        self.assertIn("not a completed peer-reviewed or community-reviewed archive", self.page)
        self.assertIn("authentic Nubian song", self.page)
        self.assertIn("Rights and consent are distinct", self.page)
        self.assertIn("Unknown stays unknown", self.page)

    def test_case_study_respects_reduced_motion_and_no_audio_autoplay(self):
        self.assertIn("prefers-reduced-motion:reduce", self.page)
        self.assertNotIn("<audio autoplay", self.page.lower())
        self.assertIn("video.pause()", self.page)

    def test_case_study_links_to_existing_project_modules(self):
        for href in (
            "./atlas.html", "./evidence.html", "./research-map.html",
            "./soundscape.html", "./culture.html", "./fieldwork.html",
            "./sources.html", "./index.html",
        ):
            with self.subTest(href=href):
                self.assertIn(f'href="{href}"', self.page)

    def test_case_study_is_discoverable_from_homepage_and_readme(self):
        self.assertIn('href="./case-study.html"', self.home)
        self.assertIn("case-study.html", self.readme)


if __name__ == "__main__":
    unittest.main()
