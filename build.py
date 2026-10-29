#!/usr/bin/env python3
"""Build the Mark A Dream website from src/template.html.

Outputs
  index.html                 the site GitHub Pages serves (images from assets/img/)
  404.html                   sends unknown paths back to the site
  dist/MarkADream-site.html  one self-contained file with images embedded

Usage:  python3 build.py
"""
import base64, hashlib, pathlib

ROOT = pathlib.Path(__file__).resolve().parent
IMG = ROOT / "assets" / "img"
BLANK = "data:image/gif;base64,R0lGODlhAQABAIAAAAAAAP///yH5BAEAAAAALAAAAAABAAEAAAIBRAA7"
KEYS = {"%%LOGO%%": "logo", "%%MARKSM%%": "mark-sm", "%%ADAM%%": "adam", "%%MARK%%": "mark"}


def wrap(body: str) -> str:
    end = body.index("</style>") + len("</style>")
    return (
        '<!doctype html>\n<html lang="en">\n<head>\n<meta charset="utf-8">\n'
        '<meta name="viewport" content="width=device-width, initial-scale=1, viewport-fit=cover">\n'
        "<style>:root{padding-top:env(safe-area-inset-top,0px);padding-bottom:env(safe-area-inset-bottom,0px)}"
        "body{margin:0}[hidden]{display:none!important}</style>\n"
        + body[:end] + "\n</head>\n<body>\n" + body[end:] + "\n</body>\n</html>\n"
    )


def data_uri(name: str) -> str:
    return "data:image/webp;base64," + base64.b64encode((IMG / f"{name}.webp").read_bytes()).decode()


def main() -> None:
    src = (ROOT / "src" / "template.html").read_text(encoding="utf-8")

    # 1) Hosted site: images load from assets/img/
    site = src
    for key, name in KEYS.items():
        # version each image by content so browsers fetch a new file whenever it changes
        ver = hashlib.md5((IMG / f"{name}.webp").read_bytes()).hexdigest()[:8]
        site = site.replace(key, f"assets/img/{name}.webp?v={ver}")
    (ROOT / "index.html").write_text(wrap(site), encoding="utf-8")

    # 2) Single self-contained file: images embedded once, attached at load
    one = src.replace('<link rel="icon" href="%%MARKSM%%">', f'<link rel="icon" href="{data_uri("mark-sm")}">')
    for key, name in KEYS.items():
        one = one.replace(f'src="{key}"', f'src="{BLANK}" data-img="{name}"')
    imgs = ",".join(f'"{n}":"{data_uri(n)}"' for n in KEYS.values())
    one = one.replace(
        'const MARK="%%MARK%%";',
        "const IMG={" + imgs + "};\nconst MARK=IMG.mark;\n"
        'document.querySelectorAll("img[data-img]").forEach(i=>i.src=IMG[i.dataset.img]);',
    )
    assert "%%" not in one and "%%" not in site, "unreplaced placeholder"
    (ROOT / "dist").mkdir(exist_ok=True)
    (ROOT / "dist" / "MarkADream-site.html").write_text(wrap(one), encoding="utf-8")

    # 3) 404 page: send old markadream.com paths (from the previous site) to their new sections
    (ROOT / "404.html").write_text("""<!doctype html><html lang="en"><head><meta charset="utf-8"><title>Mark A Dream</title>
<meta name="viewport" content="width=device-width, initial-scale=1">
<script>
(function(){
  var map={"company/about":"about","company/mission":"about","company/values":"about","portfolio":"portfolio","impact":"impact",
    "insights":"insights","contact":"contact","opportunities":"founders","strategy":"strategy"};
  var p=location.pathname.replace(/^\/(markadream-website\/)?/,"").replace(/\/+$/,"").toLowerCase();
  var base=location.pathname.indexOf("/markadream-website/")===0?"/markadream-website/":"/";
  var h=map[p]||(p.indexOf("strategy/")===0?"strategy-"+p.slice(9):"notfound");
  location.replace(base+"#"+h);
})();
</script></head><body><p><a href="/">Go to Mark A Dream</a></p></body></html>
""", encoding="utf-8")
    print("Built index.html, 404.html, dist/MarkADream-site.html")


if __name__ == "__main__":
    main()
