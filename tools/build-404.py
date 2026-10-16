#!/usr/bin/env python3
"""Generate 404.html from index.html.

The 404 page reuses the site's stylesheet, masthead and footer. Copying them by
hand means they drift the moment index.html changes -- which happened within an
hour the first time -- so they are lifted out of index.html every build instead.
Only the Route 404 body, its own styles and its own script live here.

    python3 tools/build-404.py
"""
import pathlib
import re
import sys

HERE = pathlib.Path(__file__).resolve().parent.parent
INDEX = HERE / "index.html"
OUT = HERE / "404.html"
EXTRA_CSS = pathlib.Path(sys.argv[1]) if len(sys.argv) > 1 else HERE / "tools" / "404.css"
EXTRA_JS = pathlib.Path(sys.argv[2]) if len(sys.argv) > 2 else HERE / "tools" / "404.js"

src = INDEX.read_text()

style = src[src.index("<style>"): src.index("</style>") + len("</style>")]

ms = src.index('<header class="mast">')
mast = src[ms: src.index("</header>", ms) + len("</header>")]
# in-page anchors have to become absolute, or they do nothing from a 404 URL
for a, b in (('href="#top"', 'href="/"'), ('href="#features"', 'href="/#features"'),
             ('href="#badges"', 'href="/#badges"'), ('href="#start"', 'href="/#start"')):
    mast = mast.replace(a, b)

fs = src.index('<footer class="footer">')
footer = src[fs: src.index("</footer>", fs) + len("</footer>")].replace('href="#top"', 'href="/"')

fonts = "\n".join(l for l in src.split("\n")
                  if "fonts.googleapis.com" in l or "fonts.gstatic.com" in l)

BODY = """
<main class="r404">
  <div class="r404-stack">
    <p class="r404-word">ROUTE</p>
    <p class="r404-big">404</p>
  </div>
  <div class="r404-box">
    <p>There&rsquo;s nothing this way.</p>
    <p>The page you were after isn&rsquo;t here. It may have moved, or the link may be wrong.</p>
    <span class="r404-more">&#9660;</span>
  </div>
  <div class="r404-cta">
    <a class="btn btn-primary" href="/">Back to town</a>
    <a class="btn btn-ghost" href="https://github.com/techykamatis/pokemon-agents" target="_blank" rel="noopener">View on GitHub</a>
  </div>
</main>
"""

page = f"""<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8" />
<meta name="viewport" content="width=device-width, initial-scale=1.0" />
<title>Route 404 &middot; Pok&eacute;mon Agents</title>
<meta name="robots" content="noindex" />
<meta name="description" content="There is nothing this way. Head back to the town." />
{fonts}
{style}
{EXTRA_CSS.read_text().rstrip()}
</head>
<body>
{mast}
{BODY}
{footer}
{EXTRA_JS.read_text().rstrip()}
</body>
</html>
"""
OUT.write_text(page)
print(f"wrote {OUT.name} ({len(page)} bytes) from {INDEX.name}")
