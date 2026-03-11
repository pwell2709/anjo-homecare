const fs = require("fs");
const path = require("path");

const forbidden = [
  "/al/",
  "al-madeira",
  "cleaning-for-al",
  "nettoyage-al",
  "limpeza-al",
  "landinging"
];

function scan(dir) {
  const files = fs.readdirSync(dir);
  files.forEach(file => {
    const full = path.join(dir, file);

    if (fs.statSync(full).isDirectory()) {
      scan(full);
    } else if (full.endsWith(".html")) {
      const content = fs.readFileSync(full, "utf8");

      forbidden.forEach(pattern => {
        if (content.includes(pattern)) {
          console.error(`Forbidden slug detected: ${pattern} in ${full}`);
          process.exit(1);
        }
      });
    }
  });
}

scan("_site");

console.log("Build guard passed.");