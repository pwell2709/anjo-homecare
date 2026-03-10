const fs = require("fs");
const path = require("path");

const ROOT = "./src";

function walk(dir) {
  let results = [];
  const list = fs.readdirSync(dir);

  list.forEach(file => {
    const filePath = path.join(dir, file);
    const stat = fs.statSync(filePath);

    if (stat.isDirectory()) {
      results = results.concat(walk(filePath));
    } else if (file.endsWith(".njk") || file.endsWith(".html")) {
      results.push(filePath);
    }
  });

  return results;
}

function fixFile(file) {

  let content = fs.readFileSync(file,"utf8");

  const regex = /{%\s*if\s*page\.url\s*!=\s*"([^"]+)"\s*%}/g;

  content = content.replace(regex,(match,url)=>{

    return `{% if not page.url.startsWith("${url}") %}`;

  });

  fs.writeFileSync(file,content);

}

const files = walk(ROOT);

files.forEach(file => fixFile(file));

console.log("Hamburger Menü Logik korrigiert.");