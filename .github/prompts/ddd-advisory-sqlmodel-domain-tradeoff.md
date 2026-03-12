# DDD Advisory – SQLModel in domain models (design decision required)

## Context

Stack: Python 3.12, FastAPI, SQLModel. Workspace root: `c:\Users\Marc\Documents\ITA\Grid Fans`. `.venv` is at `f1_api/.venv`.

This is **not an instruction to implement** — it documents a design decision that requires a human choice before proceeding. Do not make any changes until the trade-off has been decided.

---

## Issue

Every `features/*/domain/models.py` file uses `SQLModel` as the base class and imports `Field` from `sqlmodel`:

```
features/drivers/domain/models.py
features/leagues/domain/models.py
features/teams/domain/models.py
features/user/domain/models.py
features/user_teams/domain/models.py
```

In strict DDD, domain models are **pure Python** — they carry business rules and no framework dependencies. Persistence mapping (column names, types, table declarations) belongs in the infrastructure layer. Using SQLModel in the domain means:

- Domain models cannot be unit-tested without a database session
- Changing the ORM requires changing domain models
- The domain is framework-coupled

---

## Options

### Option A — Accept the trade-off (recommended for this project)

SQLModel merging domain model and ORM mapping into one class is a **deliberate design choice** made by the SQLModel library itself. For a project of this size without a need to swap ORMs, this is standard and acceptable. No action needed.

**Consequence**: Document this as an explicit architectural decision: "Domain models are SQLModel entities. The project uses SQLModel as both the ORM and the domain model base class."

### Option B — Separate domain models from persistence models

Introduce a second class per entity:

- `domain/models.py` — pure dataclass or Pydantic model (no SQLModel)
- `infrastructure/persistence/models.py` — SQLModel table model
- `infrastructure/persistence/mappers.py` — converts between the two

This doubles the number of model classes and requires a mapper for every read/write. It is a significant refactor (every repository, every service, every route would need updating).

**Only choose Option B if**: you anticipate needing to swap ORMs, want domain models to be completely testable without a database, or the business logic in domain models is complex enough to warrant isolation.

---

## Recommendation

Keep Option A. The SQLModel-as-domain-model approach is the stated design intent of the library and is consistent with how the rest of this codebase is structured. The more impactful DDD violations (concrete infra imports in application layer, `HTTPException` in domain) are addressed in phases 6a–6d.

If Option B is desired in the future, implement it as a separate dedicated phase after 6a–6d are complete.
