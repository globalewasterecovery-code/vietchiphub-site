from pathlib import Path
import re

root = Path(__file__).parent / "public"
pages = list(root.glob("**/index.html"))
assert len(pages) >= 58, len(pages)
for page in pages:
    text = page.read_text(encoding="utf-8")
    if "thank-you" in page.parts:
        assert 'name="robots" content="noindex"' in text
        continue
    assert "<title>" in text and 'name="description"' in text
    assert 'rel="canonical"' in text
    assert 'application/ld+json' in text
    assert 'name="viewport"' in text
assert (root/"robots.txt").exists()
sitemap = (root/"sitemap.xml").read_text()
assert sitemap.count("<url>") >= 67
assert len(re.findall(r'<h1>', (root/"index.html").read_text())) == 1
assert '<html lang="vi">' in (root/"index.html").read_text()
assert '<html lang="en">' in (root/"en/index.html").read_text()
assert '<html lang="zh">' in (root/"zh/index.html").read_text()
assert '"@type":"Product"' in (root/"chip/stm32f103c8t6/index.html").read_text()
restricted = (root/"chip/nvidia-h100/index.html").read_text()
assert "Kiểm tra tuân thủ bắt buộc" in restricted
assert "né tránh giấy phép" in restricted
print(f"PASS pages={len(pages)} sitemap_urls={sitemap.count('<url>')}")
