module.exports = function (eleventyConfig) {

  // Assets kopieren
  eleventyConfig.addPassthroughCopy("src/assets");

  // Root deploy files
  eleventyConfig.addPassthroughCopy("src/robots.txt");
  eleventyConfig.addPassthroughCopy("src/.htaccess");
  eleventyConfig.addPassthroughCopy("src/oldhtaccess");
  eleventyConfig.addPassthroughCopy("src/favicon.ico");
  eleventyConfig.addPassthroughCopy("src/favicon.svg");
  eleventyConfig.addPassthroughCopy("src/favicon-96x96.png");
  eleventyConfig.addPassthroughCopy("src/apple-touch-icon.png");
  eleventyConfig.addPassthroughCopy("src/site.webmanifest");
  eleventyConfig.addPassthroughCopy("src/web-app-manifest-192x192.png");
  eleventyConfig.addPassthroughCopy("src/web-app-manifest-512x512.png");

  // Falls vorhanden: PHP mit ausgeben
  eleventyConfig.addPassthroughCopy("src/send.php");

  // Nunjucks Whitespace reduzieren
  eleventyConfig.setNunjucksEnvironmentOptions({
    trimBlocks: true,
    lstripBlocks: true
  });

  // HTML whitespace reduzieren (große Leerzeilen im Output)
  eleventyConfig.addTransform("htmlClean", function(content, outputPath) {
    if(outputPath && outputPath.endsWith(".html")) {
      // remove trailing spaces per line
      content = content.replace(/[ \t]+\n/g, "\n");
      // collapse many blank lines
      content = content.replace(/\n{3,}/g, "\n\n");
    }
    return content;
  });


  return {
    dir: {
  input: "src",
  layouts: "layouts",
  includes: "_includes",
  data: "_data",
  output: "_site"
}
  };
};
