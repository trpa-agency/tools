/* TRPA Tools, QA gate.
   Every page under qa/ loads this script first in <head>. It hides the page
   until the visitor enters the shared QA password, then remembers the unlock
   in localStorage for TTL_DAYS. The password itself is not in the repo: only
   the SHA-256 of SALT + password is, so this keeps casual visitors out of
   work in progress. It is not security; the pages and their data still ship
   to the browser. Do not gate anything that must stay private.

   To change the password, run from the repo root:
     python scripts/qa_gate_hash.py "new password"
   and paste the printed hash into HASH below. Everyone is asked for the new
   password on their next visit because the stored unlock carries the hash. */
(function () {
  'use strict';

  var HASH = '521b3c33dcd4759575d3ab6cfb9cca4f80c8c536091f72299831cb0cd9729050';
  var SALT = 'tools.trpa.gov/qa';
  var KEY = 'trpa-tools-qa-gate';
  var TTL_DAYS = 30;
  var REQUEST_MAILTO = 'mailto:gis@trpa.gov?subject=' + encodeURIComponent('TRPA Tools QA password') +
    '&body=' + encodeURIComponent('Hi GIS team,\n\nCould you send me the password for the apps in development at TRPA Tools?\n\nPage: ') + encodeURIComponent(location.href);

  function unlocked() {
    try {
      var saved = JSON.parse(localStorage.getItem(KEY) || 'null');
      return !!saved && saved.hash === HASH && saved.until > Date.now();
    } catch (e) { return false; }
  }

  function remember() {
    try {
      localStorage.setItem(KEY, JSON.stringify({ hash: HASH, until: Date.now() + TTL_DAYS * 86400000 }));
    } catch (e) { /* private mode: the unlock lasts for this page only */ }
  }

  function sha256(text) {
    var bytes = new TextEncoder().encode(text);
    return crypto.subtle.digest('SHA-256', bytes).then(function (buf) {
      return Array.prototype.map.call(new Uint8Array(buf), function (b) {
        return ('0' + b.toString(16)).slice(-2);
      }).join('');
    });
  }

  // Relock from the console or a future "lock" link: qaGate.lock()
  window.qaGate = {
    lock: function () { try { localStorage.removeItem(KEY); } catch (e) {} location.reload(); }
  };

  if (unlocked()) return;

  // Assets live next to this script, whatever the page depth.
  var assets = (document.currentScript && document.currentScript.src || '').replace(/[^\/]*$/, '');

  var root = document.documentElement;
  root.classList.add('qa-locked');

  var style = document.createElement('style');
  style.textContent = [
    'html.qa-locked { overflow: hidden !important; }',
    'html.qa-locked body > :not(.qa-gate) { visibility: hidden !important; }',
    '.qa-gate { position: fixed; inset: 0; z-index: 2147483647; display: flex; align-items: center; justify-content: center;',
    '  padding: 1.5rem; box-sizing: border-box; background: #003B71; visibility: visible !important;',
    '  font-family: "Open Sans", "Segoe UI", Calibri, system-ui, sans-serif; color: #003B71; }',
    '.qa-gate * { box-sizing: border-box; }',
    '.qa-gate .qa-gate-card { width: 100%; max-width: 420px; background: #fff; border-radius: 10px; padding: 2rem 2rem 1.5rem;',
    '  box-shadow: 0 12px 40px rgba(0, 0, 0, 0.35); border-top: 6px solid #E87722; }',
    '.qa-gate .qa-gate-logo { display: block; height: 44px; width: auto; margin: 0 0 1.25rem; }',
    '.qa-gate h1 { font-size: 1.25rem; font-weight: 600; margin: 0 0 0.35rem; line-height: 1.3; }',
    '.qa-gate p { margin: 0 0 1.25rem; font-size: 0.95rem; line-height: 1.5; color: #3d5a7a; }',
    '.qa-gate label { display: block; font-size: 0.85rem; font-weight: 600; margin-bottom: 0.35rem; }',
    '.qa-gate .qa-gate-row { display: flex; gap: 0.5rem; }',
    '.qa-gate input { flex: 1; min-width: 0; font: inherit; font-size: 1rem; padding: 0.6rem 0.75rem; border: 1px solid #9fb6cf; border-radius: 6px; color: #003B71; }',
    '.qa-gate input:focus { outline: 2px solid #0072CE; outline-offset: 1px; border-color: #0072CE; }',
    '.qa-gate button { font: inherit; font-size: 1rem; font-weight: 600; padding: 0.6rem 1.1rem; border: 0; border-radius: 6px; background: #0072CE; color: #fff; cursor: pointer; }',
    '.qa-gate button:hover { background: #005ea8; }',
    '.qa-gate button:disabled { opacity: 0.6; cursor: default; }',
    '.qa-gate .qa-gate-error { min-height: 1.3em; margin: 0.6rem 0 0; font-size: 0.875rem; color: #9C3E27; }',
    '.qa-gate .qa-gate-request { display: inline-flex; align-items: center; gap: 0.4rem; margin: 0.9rem 0 0; padding: 0.5rem 0.9rem; border: 1px solid #0072CE; border-radius: 6px;',
    '  background: #fff; color: #0072CE; font-size: 0.9rem; font-weight: 600; text-decoration: none; }',
    '.qa-gate .qa-gate-request:hover { background: #eaf3fc; }',
    '.qa-gate .qa-gate-request svg { width: 16px; height: 16px; flex: none; }',
    '.qa-gate .qa-gate-foot { margin: 1.25rem 0 0; padding-top: 0.9rem; border-top: 1px solid #e3ebf4; font-size: 0.8rem; color: #5f7893; }',
    '.qa-gate .qa-gate-foot a { color: #0072CE; }',
    '@media (prefers-reduced-motion: no-preference) { .qa-gate .qa-gate-card.shake { animation: qa-gate-shake 0.35s; } }',
    '@keyframes qa-gate-shake { 20%, 60% { transform: translateX(-6px); } 40%, 80% { transform: translateX(6px); } }'
  ].join('\n');
  document.head.appendChild(style);

  function render() {
    var gate = document.createElement('div');
    gate.className = 'qa-gate';
    gate.setAttribute('role', 'dialog');
    gate.setAttribute('aria-labelledby', 'qa-gate-title');
    gate.innerHTML =
      '<form class="qa-gate-card" autocomplete="off">' +
        '<img class="qa-gate-logo" src="' + assets + 'TRPALogo_COLOR.png" alt="Tahoe Regional Planning Agency" />' +
        '<h1 id="qa-gate-title">Apps in development</h1>' +
        '<p>This part of TRPA Tools holds apps under review that may change or break. Enter the QA password to continue.</p>' +
        '<label for="qa-gate-input">Password</label>' +
        '<div class="qa-gate-row">' +
          '<input id="qa-gate-input" type="password" autocapitalize="off" spellcheck="false" required />' +
          '<button type="submit">Enter</button>' +
        '</div>' +
        '<p class="qa-gate-error" role="alert" aria-live="polite"></p>' +
        '<a class="qa-gate-request" href="' + REQUEST_MAILTO + '">' +
          '<svg viewBox="0 0 16 16" aria-hidden="true" fill="none" stroke="currentColor" stroke-width="1.5"><rect x="1.5" y="3" width="13" height="10" rx="1.5"/><path d="M2 4l6 5 6-5"/></svg>' +
          'Request the password' +
        '</a>' +
        '<p class="qa-gate-foot">Looking for the public apps? <a href="' + assets + '../">TRPA Tools</a></p>' +
      '</form>';
    document.body.appendChild(gate);

    var form = gate.querySelector('form');
    var input = gate.querySelector('input');
    var button = gate.querySelector('button');
    var error = gate.querySelector('.qa-gate-error');

    if (!(window.crypto && crypto.subtle)) {
      error.textContent = 'This page has to be opened over https or localhost to unlock.';
      input.disabled = button.disabled = true;
      return;
    }

    form.addEventListener('submit', function (ev) {
      ev.preventDefault();
      var value = input.value;
      if (!value) return;
      button.disabled = true;
      sha256(SALT + value).then(function (hex) {
        if (hex === HASH) {
          remember();
          root.classList.remove('qa-locked');
          gate.remove();
          style.remove();
          return;
        }
        error.textContent = 'That password did not match.';
        form.classList.remove('shake');
        void form.offsetWidth;
        form.classList.add('shake');
        input.select();
        button.disabled = false;
      });
    });

    input.focus();
  }

  if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', render);
  } else {
    render();
  }
})();
