// cookie.js — minimal, robust cookie banner state
(() => {
  const KEY = "anjo_cookie_consent_v4"; // "accepted" | "declined"
  const banner = document.querySelector("[data-cookie-banner]");
  if (!banner) return;

  const btnAccept = banner.querySelector("[data-cookie-accept]");
  const btnDecline = banner.querySelector("[data-cookie-decline]");

  function updateGtmConsent(value) {
    if (typeof window.gtag !== "function") return;
    if (value === "accepted") {
      window.gtag("consent", "update", {
        ad_storage: "granted",
        analytics_storage: "granted",
        ad_user_data: "granted",
        ad_personalization: "granted"
      });
    } else {
      window.gtag("consent", "update", {
        ad_storage: "denied",
        analytics_storage: "denied",
        ad_user_data: "denied",
        ad_personalization: "denied"
      });
    }
  }

  function setConsent(value) {
    try { localStorage.setItem(KEY, value); } catch (_) {}
    document.documentElement.dataset.consent = value;
    updateGtmConsent(value);
    banner.hidden = true;
  }

  function readConsent() {
    try { return localStorage.getItem(KEY); } catch (_) { return null; }
  }

  const existing = readConsent();
  if (existing === "accepted" || existing === "declined") {
    document.documentElement.dataset.consent = existing;
    updateGtmConsent(existing);
    banner.hidden = true;
  } else {
    banner.hidden = false;
  }

  btnAccept?.addEventListener("click", () => setConsent("accepted"));
  btnDecline?.addEventListener("click", () => setConsent("declined"));
})();
