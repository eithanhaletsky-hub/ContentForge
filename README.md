# ContentForge — AI Marketing Content Generator

Professional AI-powered platform for creating marketing content. Built with FastAPI, Gemini AI, and TailwindCSS.

## Features

- **6 Content Types**: Social posts, marketing emails, ads, blog articles, product descriptions, bio/about
- **AI-Powered**: Google Gemini API generates professional content in seconds
- **Bilingual**: Full Hebrew (RTL) and English (LTR) support
- **User System**: Registration, login, profiles with JWT authentication
- **Content History**: All generated content saved and searchable
- **Modern UI**: Professional design with TailwindCSS, fully responsive
- **Secure**: bcrypt password hashing, HTTP-only cookies, input validation

## Quick Start

### 1. Install Python dependencies

```bash
pip install -r requirements.txt
```

### 2. Set up environment variables

Copy `.env.example` to `.env` and add your Gemini API key:

```bash
cp .env.example .env
```

Edit `.env`:
```
GEMINI_API_KEY=your-gemini-api-key-here
SECRET_KEY=your-random-secret-key-here
```

### 3. Get a Gemini API Key

1. Go to https://aistudio.google.com/apikey
2. Click "Create API Key"
3. Copy the key and paste it in your `.env` file

### 4. Run the application

```bash
python run.py
```

Open your browser at: **http://127.0.0.1:8000**

## Tech Stack

| Technology | Purpose |
|---|---|
| FastAPI | Backend web framework |
| SQLAlchemy | Database ORM |
| SQLite | Database (upgradeable to PostgreSQL) |
| Google Gemini API | AI content generation |
| Jinja2 | HTML templating |
| TailwindCSS (CDN) | Styling |
| Lucide Icons | Icon library |

## Project Structure

```
AIproject/
├── app/
│   ├── main.py              # Application entry point
│   ├── config.py            # Settings & environment
│   ├── database.py          # Database setup
│   ├── models/              # Database models
│   ├── routers/             # API routes
│   ├── services/            # Business logic
│   ├── templates/           # HTML templates
│   └── static/              # CSS, JS, images
├── .env.example             # Environment template
├── requirements.txt         # Python dependencies
└── run.py                   # Run script
```

## License

This is a commercial product. All rights reserved.
