import os
from pathlib import Path
from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from contextlib import asynccontextmanager
from app.database import init_db
from app.routers import auth, dashboard, generator, history, profile
from app.services.auth_service import get_current_user
from app.database import get_db

BASE_DIR = Path(__file__).resolve().parent
TEMPLATES_DIR = str(BASE_DIR / "templates")
STATIC_DIR = str(BASE_DIR / "static")


@asynccontextmanager
async def lifespan(app: FastAPI):
    os.chdir(BASE_DIR.parent)
    await init_db()
    yield


app = FastAPI(title="ContentForge", lifespan=lifespan)
app.mount("/static", StaticFiles(directory=STATIC_DIR), name="static")

app.include_router(auth.router)
app.include_router(dashboard.router)
app.include_router(generator.router)
app.include_router(history.router)
app.include_router(profile.router)

templates = Jinja2Templates(directory=TEMPLATES_DIR)


@app.get("/", response_class=HTMLResponse)
async def landing(request: Request):
    async for db in get_db():
        user = await get_current_user(request, db)
        break
    lang = request.cookies.get("lang", "he")
    return templates.TemplateResponse("landing.html", {
        "request": request, "user": user, "lang": lang,
    })


@app.get("/set-lang/{lang}")
async def set_language(lang: str, request: Request):
    if lang not in ("he", "en"):
        lang = "he"
    referer = request.headers.get("referer", "/")
    response = RedirectResponse(referer, status_code=303)
    response.set_cookie("lang", lang, max_age=60 * 60 * 24 * 365)
    return response
