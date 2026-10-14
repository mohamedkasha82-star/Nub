"""Zero-cost regression checks for local HTML links and fragment targets.

This static audit intentionally skips external URLs and JavaScript-generated destinations.
It checks only links represented in the checked-in HTML source.
"""
from html.parser import HTMLParser
from pathlib import Path
from urllib.parse import unquote, urlsplit
import unittest

ROOT = Path(__file__).resolve().parents[1]
PAGES = sorted(ROOT.glob("*.html"))
SITE_PREFIX = "/Nub/"


class LinkInventory(HTMLParser):
    def __init__(self):
        super().__init__(convert_charrefs=True)
        self.links = []
        self.targets = set()

    def handle_starttag(self, tag, attrs):
        attrs = dict(attrs)
        if "id" in attrs and attrs["id"]:
            self.targets.add(attrs["id"])
        if tag == "a" and attrs.get("name"):
            self.targets.add(attrs["name"])
        if tag in {"a", "area", "link"} and attrs.get("href"):
            self.links.append(attrs["href"])


def inventory(path):
    parser = LinkInventory()
    parser.feed(path.read_text(encoding="utf-8"))
    parser.close()
    return parser


def resolve_local_href(source, href):
    """Return (target path, fragment) for a local URL, or None for non-local URLs."""
    parts = urlsplit(href.strip())
    if parts.scheme or parts.netloc:
        return None
    if href.strip().startswith(("#", "javascript:", "data:", "mailto:", "tel:")):
        if parts.scheme:
            return None
    raw_path = unquote(parts.path)
    if raw_path.startswith(SITE_PREFIX):
        raw_path = raw_path[len(SITE_PREFIX):]
        target = ROOT / raw_path
    elif raw_path.startswith("/"):
        target = ROOT / raw_path.lstrip("/")
    elif raw_path:
        target = source.parent / raw_path
    else:
        target = source
    try:
        target = target.resolve()
        target.relative_to(ROOT.resolve())
    except (ValueError, OSError):
        return None
    if target.is_dir():
        target = target / "index.html"
    return target, unquote(parts.fragment)


class InternalLinkRegressionTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.inventories = {path: inventory(path) for path in PAGES}

    def test_site_has_pages_to_audit(self):
        self.assertTrue(PAGES, "Expected root-level HTML pages to be audited")

    def test_local_link_targets_exist(self):
        problems = []
        for source, parsed in self.inventories.items():
            for href in parsed.links:
                resolved = resolve_local_href(source, href)
                if resolved is None:
                    continue
                target, _fragment = resolved
                if not target.is_file():
                    problems.append(f"{source.relative_to(ROOT)}: {href!r} -> missing {target}")
        self.assertEqual([], problems, "Broken local link targets:\\n" + "\\n".join(problems))

    def test_local_fragment_targets_exist(self):
        problems = []
        for source, parsed in self.inventories.items():
            for href in parsed.links:
                resolved = resolve_local_href(source, href)
                if resolved is None:
                    continue
                target, fragment = resolved
                if not fragment or not target.is_file() or target.suffix.lower() != ".html":
                    continue
                # The evidence catalogue builds source-card IDs from JavaScript data at runtime.
                # Static HTML parsing cannot see those generated targets.
                if target.name == "evidence.html":
                    continue
                target_inventory = self.inventories.get(target)
                if target_inventory is None:
                    target_inventory = inventory(target)
                if fragment not in target_inventory.targets:
                    problems.append(
                        f"{source.relative_to(ROOT)}: {href!r} -> missing #{fragment} in {target.relative_to(ROOT)}"
                    )
        self.assertEqual([], problems, "Broken local fragment targets:\\n" + "\\n".join(problems))


if __name__ == "__main__":
    unittest.main()
