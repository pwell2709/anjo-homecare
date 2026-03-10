const fs = require("fs");
const path = require("path");

const ROOT = "./src";

function walk(dir) {
  let results = [];
  const list = fs.readdirSync(dir);

  list.forEach(file => {
    const filePath = path.join(dir, file);
    const stat = fs.statSync(filePath);

    if (stat && stat.isDirectory()) {
      results = results.concat(walk(filePath));
    } else {
      if (filePath.endsWith(".njk") || filePath.endsWith(".html")) {
        results.push(filePath);
      }
    }
  });

  return results;
}

function processFile(file) {
  let content = fs.readFileSync(file, "utf8");

  const regex = /<li>\s*<a href="([^"]+)">([\s\S]*?)<\/a>\s*<\/li>/g;

  const updated = content.replace(regex, (match, url, text) => {
    if (match.includes("page.url")) return match;

    return `{% if page.url != "${url}" %}\n<li><a href="${url}">${text}</a></li>\n{% endif %}`;
  });

  if (updated !== content) {
    fs.writeFileSync(file, updated);
    console.log("updated:", file);
  }
}

const files = walk(ROOT);

files.forEach(file => processFile(file));

console.log("Hamburger-Menüs automatisch angepasst.");