// langfix.js — build correct language URLs from the REAL current path
// + preserve ?src=orte when switching languages on the contact form (Locations/Property Care restriction)
(() => {
  const LANGS = ["de", "en", "fr", "pt"];

  // NEW: sanitize any incoming path to remove quotes + normalize slashes
  function sanitizePath(p) {
    if (!p) return "/";
    p = p.replace(/"/g, "");       // remove stray quotes
    p = p.replace(/'+/g, "");      // remove stray single quotes
    p = p.replace(/\/{2,}/g, "/"); // collapse multiple slashes
    if (!p.startsWith("/")) p = "/" + p;
    return p;
  }

  function stripLeadingLang(pathname) {
    let p = sanitizePath(pathname || "/");

    for (const l of LANGS) {
      if (p === `/${l}`) return "/";
      if (p.startsWith(`/${l}/`)) return p.slice(3); // keep leading "/"
    }
    return p;
  }

  function isContactRestPath(restPath) {
    if (!restPath) return false;
    const p = sanitizePath(restPath.endsWith("/") ? restPath.slice(0, -1) : restPath);

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
    const rest = stripLeadingLang(window.location.pathname);
    const onContact = isContactRestPath(rest);

    if (!onContact) return;

    if (hasSrcOrteInSearch(window.location.search)) {
      try { sessionStorage.setItem("src", "orte"); } catch (e) {}
    } else {
      try { sessionStorage.removeItem("src"); } catch (e) {}
    }
  }

  function appendContextParamsIfNeeded(url) {
    url = sanitizePath(url);

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
      return sanitizePath(u.pathname + (q ? "?" + q : ""));
    } catch (e) {
      let out = url;
      if (onContact && src === "orte" && !/(?:\?|&)src=orte(?:&|$)/.test(out)) {
        out += out.indexOf("?") === -1 ? "?src=orte" : "&src=orte";
      }
      if (ctx === "" && !/(?:\?|&)ctx=(?:&|$)/.test(out)) {
        out += out.indexOf("?") === -1 ? "?ctx=" : "&ctx=";
      }
      return sanitizePath(out);
    }
  }

  function buildHref(targetLang) {
    const rest = stripLeadingLang(window.location.pathname);
    return sanitizePath(`/${targetLang}${rest}`);
  }

  function apply() {
    setSessionSrcFlag();

    document.querySelectorAll(".lang-switch .lang-btn[data-lang]").forEach(a => {
      const targetLang = a.getAttribute("data-lang");
      if (!targetLang) return;

      const explicit = a.getAttribute("data-href");
      let target;

      if (explicit && explicit.startsWith("/") && explicit !== `/${targetLang}/` && explicit !== `/${targetLang}`) {
        target = sanitizePath(explicit);
      } else {
        target = buildHref(targetLang);
      }

      target = appendContextParamsIfNeeded(target);

      a.setAttribute("href", target);
    });
  }

  apply();
  document.addEventListener("DOMContentLoaded", apply);
})();

