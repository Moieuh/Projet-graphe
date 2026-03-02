# Job Market Data Pipeline & Analytics Dashboard

## Project Overview

This project is a production-style ETL pipeline that:

- Extracts remote job data from Remotive API
- Transforms and cleans the data
- Loads it into PostgreSQL
- Tracks pipeline runs
- Visualizes analytics with Metabase

---

## 🏗 Architecture

Remotive API
        ↓
Python ETL (pipeline.py)
        ↓
PostgreSQL (Docker)
        ↓
Metabase Dashboard

---

## Tech Stack

- Python
- PostgreSQL
- Docker & Docker Compose
- Metabase
- Logging system
- Incremental loading

---

## Dashboard Features

- Total jobs KPI
- Jobs by category
- Jobs by job type
- Top 5 companies
- Jobs by location
- Dynamic filters (Category, Job Type)

---

## How to Run

```bash
docker compose up --build
