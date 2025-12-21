import shutil
from pathlib import Path
import markdown
from jinja2 import Environment, FileSystemLoader

from app.indexer import load_pages, render_wikilinks
from app.config import get_config

# -------------------------
# Configuration
# -------------------------
OUTPUT_DIR = Path("dist")
PAGES_DIR = OUTPUT_DIR / "page"
ASSETS_DIR = OUTPUT_DIR / "assets"

CONFIG = get_config()
env = Environment(loader=FileSystemLoader("templates"))

# -------------------------
# Nettoyer et recréer dist
# -------------------------
if OUTPUT_DIR.exists():
    shutil.rmtree(OUTPUT_DIR)

OUTPUT_DIR.mkdir(parents=True)
PAGES_DIR.mkdir(parents=True)
ASSETS_DIR.mkdir(parents=True)

# Copier les fichiers statiques
shutil.copytree("static", ASSETS_DIR, dirs_exist_ok=True)

# -------------------------
# Charger les pages
# -------------------------
PAGES = load_pages()

# -------------------------
# Générer les pages individuelles
# -------------------------
page_template = env.get_template("page.html")

for page in PAGES.values():
    html_content = markdown.markdown(
        render_wikilinks(page.content),
        extensions=["fenced_code", "tables"]
    )

    out_path = PAGES_DIR / f"{page.slug}.html"

    with open(out_path, "w", encoding="utf-8") as f:
        f.write(
            page_template.render(
                page=page,
                html=html_content,
                backlinks=[PAGES[s] for s in page.backlinks],
                config=CONFIG,
                title=page.title,
                # pour les liens relatifs
                base_url="../"
            )
        )

# -------------------------
# Générer la page d'accueil (sections)
# -------------------------
home_template = env.get_template("home.html")

sections = {}
for page in PAGES.values():
    sections.setdefault(page.section, []).append(page)

sections = dict(sorted(sections.items(), key=lambda x: x[0].lower()))
for pages in sections.values():
    pages.sort(key=lambda p: p.title.lower())

with open(OUTPUT_DIR / "index.html", "w", encoding="utf-8") as f:
    f.write(home_template.render(
        sections=sections,
        config=CONFIG,
        title=CONFIG["site"].get("name", "Wiki"),
        base_url=""  # la racine
    ))

# -------------------------
# Générer les pages par tag
# -------------------------
tags_template = env.get_template("index.html")

tags = {}
for page in PAGES.values():
    for tag in page.tags:
        tags.setdefault(tag, []).append(page)

for tag, pages in tags.items():
    out_path = OUTPUT_DIR / f"tag_{tag}.html"
    with open(out_path, "w", encoding="utf-8") as f:
        f.write(tags_template.render
                (
            pages=pages,
            config=CONFIG,
            title=f"Tag: {tag}",
            base_url=""  # à la racine
        ))

print(f"✅ Site statique prêt dans {OUTPUT_DIR.resolve()}")
