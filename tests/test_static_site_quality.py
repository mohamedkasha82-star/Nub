"""Free regression checks for baseline accessibility and safe external links.

These checks are deliberately dependency-light and do not replace a full WCAG audit.
"""
from html.parser import HTMLParser
from pathlib import Path
import unittest

ROOT = Path(__file__).resolve().parents[1]
PAGES = sorted(ROOT.glob("*.html"))


class DocumentAudit(HTMLParser):
    def __init__(self):
        super().__init__(convert_charrefs=True)
        self.html_attrs = None
        self.title_text = []
        self.in_title = False
        self.meta_names = set()
        self.images = []
        self.blank_links = []
        self.audio = []
        self._audio_attrs = None

    def handle_starttag(self, tag, attrs):
        attrs = dict(attrs)
        if tag == "html":
            self.html_attrs = attrs
        elif tag == "title":
            self.in_title = True
        elif tag == "meta":
            if attrs.get("name", "").lower() == "viewport":
                self.meta_names.add("viewport")
        elif tag == "img":
            self.images.append(attrs)
        elif tag == "a" and attrs.get("target", "").lower() == "_blank":
            self.blank_links.append(attrs)
        elif tag == "audio":
            self.audio.append(attrs)

    def handle_endtag(self, tag):
        if tag == "title":
            self.in_title = False

    def handle_data(self, data):
        if self.in_title:
            self.title_text.append(data)


def audit(path):
    parser = DocumentAudit()
    parser.feed(path.read_text(encoding="utf-8"))
    parser.close()
    return parser


class StaticSiteQualityTests(unittest.TestCase):
    def test_site_has_html_pages_to_audit(self):
        self.assertTrue(PAGES, "Expected root-level HTML pages to be audited")

    def test_every_page_declares_language_direction_title_and_viewport(self):
        for path in PAGES:
            with self.subTest(page=path.name):
                audit_result = audit(path)
                self.assertIsNotNone(audit_result.html_attrs, "Missing html element")
                self.assertTrue(audit_result.html_attrs.get("lang", "").strip(), "Missing document language")
                self.assertTrue(audit_result.html_attrs.get("dir", "").strip(), "Missing text direction")
                self.assertTrue("viewport" in audit_result.meta_names, "Missing responsive viewport meta")
                self.assertTrue("".join(audit_result.title_text).strip(), "Missing document title")

    def test_images_have_alt_attributes(self):
        for path in PAGES:
            for index, image_attrs in enumerate(audit(path).images, start=1):
                with self.subTest(page=path.name, image=index):
                    self.assertIn("alt", image_attrs, "Image is missing alt text (use alt='' only if decorative)")

    def test_new_tab_links_prevent_opener_access(self):
        for path in PAGES:
            for index, link_attrs in enumerate(audit(path).blank_links, start=1):
                with self.subTest(page=path.name, link=index, href=link_attrs.get("href")):
                    rel = {token.lower() for token in link_attrs.get("rel", "").split()}
                    self.assertIn("noopener", rel, "target=_blank links must include rel=noopener")

    def test_audio_is_user_controlled_not_autoplayed(self):
        for path in PAGES:
            for index, audio_attrs in enumerate(audit(path).audio, start=1):
                with self.subTest(page=path.name, audio=index):
                    self.assertIn("controls", audio_attrs, "Audio needs visible playback controls")
                    self.assertNotIn("autoplay", audio_attrs, "Cultural audio must never autoplay")

    def test_sonic_atlas_is_opt_in_and_culturally_transparent(self):
        page = ROOT / "soundscape.html"
        self.assertTrue(page.is_file(), "Sonic Atlas page should exist")
        source = page.read_text(encoding="utf-8")
        self.assertIn("Audio never starts automatically", source)
        self.assertIn("or an authentic Nubian song", source)
        self.assertIn("prefers-reduced-motion:reduce", source)
        self.assertIn("visibilitychange", source)
        self.assertIn("addEventListener('click',()=>playing?stopSound():startSound())", source)

    def test_sonic_atlas_is_linked_from_homepage(self):
        source = (ROOT / "index.html").read_text(encoding="utf-8")
        self.assertIn('href="./soundscape.html"', source)
        self.assertIn("Sonic Atlas", source)


    def test_case_study_is_bilingual_and_academically_transparent(self):
        page = ROOT / "case-study.html"
        self.assertTrue(page.is_file(), "NŪB case study should exist")
        source = page.read_text(encoding="utf-8")
        self.assertIn('data-ar=', source)
        self.assertIn('data-en=', source)
        self.assertIn("peer review", source)
        self.assertIn("UNKNOWN", source)
        self.assertIn("prefers-reduced-motion:reduce", source)
        self.assertIn('href="./research-map.html"', source)
        self.assertIn('href="./fieldwork.html"', source)

    def test_case_study_is_linked_from_homepage(self):
        source = (ROOT / "index.html").read_text(encoding="utf-8")
        self.assertIn('href="./case-study.html"', source)
        case_study = (ROOT / "case-study.html").read_text(encoding="utf-8")
        self.assertIn("not a replacement for Nubia Odyssey", case_study)


if __name__ == "__main__":
    unittest.main()
