from fastapi import APIRouter, Request, Depends
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.templating import Jinja2Templates
from sqlalchemy.ext.asyncio import AsyncSession
from app.database import get_db
from app.services.auth_service import require_user
from app.services.content_service import get_user_contents, get_content_by_id, delete_content

router = APIRouter(prefix="/history", tags=["history"])
from pathlib import Path
templates = Jinja2Templates(directory=str(Path(__file__).resolve().parent.parent / "templates"))


@router.get("", response_class=HTMLResponse)
async def history_page(request: Request, db: AsyncSession = Depends(get_db)):
    user = await require_user(request, db)
    lang = request.cookies.get("lang", user.language)
    contents = await get_user_contents(db, user.id)
    return templates.TemplateResponse("dashboard/history.html", {
        "request": request, "user": user, "lang": lang, "contents": contents,
    })


@router.get("/{content_id}", response_class=HTMLResponse)
async def view_content(content_id: int, request: Request, db: AsyncSession = Depends(get_db)):
    user = await require_user(request, db)
    lang = request.cookies.get("lang", user.language)
    content = await get_content_by_id(db, content_id, user.id)
    if not content:
        return RedirectResponse("/history", status_code=303)
    return templates.TemplateResponse("dashboard/view_content.html", {
        "request": request, "user": user, "lang": lang, "content": content,
    })


@router.post("/{content_id}/delete")
async def delete(content_id: int, request: Request, db: AsyncSession = Depends(get_db)):
    user = await require_user(request, db)
    await delete_content(db, content_id, user.id)
    return RedirectResponse("/history", status_code=303)
