# AI-Powered Smart Retail Cart Platform

A comprehensive software-first prototype of an IoT retail cart system with real-time billing, AI product verification, navigation, recommendations, and admin analytics.

## 🏗️ System Architecture

```
┌─────────────────┐
│   Cart UI App   │ (React - Simulated Cart Device)
└────────┬────────┘
         │ HTTP/WebSocket
┌────────▼─────────────────────────────────────┐
│         FastAPI Backend Server               │
│  ┌────────────────────────────────────────┐  │
│  │  Billing Engine │ Cart Management      │  │
│  │  AI Vision      │ Navigation           │  │
│  │  Recommendations│ Theft Detection      │  │
│  │  Payment Sim    │ IoT Events           │  │
│  └────────────────────────────────────────┘  │
└────────┬─────────────────────────────────────┘
         │
    ┌────┴────┬──────────────┬──────────┐
    │         │              │          │
┌───▼───┐ ┌──▼───┐    ┌──────▼──────┐  │
│PostgreSQL│Redis│    │  AI Module  │  │
│Database  │Cache│    │ (YOLOv8)    │  │
└─────────┘ └─────┘    └─────────────┘  │
                                      │
                              ┌───────▼───────┐
                              │ Admin Dashboard│
                              │    (React)    │
                              └───────────────┘
```

## 📁 Project Structure

```
smart-retail-cart/
├── backend/
│   ├── app/
│   │   ├── __init__.py
│   │   ├── main.py
│   │   ├── config.py
│   │   ├── database.py
│   │   ├── models/
│   │   ├── schemas/
│   │   ├── api/
│   │   ├── services/
│   │   └── ai/
│   ├── requirements.txt
│   └── alembic/
├── frontend/
│   ├── cart-app/
│   └── admin-dashboard/
├── ai_module/
│   ├── models/
│   └── inference.py
├── database/
│   ├── init.sql
│   └── seed_data.sql
└── docs/
    └── API.md
```

## 🚀 Quick Start

### Prerequisites
- Python 3.9+
- Node.js 16+
- PostgreSQL 12+
- Redis 6+

### Backend Setup

```bash
cd backend
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
pip install -r requirements.txt
```

### Database Setup

```bash
# Create database
createdb smart_retail_cart

# Run migrations
cd backend
alembic upgrade head

# Seed data
psql smart_retail_cart < ../database/seed_data.sql
```

### Frontend Setup

```bash
cd frontend/cart-app
npm install
npm start

cd ../admin-dashboard
npm install
npm start
```

### Run Backend

```bash
cd backend
uvicorn app.main:app --reload --port 8000
```

## 🎯 Features

- ✅ Real-time billing engine
- ✅ AI product verification (YOLOv8)
- ✅ Store navigation with aisle routing
- ✅ Product recommendations
- ✅ Theft detection system
- ✅ Payment simulation (QR codes)
- ✅ Admin analytics dashboard
- ✅ IoT event simulation

## 📚 API Documentation

See [docs/API.md](docs/API.md) for complete API documentation.

API will be available at: http://localhost:8000/docs (Swagger UI)

## 🧪 Demo Workflow

1. Start backend server
2. Start cart app frontend
3. Start admin dashboard
4. Create a cart session
5. Scan/add products
6. View AI verification
7. Get navigation routes
8. See recommendations
9. Complete payment
10. View analytics in admin dashboard
