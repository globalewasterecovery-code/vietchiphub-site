from pathlib import Path
import re

root = Path(__file__).parent / "public"
pages = list(root.glob("**/index.html"))
assert len(pages) >= 20, len(pages)
for page in pages:
    text = page.read_text(encoding="utf-8")
    assert "<title>" in text and 'name="description"' in text
    assert 'rel="canonical"' in text
    assert 'application/ld+json' in text
    assert 'name="viewport"' in text
assert (root/"robots.txt").exists()
sitemap = (root/"sitemap.xml").read_text()
assert sitemap.count("<url>") >= 19
assert len(re.findall(r'<h1>', (root/"index.html").read_text())) == 1
print(f"PASS pages={len(pages)} sitemap_urls={sitemap.count('<url>')}")
