# 🚀 DevUpward | Hackathon Team Showcase Bot & Management Dashboard

[![Python](https://img.shields.io/badge/Python-3.13-3776AB?logo=python&logoColor=white)](https://www.python.org/)
[![FastAPI](https://img.shields.io/badge/FastAPI-0.115+-009688?logo=fastapi&logoColor=white)](https://fastapi.tiangolo.com/)
[![discord.py](https://img.shields.io/badge/discord.py-2.4+-5865F2?logo=discord&logoColor=white)](https://discordpy.readthedocs.io/)
[![React](https://img.shields.io/badge/React-19-61DAFB?logo=react&logoColor=black)](https://react.dev/)
[![Vite](https://img.shields.io/badge/Vite-6+-646CFF?logo=vite&logoColor=white)](https://vitejs.dev/)
[![Tailwind CSS](https://img.shields.io/badge/Tailwind_CSS-v4-38B2AC?logo=tailwind-css&logoColor=white)](https://tailwindcss.com/)

An official, interactive Discord Showcase Bot and web-based Admin Management Dashboard designed as the permanent digital storefront, interactive portfolio, and brand ambassador for a hackathon team.

---

## 🌟 Key Features

### 🤖 Discord Bot Capabilities
* **Team Identity (`/about`, `/socials`):** Official team branding cards, slogan, mission statement, tech specialties, and social links.
* **Interactive Team Roster (`/team`, `/member [name]`):** Browse squad members via interactive dropdown menus (`StringSelectMenu`) and autocomplete profile cards with direct portfolio links.
* **Project Showroom (`/projects`, `/project [name]`):** Rich prototype spotlight embeds featuring problem/solution summaries, awards won, screenshots, and buttons linking to live demos, GitHub repositories, and Devpost submissions.
* **Hackathon Hall of Fame (`/awards`, `/stats`):** Chronological trophy room displaying medals (`🥇`, `🥈`, `🥉`) and dynamically computed team statistics (win rate, total projects, awards won).
* **Hospitality & Onboarding:**
  * Automated VIP onboarding greeting guests in `#welcome`.
  * In-Discord Contact Form (`/contact` Modal) routing inquiries from recruiters, mentors, and event organizers straight into an internal `#team-inbox` channel.
* **Dynamic Team Presence:** Continuously cycles through custom team statuses (e.g. *"🏆 4x Hackathon Winners"*, *"⚡ Building next-gen AI"*).

### 🖥️ React Management Dashboard
* **Real-time Bot Telemetry:** Live bot status indicator (online/offline, ping, connected guild count).
* **Roster Manager:** Form-based member profiles, avatar previews, skill tags, and display ordering.
* **Showroom Manager:** Add/edit hackathon prototypes, media previews, and toggle featured projects.
* **Awards Tracker:** Log placements, categories, and associate awards with projects.
* **Bot Controls:** Update live Discord presence in one click, trigger slash command syncs, and configure channel IDs.
* **Inquiries Inbox:** Review and track `/contact` submissions made by server visitors.

---

## 🏗️ Architecture Overview

The application is structured as a **Unified Async Monolith**:
* **Backend:** `FastAPI` (REST CRUD API) and `discord.py` (Discord client) run concurrently inside Python's native `asyncio` event loop. This allows the API to directly command the bot instance in memory (e.g. instant presence updates) without needing Redis.
* **Persistence:** `SQLModel` (SQLAlchemy Async + Pydantic) using `SQLite` in WAL (Write-Ahead Logging) mode for zero-cost, high-concurrency storage, seamlessly portable to PostgreSQL.
* **Frontend:** Single-Page Application (SPA) built with React 19, Vite, Tailwind CSS v4, and Lucide icons.

```
devupward/
├── backend/
│   ├── app/
│   │   ├── api/            # FastAPI REST routes (team, projects, awards, settings)
│   │   ├── bot/            # discord.py bot engine and cogs
│   │   │   └── cogs/       # identity, roster, projects, awards, hospitality
│   │   ├── core/           # Configuration and settings loader
│   │   └── models/         # SQLModel database entity schemas
│   ├── requirements.txt    # Python dependencies
│   └── venv/               # Isolated virtual environment
├── frontend/
│   ├── src/
│   │   ├── components/     # UI components (modals, navbar, forms, cards)
│   │   ├── pages/          # Dashboard views
│   │   └── App.tsx         # Main application container
│   ├── package.json
│   └── vite.config.ts      # Vite config with API proxy
├── data/                   # SQLite database directory (.gitignore protected)
├── .env.example            # Environment template
└── README.md
```

---

## ⚡ Quick Start Guide

### Prerequisites
* **Python:** 3.11 or newer (tested on 3.13)
* **Node.js:** 18 or newer (tested on 22)

---

### 1. Environment Configuration
Copy the template and fill in your Discord credentials:
```bash
cp .env.example .env
```

| Variable | Description | Default |
| :--- | :--- | :--- |
| `DISCORD_BOT_TOKEN` | Bot token from Discord Developer Portal | *Required* |
| `DISCORD_CLIENT_ID` | Application Client ID | *Required* |
| `DISCORD_GUILD_ID` | Target server ID (for fast slash command sync) | *Optional* |
| `ADMIN_API_KEY` | Secret key used by the dashboard for admin actions | `dev_admin_key_12345` |
| `DATABASE_URL` | Async database connection string | `sqlite+aiosqlite:///./data/showcase.db` |
| `TEAM_NAME` | Default branding name | `DevUpward` |

---

### 2. Quick Launch (Development Mode)
Run both the Python backend and React frontend concurrently with one command:
```bash
# Windows PowerShell:
.\start_dev.ps1

# Windows Command Prompt:
start_dev.bat
```

Or run them individually:
* **Backend:**
  ```bash
  .\backend\venv\Scripts\Activate.ps1
  python backend/app/main.py
  ```
* **Frontend:**
  ```bash
  cd frontend
  npm run dev
  ```
  Open `http://localhost:3000` in your browser. All `/api` requests proxy to `http://localhost:8000`.

---

### 3. Docker Deployment (Single-Port Production Mode)
The repository includes a multi-stage `Dockerfile` and `docker-compose.yml`. In production, the React dashboard is built and mounted directly into FastAPI, allowing the **Bot Gateway, REST API, and Web UI** to run from a single container on port `8000`:
```bash
docker compose up -d --build
```
* **Web Dashboard & API:** `http://localhost:8000`
* **API Documentation:** `http://localhost:8000/docs`
* **Data Persistence:** `./data` is mounted to `/app/data` to preserve your SQLite database across container upgrades.

---

### 4. Portfolio Data Backup & Migration
Export or restore your team members, projects, awards, and settings into a single JSON file:
```bash
# Export all data to JSON:
python backend/backup.py export my_portfolio_backup.json

# Restore data from JSON backup:
python backend/backup.py import my_portfolio_backup.json
```

---

### 5. Discord Developer Portal Setup
1. Go to the [Discord Developer Portal](https://discord.com/developers/applications) and create a New Application.
2. Under **Bot**, click **Reset Token** and copy your token into `DISCORD_BOT_TOKEN` in `.env`.
3. Under **Privileged Gateway Intents**, enable **Server Members Intent** (required for onboarding welcome messages).
4. Under **OAuth2 > URL Generator**:
   * Scopes: `bot`, `applications.commands`
   * Permissions: `Send Messages`, `Embed Links`, `Attach Files`, `Read Message History`, `Use Slash Commands`
5. Open the generated URL in your browser to invite the bot to your server.

---

## 🛠️ Tech Stack


* **Backend:** Python 3.13, `discord.py` 2.7, `FastAPI` 0.115, `SQLModel` 0.0.48, `aiosqlite` 0.22, `Uvicorn`
* **Frontend:** React 19, TypeScript, Vite, Tailwind CSS v4, Lucide React, Axios
* **Database:** SQLite (Async WAL mode) / PostgreSQL compatible

---

## 📄 License
Copyright © 2026 DevUpward. All Rights Reserved.  
This software is **proprietary and confidential**. Unauthorized copying, distribution, or modification of this project, in whole or in part, via any medium, is strictly prohibited. See [LICENSE](LICENSE) for details.


