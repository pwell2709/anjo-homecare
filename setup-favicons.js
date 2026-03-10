const fs = require("fs");
const path = require("path");

const PROJECT = "./src/assets/favicons";
const SOURCE = "C:\Users\pwell\Downloads\06ad2fd4529ae1b4a15e44886c611f23";

const ICONS = [
"android-icon-192x192.png",
"apple-icon-57x57.png",
"apple-icon-60x60.png",
"apple-icon-72x72.png",
"apple-icon-76x76.png",
"apple-icon-114x114.png",
"apple-icon-120x120.png",
"apple-icon-144x144.png",
"apple-icon-152x152.png",
"apple-icon-180x180.png",
"favicon-16x16.png",
"favicon-32x32.png",
"favicon-96x96.png",
"favicon-256x256.png",
"ms-icon-70x70.png",
"ms-icon-144x144.png",
"ms-icon-150x150.png",
"ms-icon-310x310.png"
];

const HEAD_FILES = [
"./src/_includes/base.njk",
"./src/_includes/head.njk"
];

const faviconBlock = `
<link rel="icon" sizes="32x32" href="/assets/favicons/favicon-32x32.png">
<link rel="icon" sizes="16x16" href="/assets/favicons/favicon-16x16.png">
<link rel="icon" sizes="96x96" href="/assets/favicons/favicon-96x96.png">
<link rel="icon" sizes="256x256" href="/assets/favicons/favicon-256x256.png">

<link rel="apple-touch-icon" sizes="180x180" href="/assets/favicons/apple-icon-180x180.png">

<link rel="manifest" href="/assets/favicons/site.webmanifest">

<meta name="theme-color" content="#ffffff">
`;

function ensureDir() {
if (!fs.existsSync(PROJECT)) {
fs.mkdirSync(PROJECT, { recursive: true });
}
}

function copyIcons() {
ICONS.forEach(icon => {
const src = path.join(SOURCE, icon);
const dst = path.join(PROJECT, icon);

if (fs.existsSync(src)) {
fs.copyFileSync(src, dst);
console.log("kopiert:", icon);
}
});
}

function createManifest() {
const manifest = {
name: "Anjo Luxury Property Care Madeira",
short_name: "Anjo",
icons: [
{
src: "/assets/favicons/android-icon-192x192.png",
sizes: "192x192",
type: "image/png"
},
{
src: "/assets/favicons/favicon-256x256.png",
sizes: "256x256",
type: "image/png"
}
],
theme_color: "#ffffff",
background_color: "#ffffff",
display: "standalone"
};

fs.writeFileSync(
path.join(PROJECT, "site.webmanifest"),
JSON.stringify(manifest, null, 2)
);
}

function injectHead() {
HEAD_FILES.forEach(file => {

if (!fs.existsSync(file)) return;

let content = fs.readFileSync(file, "utf8");

if (content.includes("favicons")) return;

content = content.replace("</head>", faviconBlock + "\n</head>");

fs.writeFileSync(file, content);
});
}

ensureDir();
copyIcons();
createManifest();
injectHead();

console.log("Favicons komplett installiert.");