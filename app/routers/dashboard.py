from fastapi import APIRouter, Request, Depends
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, func
from app.database import get_db
from app.models.user import User
from app.models.content import GeneratedContent
from app.services.auth_service import require_user

router = APIRouter(prefix="/dashboard", tags=["dashboard"])
from pathlib import Path
templates = Jinja2Templates(directory=str(Path(__file__).resolve().parent.parent / "templates"))


@router.get("", response_class=HTMLResponse)
async def dashboard(request: Request, db: AsyncSession = Depends(get_db)):
    user = await require_user(request, db)
    lang = request.cookies.get("lang", user.language)

    total_result = await db.execute(
        select(func.count(GeneratedContent.id)).where(GeneratedContent.user_id == user.id)
    )
    total_contents = total_result.scalar() or 0

    recent_result = await db.execute(
        select(GeneratedContent)
        .where(GeneratedContent.user_id == user.id)
        .order_by(GeneratedContent.created_at.desc())
        .limit(5)
    )
    recent_contents = recent_result.scalars().all()

    type_counts = {}
    for ctype in ["social_post", "email", "ad", "blog", "product", "bio"]:
        r = await db.execute(
            select(func.count(GeneratedContent.id))
            .where(GeneratedContent.user_id == user.id, GeneratedContent.content_type == ctype)
        )
        type_counts[ctype] = r.scalar() or 0

    return templates.TemplateResponse("dashboard/index.html", {
        "request": request, "user": user, "lang": lang,
        "total_contents": total_contents,
        "recent_contents": recent_contents,
        "type_counts": type_counts,
    })
