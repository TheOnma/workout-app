# FitTrack API

A RESTful backend for a personal workout tracking application, built with FastAPI and SQLAlchemy. This is the backend foundation for a planned iOS app — the goal is to build something I'd actually use daily, with a clean architecture that scales as features grow.

---

## Why I Built This

Most workout apps either do too much or lock your data behind a subscription. I wanted to build something minimal and personal — an API I own completely, that tracks workouts and routines in a way that makes sense for how I actually train.

This project is also my foundation for learning how to design and ship a production-grade mobile backend: authentication, relational data modeling, clean API design, and eventually deployment to a real server before the iOS frontend is built on top.

---

## What It Does

- **User authentication** — JWT-based auth with bcrypt password hashing. Users register, log in, and receive a token that gates all workout and routine endpoints.
- **Workout management** — Create, retrieve, and delete individual workouts. Each workout belongs to the authenticated user.
- **Routine management** — Group workouts into routines via a many-to-many relationship. A routine can contain multiple workouts, and a workout can belong to multiple routines.
- **User-scoped data** — Every query is filtered to the authenticated user. You only ever see your own data.

---

## Data Model

The core relationship is between **Workouts** and **Routines**, linked through an association table:

```
User
 ├── Workout (many)
 └── Routine (many)
      └── workout_routine (association) ── Workout
```

A `Workout` is a single exercise or session — it has a name and description.  
A `Routine` is a collection of workouts — for example, "Push Day" might contain Bench Press, Shoulder Press, and Tricep Dips.

This many-to-many design means the same workout can live in multiple routines without duplication.

---

## Tech Stack

| Layer | Choice | Why |
|---|---|---|
| Framework | FastAPI | Async-ready, automatic docs, type safety via Pydantic |
| ORM | SQLAlchemy | Mature, flexible, great for relational modeling |
| Database | SQLite (dev) | Zero-config for local development, easy swap to Postgres for production |
| Auth | JWT + bcrypt | Stateless tokens, industry-standard password hashing |
| Validation | Pydantic v2 | Request/response validation built into FastAPI |

---

## Project Structure

```
fastapibackend/
└── api/
    ├── main.py          # App entrypoint, middleware, router registration
    ├── database.py      # SQLAlchemy engine and session setup
    ├── models.py        # ORM models: User, Workout, Routine, association table
    ├── deps.py          # Shared dependencies: DB session, JWT auth, bcrypt
    └── routers/
        ├── auth.py      # POST /auth/ (register), POST /auth/token (login)
        ├── workouts.py  # GET, POST, DELETE /workouts/
        └── routines.py  # GET, POST, DELETE /routines/
```

---

## API Endpoints

| Method | Endpoint | Auth | Description |
|---|---|---|---|
| `POST` | `/auth/` | No | Register a new user |
| `POST` | `/auth/token` | No | Log in, receive JWT token |
| `GET` | `/workouts/` | Yes | Get a workout by ID |
| `GET` | `/workouts/workouts` | Yes | Get all workouts |
| `POST` | `/workouts/` | Yes | Create a new workout |
| `DELETE` | `/workouts/` | Yes | Delete a workout |
| `GET` | `/routines/` | Yes | Get all routines (with workouts) |
| `POST` | `/routines/` | Yes | Create a routine with workouts |
| `DELETE` | `/routines/` | Yes | Delete a routine |

Interactive docs available at `http://localhost:8000/docs` when running locally.

---

## Setup

### Prerequisites
- Python 3.11+

### Installation

```bash
git clone https://github.com/TheOnma/fittrack-api
cd fittrack-api/fastapibackend

python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate

pip install -r requirements.txt
```

### Environment Variables

Create a `.env` file in the `fastapibackend/` directory:

```
AUTH_SECRET_KEY=your-secret-key-here
AUTH_ALGORITHM=HS256
```

### Run

```bash
uvicorn api.main:app --reload
# API running at http://localhost:8000
# Docs at http://localhost:8000/docs
```

---

## Roadmap

This backend is actively being developed. Planned additions:

- [ ] Exercise library with sets, reps, and weight tracking per workout
- [ ] Workout session logging — record when and how a routine was performed
- [ ] Progress tracking endpoints — personal records, volume over time
- [ ] PostgreSQL support for production deployment
- [ ] Docker setup for easy self-hosting
- [ ] iOS frontend (SwiftUI) consuming this API

---

## Design Decisions Worth Noting

**Why SQLite for now?** SQLAlchemy makes swapping to Postgres a one-line change in `database.py`. SQLite removes friction during development and keeps the repo self-contained. Production will use Postgres.

**Why JWT over sessions?** The planned iOS client is stateless by nature — JWTs are the right fit for mobile. Tokens expire after 20 minutes currently; refresh token logic is on the roadmap.

**Why many-to-many for workouts and routines?** A "Push Day" and a "Full Body" routine might both include the same workout. Duplicating the workout record for each routine would be the wrong model — the association table keeps data clean and queries simple.
