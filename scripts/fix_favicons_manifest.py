from __future__ import annotations

import json
import os
import re
import shutil
import subprocess
import sys
from pathlib import Path


def find_project_root(start: Path) -> Path:
    current = start.resolve()
    for candidate in [current, *current.parents]:
        if (candidate / "src" / "layouts" / "base.njk").exists() and (candidate / "src" / "assets" / "favicons").exists():
            return candidate
    raise FileNotFoundError(
        "Projektwurzel nicht gefunden. Starte das Script im Projektordner oder in einem Unterordner davon."
    )


def write_text(path: Path, content: str) -> None:
    path.write_text(content, encoding="utf-8", newline="\n")


def read_text(path: Path) -> str:
    return path.read_text(encoding="utf-8")


def ensure_dir(path: Path) -> None:
    path.mkdir(parents=True, exist_ok=True)


def copy_file(src: Path, dst: Path) -> None:
    if not src.exists():
        raise FileNotFoundError(f"Quelldatei fehlt: {src}")
    shutil.copyfile(src, dst)


def try_create_512_with_cairosvg(svg_path: Path, out_path: Path) -> bool:
    try:
        import cairosvg  # type: ignore
    except Exception:
        return False

    try:
        cairosvg.svg2png(url=str(svg_path), write_to=str(out_path), output_width=512, output_height=512)
        return out_path.exists() and out_path.stat().st_size > 0
    except Exception:
        return False


def try_create_512_with_pillow(source_png: Path, out_path: Path) -> bool:
    try:
        from PIL import Image  # type: ignore
    except Exception:
        return False

    try:
        with Image.open(source_png) as img:
            img = img.convert("RGBA")
            img = img.resize((512, 512), Image.LANCZOS)
            img.save(out_path, format="PNG")
        return out_path.exists() and out_path.stat().st_size > 0
    except Exception:
        return False


def try_create_512_with_powershell(source_png: Path, out_path: Path) -> bool:
    if os.name != "nt":
        return False

    ps_script = rf"""
Add-Type -AssemblyName System.Drawing
$src = "{str(source_png)}"
$dst = "{str(out_path)}"

$img = [System.Drawing.Image]::FromFile($src)
try {{
    $bmp = New-Object System.Drawing.Bitmap 512, 512
    try {{
        $g = [System.Drawing.Graphics]::FromImage($bmp)
        try {{
            $g.InterpolationMode = [System.Drawing.Drawing2D.InterpolationMode]::HighQualityBicubic
            $g.SmoothingMode = [System.Drawing.Drawing2D.SmoothingMode]::HighQuality
            $g.PixelOffsetMode = [System.Drawing.Drawing2D.PixelOffsetMode]::HighQuality
            $g.Clear([System.Drawing.Color]::Transparent)
            $g.DrawImage($img, 0, 0, 512, 512)
            $bmp.Save($dst, [System.Drawing.Imaging.ImageFormat]::Png)
        }}
        finally {{
            $g.Dispose()
        }}
    }}
    finally {{
        $bmp.Dispose()
    }}
}}
finally {{
    $img.Dispose()
}}
"""
    try:
        subprocess.run(
            ["powershell", "-NoProfile", "-ExecutionPolicy", "Bypass", "-Command", ps_script],
            check=True,
            capture_output=True,
            text=True,
        )
        return out_path.exists() and out_path.stat().st_size > 0
    except Exception:
        return False


