const fs = require("fs");

const header = "./src/_includes/components/header.njk";
const siteData = "./src/_data/site.js";

/* 1. Hamburger Menü korrigieren */

let headerContent = fs.readFileSync(header, "utf8");

headerContent = headerContent.replace(
`<li>
              {% set itemIsCurrent = (navCurrentUrl == item.url) or (navCurrentUrl == item.url ~ "/") or (navCurrentUrl ~ "/" == item.url) %}
              <a class="menu-link{% if itemIsCurrent %} is-current{% endif %}" href="{{ item.url }}"{% if item.external %} target="_blank" rel="noopener noreferrer"{% endif %}{% if itemIsCurrent and not item.external %} aria-current="page"{% endif %}>{{ item.label }}</a>
            </li>`,
`{% set itemIsCurrent = (navCurrentUrl == item.url) or (navCurrentUrl == item.url ~ "/") or (navCurrentUrl ~ "/" == item.url) %}
{% if not itemIsCurrent %}
<li>
  <a class="menu-link" href="{{ item.url }}"{% if item.external %} target="_blank" rel="noopener noreferrer"{% endif %}>{{ item.label }}</a>
</li>
{% endif %}`
);

fs.writeFileSync(header, headerContent);


/* 2. FR + PT Menütexte korrigieren */

let siteContent = fs.readFileSync(siteData, "utf8");

siteContent = siteContent
.replace("Services Luxe", "Luxe Services")
.replace("Serviços de Luxo", "Luxo Serviços");

fs.writeFileSync(siteData, siteContent);

console.log("Hamburger Menü + FR/PT Texte korrigiert.");