from sqlalchemy import select, desc
from sqlalchemy.ext.asyncio import AsyncSession
from app.models.content import GeneratedContent


async def save_content(
    db: AsyncSession,
    user_id: int,
    content_type: str,
    title: str,
    prompt_data: str,
    generated_text: str,
    language: str = "he",
    platform: str = "",
) -> GeneratedContent:
    content = GeneratedContent(
        user_id=user_id,
        content_type=content_type,
        title=title,
        prompt_data=prompt_data,
        generated_text=generated_text,
        language=language,
        platform=platform,
    )
    db.add(content)
    await db.commit()
    await db.refresh(content)
    return content


async def get_user_contents(db: AsyncSession, user_id: int, limit: int = 50):
    result = await db.execute(
        select(GeneratedContent)
        .where(GeneratedContent.user_id == user_id)
        .order_by(desc(GeneratedContent.created_at))
        .limit(limit)
    )
    return result.scalars().all()


async def get_content_by_id(db: AsyncSession, content_id: int, user_id: int):
    result = await db.execute(
        select(GeneratedContent)
        .where(GeneratedContent.id == content_id, GeneratedContent.user_id == user_id)
    )
    return result.scalar_one_or_none()


async def delete_content(db: AsyncSession, content_id: int, user_id: int) -> bool:
    content = await get_content_by_id(db, content_id, user_id)
    if not content:
        return False
    await db.delete(content)
    await db.commit()
    return True
