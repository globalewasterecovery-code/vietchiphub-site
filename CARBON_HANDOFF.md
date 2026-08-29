DATE=2026-08-29
AI_WORKER=Claude
PROJECT=VietChipHub (vietchiphub-v1)
BRANCH=main
LAST_COMMIT=cce99d8
COMPLETED=
- Shared lang-persist.js wired in (see commit cce99d8). Existing vi/en/zh + hreflang generator structure untouched — persistence only.
- Added public/js/lang-persist.js: click-listener on the top-bar switcher (`.top a`) storing the chosen language (localStorage + 365-day cookie); on the plain Vietnamese root page only, redirects a returning visitor to their stored non-vi choice, or recommends zh/en from navigator.languages on a genuinely first visit (never forces, never touches a direct /en/ or /zh/ visit).
- Instead of editing each of the ~5 separate page-shell f-string builders individually (higher risk of missing one), patched the 2 shared footer builders (footer() and localized_page()'s inline `foot` variable) that every shell ultimately calls — one script tag insertion point covers all ~96 generated pages.
- Backed up build_site.py to build_site.py.pre-i18n-backup before editing.
TESTED=
- python3 -m py_compile — syntax OK.
- Ran `python3 build_site.py` — regenerated all ~96 pages successfully, no errors.
- git diff confirmed EVERY changed file's only difference is the single appended `<script src="/js/lang-persist.js" defer></script>` line — no unintended content drift anywhere.
- Unit-tested the redirect-decision logic in isolation (Node): manual/stored choice always wins over browser locale; an already-vi visitor with no stored preference gets no redirect; a first-time zh-CN browser gets recommended /zh/; a stored 'en' choice persists even when the browser locale is vi-VN.
NOT_TESTED=
- Live browser round-trip against the deployed Netlify site (verified at the unit-logic + build-output level only, consistent with the time budget for this pass).
BLOCKERS=
GitHub push not attempted this pass — same 403-from-proxy condition as the other 3 repos, not retried (per the standing rule: one attempt per repo, no repeated retries).
FILES_CHANGED=
build_site.py (2 targeted edits to footer()/foot), build_site.py.pre-i18n-backup (new), public/js/lang-persist.js (new), ~96 generated HTML pages under public/ (regenerated, each with one appended script tag), CARBON_HANDOFF.md (this file).
DATABASE_CHANGES=none
ROLLBACK=
Restore build_site.py from build_site.py.pre-i18n-backup, delete public/js/lang-persist.js, re-run `python3 build_site.py` to regenerate all pages back to their prior state.
NEXT_ACTION=
1. Extend to ko/ja per Carbon's VietChipHub priority list — same caution as VietnamZiChan applies: check whether build_site.py has similarly scattered per-language dict literals before adding new lang codes (this file's structure is different — labels come from one `labels = ({...} if vi else {...})` ternary in localized_page(), which is cleaner than VietnamZiChan's — worth a quick check but likely safer to extend).
2. Live browser verification against the deployed site once pushed.
SAFE_TO_CONTINUE=yes

UPDATE_2026_08_29_CLAUDE_PUSH_ATTEMPT=
- Read /Users/shangdizhishou/Documents/Codex/2026-08-29/referenced-chatgpt-conversation-this-is-an/CLAUDE_HANDOFF_2026-08-29.md in full before acting; did not repeat any already-completed Netlify deploy or Supabase migration work.
- Verified local state directly (not trusting prior claims): VNGO HEAD=b130b96, VietChipHub HEAD=9541c25, SoulEntropy HEAD=4494434, VietnamZiChan HEAD=ab74248 — all four match the handoff exactly; all four working trees clean except the pre-existing untracked memory/ files (left untouched).
- NEW FINDING: this session's device-bridge shell (the sandboxed VM behind the remote-devices tools) has ZERO network egress to github.com AND api.netlify.com — `curl https://api.github.com/` and `curl https://api.netlify.com/` both return "403 from proxy after CONNECT" with no credentials involved at all. `git fetch origin` on VNGO fails the same way. This is a proxy/allowlist-level block on this specific bridged environment, distinct from (and in addition to) the GitHub-identity mismatch the handoff already diagnosed (yuguanbo020-svg cached, wrong owner for these 3 repos). Even with correct globalewasterecovery-code credentials, this session cannot push, fetch, or check Netlify from here.
- Consequence: could not fetch/verify fast-forward safety, could not push, could not check Netlify deploy status, could not run the post-push smoke test — none of this is executable from this session's environment regardless of GitHub identity. Did not force-push, did not touch remotes, did not touch Netlify settings, did not attempt the push blindly.
- No PAT/credential was requested from or entered by Claude — per standing policy, credential entry is left to the user's own terminal.
- Handoff docs and CARBON_TASK_QUEUE.json updated with this finding so the next session/agent does not re-attempt the push from this same bridged environment expecting a different result.
