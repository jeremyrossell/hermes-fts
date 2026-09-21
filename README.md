<div align="center">
  <img src="docs/assets/banner.png" alt="Hermes FTS Banner" width="100%" max-width="700px">

  # Hermes FTS
  High-performance Full-Text Search (FTS) REST API built with Django and PostgreSQL GIN Indexes.
</div>

---

## Overview

**Hermes FTS**—named after the Greek deity known as the messenger of the gods—is a backend reference API designed to eliminate database query latency in text-heavy applications. Standard SQL `LIKE` or Django `icontains` lookups force full-table sequential scans, severely degrading query performance as data scales. To resolve this, Hermes FTS leverages PostgreSQL native `SearchVectorField` and Generalized Inverted Indexes (`GinIndex`), tokenizing raw text into lexemes and mapping them directly to row IDs.

The project provides both a RESTful HTTP API and a CLI benchmark suite, demonstrating **sub-30ms query execution across 5,020,000 records**, achieving a **5.2x speedup** over unindexed scans. Designed as a pluggable backend engine for modern web and mobile frameworks (e.g., Flutter, React, Vue, etc), it delivers a lightweight, high-performance alternative to resource-intensive search clusters like Elasticsearch for e-commerce catalogs and log exploration.

## Cross-platform compatibility

This project is fully OS-agnostic and runs identically on:
- **Linux** (Native)
- **macOS** (Intel & Apple Silicon)
- **Windows** (Native PowerShell or WSL2)

System dependencies are encapsulated via `uv` and Docker, ensuring consistent execution environments across all platforms.

## Prerequisites

- **Python:** 3.12 or higher
- **Framework:** Django 6.x
- **Package Manager:** `uv`
- **Database:** PostgreSQL 16
- **Container Runtime:** Docker Desktop or Docker Engine

---

## Getting started

### 1. Repository setup

Clone the repository and install dependencies using `uv`:
```bash
git clone https://github.com/jeremyrossell/hermes-fts.git
cd hermes-fts
uv sync
```

### 2. Environment configuration

Copy the environment variable template:
```bash
cp .env.example .env
```

Ensure your `.env` contains the default local configuration:
```env
DEBUG=True
SECRET_KEY=django-insecure-development-key-change-in-prod
ALLOWED_HOSTS=127.0.0.1,localhost

DB_NAME=postgres-search
DB_USER=postgres
DB_PASSWORD=postgres
DB_HOST=localhost
DB_PORT=5432
```

### 3. Database initialization (Docker)

Spin up a PostgreSQL container named `postgres-search`:
```bash
docker run --name postgres-search \
  -e POSTGRES_DB=postgres-search \
  -e POSTGRES_USER=postgres \
  -e POSTGRES_PASSWORD=postgres \
  -p 5432:5432 \
  -d postgres:16-alpine
```

### 4. Database migrations

Apply schema migrations to generate the GIN index in PostgreSQL:
```bash
uv run python manage.py migrate
```

### 4.1. Data seeding

Populate the database with X synthetic articles pre-calculated with search vectors:
```bash
uv run python manage.py seed_data --count 5000000
```

### 5. Running benchmarks

Execute the CLI benchmarking tool to compare sequential table scans against the PostgreSQL GIN index:
```bash
uv run python manage.py benchmark_search --query infrastructure
```

### 6. (Development) Server & API usage

Start the local Django server:
```bash
uv run python manage.py runserver
```

#### API Endpoints

* **Optimized search (GIN Index):**
`GET /api/search/?q=infrastructure&mode=fast`
* **Unoptimized search (Sequential Scan):**
`GET /api/search/?q=infrastructure&mode=slow`

Example JSON Response:
```json
{
  "mode": "fast",
  "query": "infrastructure",
  "execution_time_ms": 1.82,
  "count": 20,
  "results": [
    {
      "id": 104,
      "title": "Article #104: Infrastructure Performance Search"
    }
  ]
}
```

## Running unit tests

Execute the automated test suite:
```bash
uv run python manage.py test
```