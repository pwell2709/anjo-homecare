// back.js — global back button
(() => {
  const btn = document.querySelector('[data-back-button]');
  if (!btn) return;

  const fallback = btn.getAttribute('data-fallback') || '/';

  const sameOriginReferrer = (() => {
    try {
      return !!document.referrer && new URL(document.referrer).origin === window.location.origin;
    } catch (_) {
      return false;
    }
  })();

  btn.addEventListener('click', () => {
    if (window.history.length > 1 && sameOriginReferrer) {
      window.history.back();
    } else {
      window.location.assign(fallback);
    }
  });
})();
