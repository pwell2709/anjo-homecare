// langfix.js — build correct language URLs from the REAL current path
// + preserve ?src=orte when switching languages on the contact form (Locations/Property Care restriction)
(() => {
  const LANGS = ["de", "en", "fr", "pt"];

  function stripLeadingLang(pathname) {
    let p = pathname || "/";
    if (!p.startsWith("/")) p = "/" + p;

    for (const l of LANGS) {
      if (p === `/${l}`) return "/";
      if (p.startsWith(`/${l}/`)) return p.slice(3); // keep leading "/"
    }
    return p;
  }

  function isContactRestPath(restPath) {
    // restPath has no leading language (e.g. "/contact/" or "/contact/index.html")
    if (!restPath) return false;
    const p = restPath.endsWith("/") ? restPath.slice(0, -1) : restPath;

    // Support pretty URLs and direct file access
    return (
      p === "/contact" ||
      p === "/contact/index.html" ||
      p === "/contact/index.htm" ||
      p === "/contact.html" ||
      p === "/contact.htm"
    );
  }

  function hasSrcOrteInSearch(search) {
    try {
      const qs = new URLSearchParams(search || "");
      return qs.get("src") === "orte";
    } catch (e) {
      return /(?:\?|&)src=orte(?:&|$)/.test(search || "");
    }
  }

  function setSessionSrcFlag() {
    // Persist the restriction across language switches while staying on the contact form.
    const rest = stripLeadingLang(window.location.pathname);
    const onContact = isContactRestPath(rest);

    if (!onContact) {
      // Leaving contact: do not force anything
      return;
    }

    if (hasSrcOrteInSearch(window.location.search)) {
      try { sessionStorage.setItem("src", "orte"); } catch (e) {}
    } else {
      // If user arrived on contact without src=orte, clear the flag
      try { sessionStorage.removeItem("src"); } catch (e) {}
    }
  }

  function appendContextParamsIfNeeded(url) {
    const rest = stripLeadingLang(window.location.pathname);
    const onContact = isContactRestPath(rest);

    let src = null;
    let ctx = null;
    try {
      const qs = new URLSearchParams(window.location.search || "");
      src = qs.get("src") || null;
      ctx = qs.get("ctx") || null;
    } catch (e) {}

    if (!src) {
      try { src = sessionStorage.getItem("src"); } catch (e) {}
    }

    try {
      const u = new URL(url, window.location.origin);
      if (onContact && src === "orte") u.searchParams.set("src", "orte");
      if (ctx === "") u.searchParams.set("ctx", "");
      const q = u.searchParams.toString();
      return u.pathname + (q ? "?" + q : "");
    } catch (e) {
      let out = url;
      if (onContact && src === "orte" && !/(?:\?|&)src=orte(?:&|$)/.test(out)) {
        out += out.indexOf("?") === -1 ? "?src=orte" : "&src=orte";
      }
      if (ctx === "" && !/(?:\?|&)ctx=(?:&|$)/.test(out)) {
        out += out.indexOf("?") === -1 ? "?ctx=" : "&ctx=";
      }
      return out;
    }
  }

  function buildHref(targetLang) {
    const rest = stripLeadingLang(window.location.pathname);
    return `/${targetLang}${rest}`;
  }

  function apply() {
    // Ensure session flag is aligned with current URL (contact only)
    setSessionSrcFlag();

    document.querySelectorAll(".lang-switch .lang-btn[data-lang]").forEach(a => {
      const targetLang = a.getAttribute("data-lang");
      if (!targetLang) return;

      // If explicit override exists (langLinks), use it first:
      const explicit = a.getAttribute("data-href");
      let target;

      if (explicit && explicit.startsWith("/") && explicit !== `/${targetLang}/` && explicit !== `/${targetLang}`) {
        target = explicit;
      } else {
        target = buildHref(targetLang);
      }

      // Preserve src=orte on contact, EVEN for explicit links
      target = appendContextParamsIfNeeded(target);

      a.setAttribute("href", target);
    });
  }

  apply();
  document.addEventListener("DOMContentLoaded", apply);
})();
