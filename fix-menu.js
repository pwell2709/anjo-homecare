const fs = require("fs");

/* ---------- 1. Hamburger Logik ---------- */

const headerFile = "./src/_includes/components/header.njk";

let header = fs.readFileSync(headerFile,"utf8");

header = header.replace(
/<li>\s*{% set itemIsCurrent[\s\S]*?<\/li>/,
`{% set itemIsCurrent = (navCurrentUrl == item.url) or (navCurrentUrl == item.url ~ "/") or (navCurrentUrl ~ "/" == item.url) %}
{% if not itemIsCurrent %}
<li>
<a class="menu-link" href="{{ item.url }}"{% if item.external %} target="_blank" rel="noopener noreferrer"{% endif %}>{{ item.label }}</a>
</li>
{% endif %}`
);

fs.writeFileSync(headerFile,header);


/* ---------- 2. FR + PT Texte ---------- */

const navFile = "./src/_data/navigation.js";

let nav = fs.readFileSync(navFile,"utf8");

nav = nav
.replace(/Services de luxe/g,"Luxe Services")
.replace(/Serviços de luxo/g,"Luxo Serviços");

fs.writeFileSync(navFile,nav);


console.log("Menü vollständig korrigiert.");