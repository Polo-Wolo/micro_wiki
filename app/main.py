from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
from threading import Thread
import markdown
from markdown.extensions.toc import TocExtension
import markdown
import re

from .indexer import load_pages
from .watcher import start_watcher          # hot reload des notes
from .config import get_config
from .config_watcher import start_config_watcher  # hot reload config

# -------------------------
# FastAPI + templates
# -------------------------
app = FastAPI()
app.mount("/assets", StaticFiles(directory="static"), name="assets")
templates = Jinja2Templates(directory="templates")

# -------------------------
# Global state
# -------------------------
PAGES = {}
CONFIG = get_config()  # dict mutable rechargé par le watcher

# -------------------------
# Helper pour templates
# -------------------------
def ctx(request: Request, **kwargs):
    """
    Contexte commun passé à tous les templates
    """
    return {
        "request": request,
        "config": CONFIG,
        **kwargs
    }

# -------------------------
# Startup
# -------------------------
@app.on_event("startup")
def startup():
    global PAGES

    # Chargement initial des pages
    PAGES = load_pages()

    # Watcher markdown
    Thread(
        target=start_watcher,
        args=(PAGES,),
        daemon=True
    ).start()

    # Watcher config.yml
    Thread(
        target=start_config_watcher,
        daemon=True
    ).start()

# -------------------------
# Routes
# -------------------------

@app.get("/", response_class=HTMLResponse)
def index(request: Request):
    sections = {}

    for page in PAGES.values():
        sections.setdefault(page.section, []).append(page)

    # tri des sections
    sections = dict(sorted(sections.items(), key=lambda x: x[0].lower()))

    # tri des pages dans chaque section
    for pages in sections.values():
        pages.sort(key=lambda p: p.title.lower())

    return templates.TemplateResponse(
        "home.html",
        ctx(
            request,
            sections=sections,
            title=CONFIG["site"].get("name", "Wiki")
        )
    )

@app.get("/page/{slug}", response_class=HTMLResponse)
def page(slug: str, request: Request):
    page = PAGES.get(slug)
    if not page:
        return HTMLResponse("Page introuvable", status_code=404)

    # Markdown avec TOC
    md = markdown.Markdown(
        extensions=[
            "fenced_code",
            "tables",
            TocExtension(anchorlink=True)
        ]
    )

    html = md.convert(page.content)

    # TOC générée par l'extension
    toc = getattr(md, "toc_tokens", None)

    return templates.TemplateResponse(
        "page.html",
        ctx(
            request,
            page=page,
            html=html,
            toc=toc,
            title=page.title
        )
    )


@app.get("/tags", response_class=HTMLResponse)
def tags(request: Request):
    """
    Liste de tous les tags
    """
    tag_map = {}

    for page in PAGES.values():
        for tag in page.tags:
            tag_map.setdefault(tag, []).append(page)

    tags = sorted(tag_map.items())

    return templates.TemplateResponse(
        "tags.html",
        ctx(
            request,
            tags=tags,
            title="Tags"
        )
    )


@app.get("/portfolio", response_class=HTMLResponse)
def portfolio(request: Request):
    """
    Page portfolio (statique pour l’instant)
    """
    return templates.TemplateResponse(
        "portfolio.html",
        ctx(
            request,
            title="Portfolio"
        )
    )

@app.get("/search", response_class=HTMLResponse)
def search(request: Request, q: str | None = None):
    results = []

    if q:
        query = q.lower()

        for page in PAGES.values():
            score = 0

            if query in page.title.lower():
                score += 3

            if query in page.content.lower():
                score += 1

            if score > 0:
                results.append((score, page))

        results.sort(key=lambda x: x[0], reverse=True)
        results = [p for _, p in results]

    return templates.TemplateResponse(
        "search.html",
        ctx(
            request,
            query=q,
            results=results,
            title="Recherche"
        )
    )

@app.get("/tags/{tag}", response_class=HTMLResponse)
def by_tag(tag: str, request: Request):
    # Filtrer les pages qui contiennent ce tag
    pages = [p for p in PAGES.values() if tag in p.tags]

    # Passer le tag et les pages au template
    return templates.TemplateResponse(
        "tag.html",
        ctx(
            request,
            tag=tag,
            pages=pages,
            title=f'Pages taggée(s) "{tag}"'
        )
    )
