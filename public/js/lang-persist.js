// Carbon shared language-persistence script (site_i18n module, persistence-only
// overlay for sites with their own existing per-locale page system).
// VietChipHub already generates real vi/en/zh pages with hreflang via
// build_site.py — this script does NOT translate anything. It only:
// 1. Remembers a visitor's manually-chosen language (localStorage + cookie).
// 2. On the site root ("/", Vietnamese) only, redirects a returning visitor
//    to their stored language, or recommends one from navigator.languages
//    on a first visit — manual/previous choice always wins, never IP-forced.
(function () {
  'use strict';
  var LK = 'vchub_lang';

  function setLang(v) {
    try { localStorage.setItem(LK, v); } catch (e) {}
    var d = new Date();
    d.setTime(d.getTime() + 365 * 864e5);
    document.cookie = LK + '=' + v + ';expires=' + d.toUTCString() + ';path=/;SameSite=Lax';
  }

  function getLang() {
    try {
      var v = localStorage.getItem(LK);
      if (v) return v;
    } catch (e) {}
    var m = document.cookie.match(/(?:^|; )vchub_lang=([^;]*)/);
    return m ? m[1] : null;
  }

  // Record clicks on the top-bar switcher links (VI / EN / 中文).
  document.addEventListener('click', function (e) {
    var a = e.target.closest && e.target.closest('.top a');
    if (!a) return;
    var href = a.getAttribute('href') || '';
    if (href === '/') { setLang('vi'); return; }
    var m = href.match(/^\/([a-z]{2})\//);
    if (m) setLang(m[1]);
  });

  // Only the plain Vietnamese root page redirects — never a direct visit to
  // /en/ or /zh/, which is always respected as-is.
  if (window.location.pathname === '/') {
    var valid = ['vi', 'en', 'zh'];
    var stored = getLang();
    if (stored && valid.indexOf(stored) !== -1 && stored !== 'vi') {
      window.location.replace('/' + stored + '/');
      return;
    }
    if (!stored) {
      var langs = (navigator.languages || [navigator.language || '']).map(function (x) {
        return (x || '').toLowerCase();
      });
      for (var i = 0; i < langs.length; i++) {
        if (langs[i].indexOf('zh') === 0) { window.location.replace('/zh/'); return; }
        if (langs[i].indexOf('en') === 0) { window.location.replace('/en/'); return; }
        if (langs[i].indexOf('vi') === 0) { return; } // already on vi root
      }
    }
  }
})();
