# ⚡ ElectroStore — Premium Electronics E-Commerce

> **Live Site:** [https://electrostore.onrender.com](https://electrostore.onrender.com)
> **GitHub:** [https://github.com/Hrithikv286/portfolio](https://github.com/Hrithikv286/portfolio)

A full-featured electronics e-commerce platform with an integrated AI assistant, built with Django (Python).

---

## 📋 Features

### Store
- **Electronics catalog** with 8 categories: Smartphones, Laptops, TVs, Audio, Gaming, Smart Home, Cameras, Accessories
- **Product search** with real-time filtering by category, price, and rating
- **Responsive design** — works on mobile, tablet, and desktop
- Product detail pages with specifications, ratings, and related items

### AI Assistant (ElectroBot)
- **Google Gemini AI** powered chatbot available on every page
- Answers FAQs from the SQL database
- Explains HTTP and site-specific error codes
- Creates **support tickets** in SQL when it cannot answer
- **Chat logs and feedback** stored in MongoDB Atlas

### Pages (≥3)
| Page | URL | Description |
|------|-----|-------------|
| Home | `/` | Hero section, categories, featured products |
| Products | `/products/` | Filtered product listing with search |
| Product Detail | `/products/<slug>/` | Full product info + specs |
| FAQ | `/faq/` | 13 categorized FAQs from SQL |
| Error Codes | `/error-codes/` | 8 error codes with explanations |
| About | `/about/` | Company info and tech stack |
| Contact | `/contact/` | AJAX contact form → support ticket |
| Health Check | `/health/` | JSON system health status |

### Error Pages
| Code | URL | Page |
|------|-----|------|
| 404 | Any bad URL | Custom 404 + "Ask Assistant" |
| 500 | `/errors/500/` | Custom 500 + "Ask Assistant" |
| 400 | `/errors/400/` | Bad Request |
| 401 | `/errors/401/` | Unauthorized |
| 403 | `/errors/403/` | Forbidden |
| 429 | `/errors/429/` | Too Many Requests |
| 503 | `/errors/503/` | Service Unavailable |
| ES001 | `/errors/ES001/` | Payment Declined (site-specific) |

---

## 🗄️ Data Storage

| Data | Storage |
|------|---------|
| Products, Categories, Brands | SQLite (SQL) |
| FAQs (≥10) | SQLite (SQL) |
| Error Codes (8+) | SQLite (SQL) |
| Support Tickets | SQLite (SQL) |
| Chat Logs | MongoDB Atlas |
| User Feedback | MongoDB Atlas |

---

## 🔌 Third-Party APIs

| API | Purpose | Fallback |
|-----|---------|---------|
| Google Gemini | AI chat responses | Rule-based FAQ matching |
| OpenWeatherMap | Weather widget on homepage | Static fallback data |
| MongoDB Atlas | Chat log persistence | Logs silently skipped |

---

## 🚀 Local Setup

### Prerequisites
- Python 3.11+
- pip

### Steps

```bash
# 1. Clone the repo
git clone https://github.com/Hrithikv286/portfolio.git
cd portfolio

# 2. Install dependencies
pip install -r requirements.txt

# 3. Create environment file
cp .env.example .env
# Edit .env and add your API keys:
# GEMINI_API_KEY=...
# MONGODB_URI=...
# OPENWEATHER_API_KEY=...

# 4. Run migrations
python manage.py migrate

# 5. Seed sample data
python manage.py seed_data

# 6. Create admin user
python manage.py createsuperuser

# 7. Start the server
python manage.py runserver

# Visit http://127.0.0.1:8000/
```

---

## 🔐 Environment Variables

Copy `.env.example` to `.env` and fill in:

| Variable | Required | Description |
|----------|----------|-------------|
| `SECRET_KEY` | ✅ | Django secret key |
| `DEBUG` | ✅ | `True` (dev) / `False` (prod) |
| `GEMINI_API_KEY` | ✅ | [Google AI Studio](https://aistudio.google.com/app/apikey) |
| `MONGODB_URI` | Optional | [MongoDB Atlas](https://cloud.mongodb.com) connection string |
| `OPENWEATHER_API_KEY` | Optional | [OpenWeatherMap](https://openweathermap.org/api) API key |

> ⚠️ **Never commit your `.env` file!** It is already in `.gitignore`.

---

## 🌐 Deploy on Render

1. Fork / push this repo to GitHub
2. Go to [render.com](https://render.com) → New Web Service
3. Connect your GitHub repo
4. Render will auto-detect `render.yaml`
5. Set environment variables in Render dashboard:
   - `GEMINI_API_KEY`
   - `MONGODB_URI`
   - `OPENWEATHER_API_KEY`
6. Deploy!

---

## 🏥 Health Check

`GET /health/` — Returns JSON:
```json
{
  "status": "healthy",
  "timestamp": "...",
  "version": "1.0.0",
  "checks": {
    "database": {"status": "ok", "products": 12},
    "mongodb": {"status": "ok"},
    "gemini_api": {"status": "configured"},
    "weather_api": {"status": "configured"}
  }
}
```

---

## 📈 Proposed Improvement

**Real-time inventory and price tracking with WebSockets:**
Add Django Channels to enable real-time price updates, live stock notifications, and a live order tracking feature. This would significantly improve the user experience and is a natural next step for scaling the platform.

---

## 🛠️ Tech Stack

- **Backend:** Django 5.1, Python 3.11
- **Database:** SQLite (SQL) + MongoDB Atlas (NoSQL)  
- **AI:** Google Gemini 1.5 Flash
- **Deployment:** Render (with Gunicorn + WhiteNoise)
- **Frontend:** Vanilla HTML/CSS/JS, Inter & Outfit fonts, Font Awesome

---

*Built as a Software Development final assessment project.*
