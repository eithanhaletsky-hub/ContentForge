from fastapi import APIRouter, Request, Depends, Form
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.templating import Jinja2Templates
from sqlalchemy.ext.asyncio import AsyncSession
from app.database import get_db
from app.services.auth_service import require_user

router = APIRouter(prefix="/profile", tags=["profile"])
from pathlib import Path
templates = Jinja2Templates(directory=str(Path(__file__).resolve().parent.parent / "templates"))


@router.get("", response_class=HTMLResponse)
async def profile_page(request: Request, db: AsyncSession = Depends(get_db)):
    user = await require_user(request, db)
    lang = request.cookies.get("lang", user.language)
    return templates.TemplateResponse("dashboard/profile.html", {
        "request": request, "user": user, "lang": lang, "success": None,
    })


@router.post("", response_class=HTMLResponse)
async def update_profile(
    request: Request,
    name: str = Form(...),
    business_name: str = Form(""),
    business_description: str = Form(""),
    db: AsyncSession = Depends(get_db),
):
    user = await require_user(request, db)
    lang = request.cookies.get("lang", user.language)
    user.name = name
    user.business_name = business_name
    user.business_description = business_description
    await db.commit()
    return templates.TemplateResponse("dashboard/profile.html", {
        "request": request, "user": user, "lang": lang,
        "success": "הפרופיל עודכן בהצלחה" if lang == "he" else "Profile updated successfully",
    })
