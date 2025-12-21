import re
import yaml
from pathlib import Path

from .config import get_config

CONFIG = get_config()
NOTES_DIR: Path = CONFIG["paths"]["notes"]

class Page:
    def __init__(self, title, slug, content, tags, section):
        self.title = title
        self.slug = slug
        self.content = content
        self.tags = tags
        self.section = section
        self.links = []
        self.backlinks = []


def slugify(text: str) -> str:
    return text.lower().replace(" ", "-")

def render_wikilinks(text: str) -> str:
    def repl(match):
        label = match.group(1)
        slug = slugify(label)
        return f'<a href="/page/{slug}">{label}</a>'
    return re.sub(r"\[\[([^\]]+)\]\]", repl, text)

def load_pages():
    pages = {}

    for path in Path(NOTES_DIR).glob("*.md"):
        with open(path, encoding="utf-8") as f:
            text = f.read()

        meta = {}
        content = text

        if text.startswith("---"):
            try:
                _, fm, content = text.split("---", 2)
                meta = yaml.safe_load(fm) or {}
            except ValueError:
                pass

        title = meta.get("title", path.stem)
        tags = meta.get("tags", [])
        section = meta.get("section", "Divers")

        slug = slugify(title)

        page = Page(
            title=title,
            slug=slug,
            content=content.strip(),
            tags=tags,
            section=section
        )

        pages[slug] = page

    # 2) Extraire wikilinks + backlinks
    for page in pages.values():
        links = re.findall(r"\[\[([^\]]+)\]\]", page.content)
        for label in links:
            dst = pages.get(slugify(label))
            if dst:
                page.links.append(dst.slug)
                dst.backlinks.append(page.slug)

    return pages
