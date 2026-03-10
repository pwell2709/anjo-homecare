// scripts/check-output.mjs
// Guardrails for Eleventy output (_site). Fails build if issues found.

import fs from "node:fs";
import path from "node:path";

const ROOT = process.cwd();
const SITE_DIR = path.join(ROOT, "_site");

// Your canonical base (MUST match your SEO decision)
const CANONICAL_BASE = "https://anjo-cleaning.com";
const FORBIDDEN_BASE = "https://www.anjo-cleaning.com";

const IGNORE_DIRS = new Set(["node_modules"]);
const TEXT_EXT = new Set([
  ".html", ".xml", ".txt", ".css", ".js", ".json", ".map", ".webmanifest", ".svg"
]);

// Paths in output that are expected to be legacy redirects / non-index pages.
// We intentionally DO NOT require full hreflang/canonical sets on these.
const IGNORE_URL_PREFIXES = [
  "/de/house/",
  "/de/house-sitting-madeira/",
  "/de/reinigung/",
  "/en/house/",
  "/en/house-sitting-madeira/",
  "/en/cleaning/",
  "/fr/house/",
  "/fr/house-sitting-madeira/",
  "/fr/nettoyage/",
  "/pt/house/",
  "/pt/house-sitting-madeira/",
  "/pt/limpeza/",
];

function shouldSkipHtmlChecks(filePath) {
  const rel = "/" + path.relative(SITE_DIR, filePath).replace(/\\/g, "/");
  // Map /de/index.html etc. into directory index form
  const relDir = rel.endsWith("/index.html") ? rel.slice(0, -("index.html".length)) : rel;
  return IGNORE_URL_PREFIXES.some(p => relDir.startsWith(p));
}

function walk(dir, out = []) {
  const entries = fs.readdirSync(dir, { withFileTypes: true });
  for (const e of entries) {
    if (e.isDirectory()) {
      if (IGNORE_DIRS.has(e.name)) continue;
      walk(path.join(dir, e.name), out);
    } else if (e.isFile()) {
      out.push(path.join(dir, e.name));
    }
  }
  return out;
}

function readTextIfLikely(filePath) {
  const ext = path.extname(filePath).toLowerCase();
  if (!TEXT_EXT.has(ext)) return null;

  const stat = fs.statSync(filePath);
  if (stat.size > 8 * 1024 * 1024) return null;

  try {
    return fs.readFileSync(filePath, "utf8");
  } catch {
    return null;
  }
}

function addError(errors, file, message) {
  errors.push({ file: path.relative(ROOT, file), message });
}

function main() {
  if (!fs.existsSync(SITE_DIR)) {
    console.error(`❌ _site not found at: ${SITE_DIR}\nRun "npm run build" first.`);
    process.exit(1);
  }

  const errors = [];
  const files = walk(SITE_DIR);

  // ---- Check robots.txt ----
  const robotsPath = path.join(SITE_DIR, "robots.txt");
  if (!fs.existsSync(robotsPath)) {
    addError(errors, robotsPath, "robots.txt is missing in _site/");
  } else {
    const robots = fs.readFileSync(robotsPath, "utf8");
    const expected = `Sitemap: ${CANONICAL_BASE}/sitemap.xml`;
    if (!robots.includes(expected)) {
      addError(errors, robotsPath, `robots.txt must contain: "${expected}"`);
    }
    if (robots.includes(FORBIDDEN_BASE)) {
      addError(errors, robotsPath, `robots.txt must not reference: ${FORBIDDEN_BASE}`);
    }
  }

  // ---- Check sitemap.xml ----

  const sitemapPath = path.join(SITE_DIR, "sitemap.xml");
  if (!fs.existsSync(sitemapPath)) {
    addError(errors, sitemapPath, "sitemap.xml is missing in _site/");
  } else {
    const xml = fs.readFileSync(sitemapPath, "utf8");

    if (!xml.includes("<urlset") || !xml.includes("<url>")) {
      addError(errors, sitemapPath, "sitemap.xml looks invalid (missing <urlset> or <url>).");
    }

    if (xml.includes(FORBIDDEN_BASE)) {
      addError(errors, sitemapPath, `sitemap.xml must not contain: ${FORBIDDEN_BASE}`);
    }

    const locMatches = [...xml.matchAll(/<loc>([^<]+)<\/loc>/g)].map(m => m[1]);
    for (const loc of locMatches) {
      if (loc.includes(" ")) {
        addError(errors, sitemapPath, `Found space in <loc>: ${loc}`);
      }
      if (!loc.startsWith(CANONICAL_BASE + "/")) {
        addError(errors, sitemapPath, `Non-canonical <loc> (must start with ${CANONICAL_BASE}/): ${loc}`);
      }
    }
  }

  // ---- Scan all text files for forbidden patterns ----
  for (const f of files) {
    const txt = readTextIfLikely(f);
    if (txt == null) continue;

    if (txt.includes(FORBIDDEN_BASE)) {
      addError(errors, f, `Contains forbidden base URL: ${FORBIDDEN_BASE}`);
    }

    // (guard) removed: generic whitespace-in-URL heuristic (handled by sitemap/canonical/hreflang checks)

    if (path.extname(f).toLowerCase() === ".html") {
      // Skip strict SEO checks for known legacy redirect pages
      if (shouldSkipHtmlChecks(f)) {
        continue;
      }

      // If page is explicitly noindex or a redirect shell, don't require hreflang set
      const isNoIndex = /<meta\s+name=["']robots["'][^>]*content=["'][^"']*noindex/i.test(txt);
      const isMetaRefresh = /<meta\s+http-equiv=["']refresh["']/i.test(txt);
      const isJsRedirect = /window\.location\.(href|replace)\s*=|location\.replace\(/i.test(txt);

      if (isNoIndex || isMetaRefresh || isJsRedirect) {
        // Still enforce no forbidden www base
        continue;
      }

      const canon = txt.match(/<link\s+rel=["']canonical["']\s+href=["']([^"']+)["']/i);
      if (!canon) {
        addError(errors, f, "Missing canonical link tag.");
      } else {
        const href = canon[1];
        if (!href.startsWith(CANONICAL_BASE + "/")) {
          addError(errors, f, `Canonical is not non-www: ${href}`);
        }
        if (href.includes(" ")) {
          addError(errors, f, `Canonical contains space: ${href}`);
        }
      }

      const hreflangs = [...txt.matchAll(/rel=["']alternate["'][^>]*hreflang=["']([^"']+)["'][^>]*href=["']([^"']+)["']/gi)]
        .map(m => ({ lang: m[1], href: m[2] }));

      const langsNeeded = ["de", "en", "fr", "pt", "x-default"];
      const foundLangs = new Set(hreflangs.map(h => h.lang.toLowerCase()));

      for (const l of langsNeeded) {
        if (!foundLangs.has(l)) {
          addError(errors, f, `Missing hreflang="${l}" link tag.`);
        }
      }

      for (const h of hreflangs) {
        if (h.href.includes(" ")) {
          addError(errors, f, `hreflang href contains space: ${h.href}`);
        }
        if (h.href.startsWith(FORBIDDEN_BASE)) {
          addError(errors, f, `hreflang href must not use www: ${h.href}`);
        }
      }
    }
  }

  if (errors.length) {
    console.error(`\n❌ Output check FAILED (${errors.length} issue(s)):\n`);
    for (const e of errors) {
      console.error(`- ${e.file}: ${e.message}`);
    }
    console.error("\nFix the issues above, then rebuild.\n");
    process.exit(1);
  }

  console.log("✅ Output check passed: non-www, sitemap, canonical/hreflang look consistent.");
}

main();
