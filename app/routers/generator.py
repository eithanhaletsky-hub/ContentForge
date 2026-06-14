import json
from fastapi import APIRouter, Request, Depends, Form
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from sqlalchemy.ext.asyncio import AsyncSession
from app.database import get_db
from app.services.auth_service import require_user
from app.services.gemini_service import generate_content
from app.services.content_service import save_content

router = APIRouter(prefix="/generate", tags=["generator"])
from pathlib import Path
templates = Jinja2Templates(directory=str(Path(__file__).resolve().parent.parent / "templates"))

CONTENT_TYPES = {
    "social_post": {"he": "פוסט לסושיאל", "en": "Social Post", "icon": "share-2"},
    "email": {"he": "אימייל שיווקי", "en": "Marketing Email", "icon": "mail"},
    "ad": {"he": "מודעה", "en": "Advertisement", "icon": "megaphone"},
    "blog": {"he": "מאמר בלוג", "en": "Blog Article", "icon": "file-text"},
    "product": {"he": "תיאור מוצר", "en": "Product Description", "icon": "shopping-bag"},
    "bio": {"he": "ביו / אודות", "en": "Bio / About", "icon": "user"},
}


@router.get("", response_class=HTMLResponse)
async def generator_page(request: Request, db: AsyncSession = Depends(get_db)):
    user = await require_user(request, db)
    lang = request.cookies.get("lang", user.language)
    content_type = request.query_params.get("type", "social_post")
    return templates.TemplateResponse("dashboard/generator.html", {
        "request": request, "user": user, "lang": lang,
        "content_type": content_type,
        "content_types": CONTENT_TYPES,
        "result": None, "error": None,
    })


@router.post("", response_class=HTMLResponse)
async def generate(
    request: Request,
    content_type: str = Form(...),
    topic: str = Form(...),
    tone: str = Form("professional"),
    audience: str = Form(""),
    platform: str = Form(""),
    details: str = Form(""),
    keywords: str = Form(""),
    email_type: str = Form(""),
    category: str = Form(""),
    db: AsyncSession = Depends(get_db),
):
    user = await require_user(request, db)
    lang = request.cookies.get("lang", user.language)

    try:
        result = await generate_content(
            content_type=content_type,
            language=lang,
            topic=topic,
            tone=tone,
            audience=audience,
            platform=platform,
            details=details,
            keywords=keywords,
            email_type=email_type,
            category=category,
        )

        prompt_data = json.dumps({
            "topic": topic, "tone": tone, "audience": audience,
            "platform": platform, "details": details,
        }, ensure_ascii=False)

        content = await save_content(
            db=db, user_id=user.id, content_type=content_type,
            title=topic[:100], prompt_data=prompt_data,
            generated_text=result, language=lang, platform=platform,
        )

        return templates.TemplateResponse("dashboard/generator.html", {
            "request": request, "user": user, "lang": lang,
            "content_type": content_type,
            "content_types": CONTENT_TYPES,
            "result": result, "content_id": content.id, "error": None,
        })
    except Exception as e:
        error_msg = str(e)
        if "429" in error_msg or "quota" in error_msg.lower() or "rate" in error_msg.lower():
            error_msg = (
                "המכסה היומית של Gemini API נוצלה. נסה שוב עוד כמה דקות, או שדרג את תוכנית ה-API שלך ב-Google AI Studio."
                if lang == "he" else
                "Gemini API quota exceeded. Please try again in a few minutes, or upgrade your API plan in Google AI Studio."
            )
        return templates.TemplateResponse("dashboard/generator.html", {
            "request": request, "user": user, "lang": lang,
            "content_type": content_type,
            "content_types": CONTENT_TYPES,
            "result": None, "error": error_msg,
        })
