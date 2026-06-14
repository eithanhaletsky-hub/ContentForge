import google.generativeai as genai
from app.config import get_settings

settings = get_settings()
genai.configure(api_key=settings.GEMINI_API_KEY)

CONTENT_PROMPTS = {
    "social_post": {
        "he": """אתה מומחה שיווק דיגיטלי. צור פוסט לרשת חברתית.
פלטפורמה: {platform}
נושא: {topic}
טון: {tone}
קהל יעד: {audience}
פרטים נוספים: {details}

צור פוסט מקצועי וקליט שמתאים לפלטפורמה. כולל אימוג'ים והאשטאגים רלוונטיים.
אורך: מתאים לפלטפורמה שנבחרה.""",
        "en": """You are a digital marketing expert. Create a social media post.
Platform: {platform}
Topic: {topic}
Tone: {tone}
Target audience: {audience}
Additional details: {details}

Create a professional, engaging post suited for the platform. Include relevant emojis and hashtags.
Length: appropriate for the chosen platform.""",
    },
    "email": {
        "he": """אתה מומחה email marketing. כתוב אימייל שיווקי.
סוג: {email_type}
נושא: {topic}
טון: {tone}
קהל יעד: {audience}
פרטים נוספים: {details}

כתוב אימייל מקצועי עם:
- כותרת (subject line) קליטה
- פתיחה מושכת
- גוף ההודעה
- קריאה לפעולה (CTA)""",
        "en": """You are an email marketing expert. Write a marketing email.
Type: {email_type}
Topic: {topic}
Tone: {tone}
Target audience: {audience}
Additional details: {details}

Write a professional email with:
- Catchy subject line
- Engaging opening
- Body content
- Call to action (CTA)""",
    },
    "ad": {
        "he": """אתה קופירייטר מומחה בפרסום דיגיטלי. צור מודעה.
פלטפורמה: {platform}
מוצר/שירות: {topic}
טון: {tone}
קהל יעד: {audience}
פרטים נוספים: {details}

צור מודעה עם:
- כותרת ראשית (headline)
- כותרת משנית
- טקסט המודעה
- קריאה לפעולה (CTA)""",
        "en": """You are an expert advertising copywriter. Create an ad.
Platform: {platform}
Product/Service: {topic}
Tone: {tone}
Target audience: {audience}
Additional details: {details}

Create an ad with:
- Primary headline
- Secondary headline
- Ad copy
- Call to action (CTA)""",
    },
    "blog": {
        "he": """אתה כותב תוכן מקצועי ומומחה SEO. כתוב מאמר בלוג.
נושא: {topic}
טון: {tone}
קהל יעד: {audience}
מילות מפתח: {keywords}
פרטים נוספים: {details}

כתוב מאמר מקצועי עם:
- כותרת ראשית מושכת
- הקדמה
- 3-5 כותרות משנה עם תוכן
- סיכום
- אורך: 500-800 מילים""",
        "en": """You are a professional content writer and SEO expert. Write a blog article.
Topic: {topic}
Tone: {tone}
Target audience: {audience}
Keywords: {keywords}
Additional details: {details}

Write a professional article with:
- Engaging main title
- Introduction
- 3-5 subheadings with content
- Summary
- Length: 500-800 words""",
    },
    "product": {
        "he": """אתה מומחה בכתיבת תיאורי מוצרים לחנויות אונליין. כתוב תיאור מוצר.
שם המוצר: {topic}
קטגוריה: {category}
פלטפורמה: {platform}
קהל יעד: {audience}
פרטים נוספים: {details}

כתוב תיאור מוצר עם:
- כותרת מוצר מושכת
- תיאור קצר (2-3 משפטים)
- תיאור מפורט
- 5 נקודות יתרון (bullet points)
- מילות מפתח ל-SEO""",
        "en": """You are an expert product description writer for e-commerce. Write a product description.
Product name: {topic}
Category: {category}
Platform: {platform}
Target audience: {audience}
Additional details: {details}

Write a product description with:
- Engaging product title
- Short description (2-3 sentences)
- Detailed description
- 5 benefit bullet points
- SEO keywords""",
    },
    "bio": {
        "he": """אתה מומחה במיתוג אישי ועסקי. כתוב ביו/תיאור עסקי.
שם העסק/אדם: {topic}
תחום: {category}
טון: {tone}
קהל יעד: {audience}
פרטים נוספים: {details}

כתוב:
- ביו קצר (2-3 משפטים) לרשתות חברתיות
- תיאור בינוני (פסקה אחת) לאתר
- תיאור מלא (2-3 פסקאות) לדף אודות""",
        "en": """You are a personal and business branding expert. Write a bio/business description.
Business/Person name: {topic}
Industry: {category}
Tone: {tone}
Target audience: {audience}
Additional details: {details}

Write:
- Short bio (2-3 sentences) for social media
- Medium description (one paragraph) for website
- Full description (2-3 paragraphs) for about page""",
    },
}


MODELS = ["gemini-2.0-flash", "gemini-1.5-flash", "gemini-1.5-pro", "gemini-2.5-flash", "gemini-2.5-flash-lite", "gemini-2.0-flash", "gemini-2.0-flash-lite", "gemini-3-flash",]


class QuotaExceededError(Exception):
    def __init__(self, language: str = "he"):
        if language == "he":
            super().__init__(
                "המכסה היומית של Gemini API נוצלה. נסה שוב מאוחר יותר או שדרג את תוכנית ה-API שלך."
            )
        else:
            super().__init__(
                "Gemini API daily quota exceeded. Please try again later or upgrade your API plan."
            )


async def generate_content(content_type: str, language: str, **kwargs) -> str:
    prompt_template = CONTENT_PROMPTS.get(content_type, {}).get(language)
    if not prompt_template:
        prompt_template = CONTENT_PROMPTS.get(content_type, {}).get("en", "")

    safe_kwargs = {k: (v or "") for k, v in kwargs.items()}
    prompt = prompt_template.format(**safe_kwargs)

    for model_name in MODELS:
        try:
            model = genai.GenerativeModel(model_name)
            response = await model.generate_content_async(prompt)
            return response.text
        except Exception as e:
            error_msg = str(e).lower()
            if "429" in error_msg or "quota" in error_msg or "rate" in error_msg:
                continue
            raise

    raise QuotaExceededError(language)