def create_missing_manifest_icons(favicons_dir: Path) -> None:
    icon_192_target = favicons_dir / "web-app-manifest-192x192.png"
    icon_512_target = favicons_dir / "web-app-manifest-512x512.png"

    source_192 = favicons_dir / "android-icon-192x192.png"
    source_256 = favicons_dir / "favicon-256x256.png"
    source_svg = favicons_dir / "favicon.svg"

    if not source_192.exists():
        raise FileNotFoundError(
            "android-icon-192x192.png fehlt. Ohne diese Datei kann das 192er Manifest-Icon nicht erzeugt werden."
        )

    copy_file(source_192, icon_192_target)

    created_512 = False

    if source_svg.exists():
        created_512 = try_create_512_with_cairosvg(source_svg, icon_512_target)

    if not created_512 and source_256.exists():
        created_512 = try_create_512_with_pillow(source_256, icon_512_target)

    if not created_512 and source_256.exists():
        created_512 = try_create_512_with_powershell(source_256, icon_512_target)

    if not created_512:
        raise RuntimeError(
            "512x512 Icon konnte nicht erzeugt werden. "
            "Installiere entweder cairosvg oder pillow, oder stelle sicher, dass powershell auf Windows verfügbar ist."
        )


def update_manifest(manifest_path: Path) -> None:
    manifest = {
        "name": "Anjo Property Care Madeira",
        "short_name": "Anjo",
        "description": "Property care and premium cleaning services for luxury villas and apartments on Madeira.",
        "start_url": "/",
        "scope": "/",
        "display": "standalone",
        "background_color": "#ffffff",
        "theme_color": "#001f3f",
        "icons": [
            {
                "src": "/assets/favicons/web-app-manifest-192x192.png",
                "sizes": "192x192",
                "type": "image/png",
                "purpose": "any",
            },
            {
                "src": "/assets/favicons/web-app-manifest-512x512.png",
                "sizes": "512x512",
                "type": "image/png",
                "purpose": "any",
            },
        ],
    }
    write_text(manifest_path, json.dumps(manifest, ensure_ascii=False, indent=2) + "\n")


def update_base_njk(base_path: Path) -> None:
    content = read_text(base_path)

    new_block = """  <!-- Favicons -->
  <link rel="icon" type="image/svg+xml" href="/assets/favicons/favicon.svg">
  <link rel="icon" type="image/png" sizes="32x32" href="/assets/favicons/favicon-32x32.png">
  <link rel="icon" type="image/png" sizes="96x96" href="/assets/favicons/favicon-96x96.png">
  <link rel="icon" type="image/png" sizes="192x192" href="/assets/favicons/web-app-manifest-192x192.png">
  <link rel="apple-touch-icon" sizes="180x180" href="/assets/favicons/apple-icon-180x180.png">
  <link rel="manifest" href="/assets/favicons/site.webmanifest">
  <meta name="theme-color" content="#001f3f">"""

    pattern = re.compile(
        r"""[ \t]*<!-- Favicons -->.*?[ \t]*<meta name="theme-color" content="#001f3f">""",
        re.DOTALL,
    )

    if not pattern.search(content):
        raise RuntimeError(
            "Favicon-Block in src/layouts/base.njk nicht gefunden. Script bricht ab, damit nichts versehentlich beschädigt wird."
        )

    updated = pattern.sub(new_block, content, count=1)

    if updated == content:
        raise RuntimeError("src/layouts/base.njk wurde nicht geändert.")

    write_text(base_path, updated)


def main() -> None:
    root = find_project_root(Path.cwd())
    favicons_dir = root / "src" / "assets" / "favicons"
    manifest_path = favicons_dir / "site.webmanifest"
    base_path = root / "src" / "layouts" / "base.njk"

    ensure_dir(favicons_dir)

    create_missing_manifest_icons(favicons_dir)
    update_manifest(manifest_path)
    update_base_njk(base_path)

    print("OK: Favicon-/Manifest-Fix abgeschlossen.")
    print(f"- Projekt: {root}")
    print(f"- Aktualisiert: {manifest_path}")
    print(f"- Aktualisiert: {base_path}")
    print(f"- Erzeugt/überschrieben: {favicons_dir / 'web-app-manifest-192x192.png'}")
    print(f"- Erzeugt/überschrieben: {favicons_dir / 'web-app-manifest-512x512.png'}")


if __name__ == "__main__":
    try:
        main()
    except Exception as exc:
        print(f"FEHLER: {exc}", file=sys.stderr)
        sys.exit(1)