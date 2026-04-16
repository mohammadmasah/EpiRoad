# EpiRoad
# 🛣️ EpiRoad : Infrastructure & Architecture Plan (Full Stack)

Ce document définit la vision technique complète du projet **EpiRoad**. L'objectif est d'automatiser la recherche d'alternances pour les étudiants d'Epitech en utilisant une architecture robuste, moderne et scalable.

---

## 🏗️ 1. Architecture Globale (System Design)

Nous utilisons une architecture **Service-Oriented (Découplée)**. Le backend est séparé en couches pour isoler la logique métier (Scraping) de la logique de communication (API).

* **Pattern :** Service-Layer Pattern (au lieu du MVC classique).
* **Workflow :** 1. Le **Worker** (Celery) lance les **Scrapers** (Services).
    2. Les données sont nettoyées et stockées dans **PostgreSQL**.
    3. Le **Frontend** (Next.js) consomme les données via une **API REST** (FastAPI).

---

## 🛠️ 2. Stack Technique (Full-Stack)

### **A. Backend (Le Moteur)**
* **Langage :** `Python 3.10+` (Expertise Data & Automation).
* **Framework API :** `FastAPI` (Haute performance, Async, Documentation Swagger auto-générée).
* **Gestionnaire de Tâches :** `Celery` + `Redis` (Pour l'exécution asynchrone des scrapers chaque nuit).
* **Base de Données :** * `PostgreSQL` (Stockage permanent : Offres, Utilisateurs, Candidatures).
    * `SQLModel` (ORM moderne combinant SQLAlchemy et Pydantic).
* **Migrations :** `Alembic` (Versionning de la base de données).

### **B. Scraping & Automation (L'Intelligence)**
* **Moteur Principal :** `Playwright` (Pour gérer le rendu JavaScript, les scrolls infinis et les redirections).
* **Parsing Rapide :** `BeautifulSoup4` (Pour extraire les données du HTML statique).
* **Intégration Cloud :** `gspread` (API Google Sheets pour la synchronisation en temps réel avec Google Drive).

### **C. Frontend (L'Interface)**
* **Framework :** `Next.js 14+` (React).
* **Styling :** `Tailwind CSS` (Design moderne et responsive).
* **Data Fetching :** `TanStack Query` (React Query) pour le cache et la synchronisation avec l'API.

---

## 📁 3. Structure des Dossiers (Project Layout)

```text
epiroad-root/
├── backend/
│   ├── app/
│   │   ├── api/            # Endpoints (v1/jobs, v1/users)
│   │   ├── core/           # Config, Sécurité (JWT), .env
│   │   ├── db/             # Session & Connection PostgreSQL
│   │   ├── models/         # Tables SQL (SQLModel)
│   │   ├── schemas/        # Validation de données (Pydantic)
│   │   ├── services/       # LOGIQUE MÉTIER (Scrapers logic, Cleaners)
│   │   └── worker/         # Configuration Celery Tasks
│   ├── migrations/         # Historique Alembic
│   ├── docker-compose.yml  # Orchestration (DB, Redis, API)
│   └── requirements.txt
├── frontend/
│   ├── src/components/     # UI Reusable components
│   ├── src/app/            # Next.js App Router
│   └── tailwind.config.js
└── scripts/                # Scripts de maintenance
