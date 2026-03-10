const fs = require("fs");
const path = require("path");

const ROOT = "./src";

function walk(dir){
  const files = fs.readdirSync(dir);

  files.forEach(file => {

    const full = path.join(dir,file);
    const stat = fs.statSync(full);

    if(stat.isDirectory()){
      walk(full);
      return;
    }

    if(!file.endsWith(".njk") && !file.endsWith(".html")) return;

    let content = fs.readFileSync(full,"utf8");

    /* nur Links ohne bestehende class ändern */
    content = content.replace(
      /<a\s+href="([^"]+)"/g,
      `<a class="cta-link" href="$1"`
    );

    fs.writeFileSync(full,content);

    console.log("bearbeitet:",full);

  });
}

walk(ROOT);

console.log("Textlinks wurden zu CTA-Buttons geändert.");