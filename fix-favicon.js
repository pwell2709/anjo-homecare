const fs = require("fs");

const file = "./src/_layouts/base.njk";

let content = fs.readFileSync(file, "utf8");

/* .ico entfernen */
content = content.replace(/.*favicon\.ico.*\n?/g, "");

/* SVG Favicon sicherstellen */
if (!content.includes("favicon.svg")) {

const svgLine =
'<link rel="icon" type="image/svg+xml" href="/assets/favicons/favicon.svg">';

content = content.replace(
"</head>",
svgLine + "\n</head>"
);

}

fs.writeFileSync(file, content);

console.log("favicon.svg aktiviert und .ico entfernt");