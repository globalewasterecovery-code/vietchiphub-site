#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Self-verifying publish orchestrator for VietChipHub 2026-09-16 news."""
import json, subprocess, sys, os
from pathlib import Path

ROOT = Path(__file__).parent
SLUG = "samsung-tang-gia-dram-nand-7-10-2026"
URLPATH = f"/bo-nho/{SLUG}/"
URL = "https://vietchiphub.com" + URLPATH

res = {"steps": [], "ok": True}

def run(cmd, cwd=None, timeout=300):
    p = subprocess.run(cmd, cwd=cwd, capture_output=True, text=True, timeout=timeout)
    return p.returncode, p.stdout.strip(), p.stderr.strip()

def step(name, code, out="", err=""):
    res["steps"].append({"name": name, "code": code, "out": out[-400:], "err": err[-400:]})
    if code != 0:
        res["ok"] = False

# 0) sanity: files exist
art = ROOT / "public" / "bo-nho" / SLUG / "index.html"
assert art.is_file(), "article missing"
html = art.read_text(encoding="utf-8")
assert 'application/ld+json' in html and 'FACT:' in html and f'"{URLPATH}"' in html or URL in html, "article content check failed"

sm = (ROOT / "public" / "sitemap.xml").read_text(encoding="utf-8")
assert URL in sm, "sitemap missing url"

lp = (ROOT / "public" / "bo-nho" / "index.html").read_text(encoding="utf-8")
assert SLUG in lp, "list page missing card"

res["local_checks"] = "pass"

# 1) git add/commit/push
c,_,_ = run(["git","add","public/bo-nho/"+SLUG+"/index.html","public/sitemap.xml","public/bo-nho/index.html"], cwd=str(ROOT))
step("git_add", c)
c,o,e = run(["git","commit","-m","news(vi): Samsung DRAM+NAND 7-10% price hike - Vietnam buyer BOM/price-lock checklist"], cwd=str(ROOT))
step("git_commit", c, o, e)
c,o,e = run(["git","push","origin","main"], cwd=str(ROOT), timeout=180)
step("git_push", c, o, e)

# 2) deploy to Cloudflare Pages
c,o,e = run(["npx","--yes","wrangler","pages","deploy","public","--project-name","vietchiphub-site","--branch","main"], cwd=str(ROOT), timeout=420)
step("deploy", c, o, e)

# 3) public verification via curl
def curl(url, timeout=60):
    return run(["curl","-s","-o","/dev/null","-w","%{http_code}","-L",url], timeout=timeout)

c,o,_ = curl(URL)
step("verify_article_http", c, o)
res["article_http"] = o

c,o,_ = curl("https://vietchiphub.com/sitemap.xml")
step("verify_sitemap_http", c, o)
res["sitemap_http"] = o

# sitemap contains url?
c,o,_ = run(["curl","-sL","https://vietchiphub.com/sitemap.xml"], timeout=60)
res["sitemap_contains_new_url"] = URL in o

# health
c,o,_ = run(["curl","-sL","https://vietchiphub.com/api/health"], timeout=60)
step("verify_health", c, o)
res["health"] = o

out = ROOT / "memory" / "_deploy_verify_result_20260916.json"
out.write_text(json.dumps(res, ensure_ascii=False, indent=2), encoding="utf-8")
print(json.dumps(res, ensure_ascii=False, indent=2))
sys.exit(0 if res["ok"] else 1)
