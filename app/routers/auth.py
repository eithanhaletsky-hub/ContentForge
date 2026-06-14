from fastapi import APIRouter, Request, Depends, Form
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.templating import Jinja2Templates
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from app.database import get_db
from app.models.user import User
from app.services.auth_service import (
    hash_password, verify_password, create_access_token, get_current_user,
)

router = APIRouter(prefix="/auth", tags=["auth"])
from pathlib import Path
templates = Jinja2Templates(directory=str(Path(__file__).resolve().parent.parent / "templates"))


@router.get("/register", response_class=HTMLResponse)
async def register_page(request: Request, db: AsyncSession = Depends(get_db)):
    user = await get_current_user(request, db)
    if user:
        return RedirectResponse("/dashboard", status_code=303)
    return templates.TemplateResponse("auth/register.html", {
        "request": request, "error": None, "lang": request.cookies.get("lang", "he"),
    })


@router.post("/register", response_class=HTMLResponse)
async def register(
    request: Request,
    name: str = Form(...),
    email: str = Form(...),
    password: str = Form(...),
    db: AsyncSession = Depends(get_db),
):
    lang = request.cookies.get("lang", "he")
    result = await db.execute(select(User).where(User.email == email))
    if result.scalar_one_or_none():
        return templates.TemplateResponse("auth/register.html", {
            "request": request, "lang": lang,
            "error": "האימייל כבר רשום במערכת" if lang == "he" else "Email already registered",
        })

    if len(password) < 6:
        return templates.TemplateResponse("auth/register.html", {
            "request": request, "lang": lang,
            "error": "הסיסמה חייבת להכיל לפחות 6 תווים" if lang == "he" else "Password must be at least 6 characters",
        })

    user = User(name=name, email=email, hashed_password=hash_password(password), language=lang)
    db.add(user)
    await db.commit()
    await db.refresh(user)

    token = create_access_token(user.id)
    response = RedirectResponse("/dashboard", status_code=303)
    response.set_cookie("access_token", token, httponly=True, max_age=60 * 60 * 24 * 7, samesite="lax")
    return response


@router.get("/login", response_class=HTMLResponse)
async def login_page(request: Request, db: AsyncSession = Depends(get_db)):
    user = await get_current_user(request, db)
    if user:
        return RedirectResponse("/dashboard", status_code=303)
    return templates.TemplateResponse("auth/login.html", {
        "request": request, "error": None, "lang": request.cookies.get("lang", "he"),
    })


@router.post("/login", response_class=HTMLResponse)
async def login(
    request: Request,
    email: str = Form(...),
    password: str = Form(...),
    db: AsyncSession = Depends(get_db),
):
    lang = request.cookies.get("lang", "he")
    result = await db.execute(select(User).where(User.email == email))
    user = result.scalar_one_or_none()

    if not user or not verify_password(password, user.hashed_password):
        return templates.TemplateResponse("auth/login.html", {
            "request": request, "lang": lang,
            "error": "אימייל או סיסמה שגויים" if lang == "he" else "Invalid email or password",
        })

    token = create_access_token(user.id)
    response = RedirectResponse("/dashboard", status_code=303)
    response.set_cookie("access_token", token, httponly=True, max_age=60 * 60 * 24 * 7, samesite="lax")
    return response


@router.get("/logout")
async def logout():
    response = RedirectResponse("/", status_code=303)
    response.delete_cookie("access_token")
    return response
