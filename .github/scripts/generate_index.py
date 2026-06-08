#!/usr/bin/env python3
import re
from pathlib import Path

SLIDES_DIR = Path("slides")
OUTPUT = Path("index.html")


def parse_frontmatter(md_path):
    content = md_path.read_text(encoding="utf-8")
    match = re.match(r"^---\n(.*?)\n---", content, re.DOTALL)
    if not match:
        return {}
    result = {}
    for line in match.group(1).splitlines():
        if ":" in line:
            key, _, value = line.partition(":")
            result[key.strip()] = value.strip()
    return result


def collect_slides():
    slides = []
    for folder in sorted(SLIDES_DIR.iterdir(), reverse=True):
        if not folder.is_dir() or folder.name.startswith("_"):
            continue
        md = folder / "slides.md"
        if not md.exists():
            continue
        meta = parse_frontmatter(md)
        slides.append(
            {
                "folder": folder.name,
                "title": meta.get("title", folder.name),
                "date": meta.get("date", ""),
                "description": meta.get("description", ""),
            }
        )
    return slides


def render_card(slide):
    date_html = f'<span class="date">{slide["date"]}</span>' if slide["date"] else ""
    desc_html = f'<p class="desc">{slide["description"]}</p>' if slide["description"] else ""
    return f"""    <a class="card" href="slides/{slide['folder']}/index.html">
      <div class="card-body">
        {date_html}
        <h2>{slide['title']}</h2>
        {desc_html}
      </div>
    </a>"""


def generate_html(slides):
    cards = "\n".join(render_card(s) for s in slides)
    count = len(slides)
    return f"""<!doctype html>
<html lang="zh-TW">
  <head>
    <meta charset="utf-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>簡報列表</title>
    <style>
      *, *::before, *::after {{ box-sizing: border-box; margin: 0; padding: 0; }}

      body {{
        font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", sans-serif;
        background: #0d1117;
        color: #e6edf3;
        min-height: 100vh;
        padding: 3rem 1.5rem;
      }}

      header {{
        max-width: 800px;
        margin: 0 auto 3rem;
      }}

      header h1 {{ font-size: 2rem; font-weight: 700; }}

      header p {{
        margin-top: 0.5rem;
        color: #8b949e;
        font-size: 0.95rem;
      }}

      .grid {{
        max-width: 800px;
        margin: 0 auto;
        display: grid;
        gap: 1rem;
      }}

      .card {{
        display: block;
        background: #161b22;
        border: 1px solid #30363d;
        border-radius: 8px;
        padding: 1.25rem 1.5rem;
        text-decoration: none;
        color: inherit;
        transition: border-color 0.15s, background 0.15s;
      }}

      .card:hover {{
        border-color: #58a6ff;
        background: #1c2128;
      }}

      .date {{
        font-size: 0.8rem;
        color: #8b949e;
        display: block;
        margin-bottom: 0.35rem;
      }}

      .card h2 {{
        font-size: 1.1rem;
        font-weight: 600;
        color: #58a6ff;
      }}

      .desc {{
        margin-top: 0.4rem;
        font-size: 0.88rem;
        color: #8b949e;
        line-height: 1.5;
      }}

      footer {{
        max-width: 800px;
        margin: 3rem auto 0;
        font-size: 0.8rem;
        color: #484f58;
      }}
    </style>
  </head>
  <body>
    <header>
      <h1>簡報列表</h1>
      <p>共 {count} 份簡報</p>
    </header>
    <div class="grid">
{cards}
    </div>
    <footer>由 GitHub Actions 自動產生</footer>
  </body>
</html>
"""


def main():
    slides = collect_slides()
    html = generate_html(slides)
    OUTPUT.write_text(html, encoding="utf-8")
    print(f"Generated {OUTPUT} with {len(slides)} slides.")


if __name__ == "__main__":
    main()
