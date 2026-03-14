# DDD Dependency Rules — Grid Fans

A quick reference for auditing import violations in this codebase.

---

## What Each Layer Is

### Domain
The pure business model. Contains:
- **Entities / models** — SQLModel table classes (`Drivers`, `Teams`, `SessionResult`, …)
- **Value objects** — immutable data shapes with no identity
- **Domain interfaces (Protocols)** — abstract contracts that infrastructure must satisfy (`IDriversRepository`, `ISeasonContext`, …)
- **Domain logic** — rules and invariants that belong to the business, not to any framework

Has **no knowledge** of how data is stored, fetched, or delivered. No FastAPI, no SQLModel sessions, no FastF1.

### Application
The use-case orchestration layer. Contains:
- **Services** — classes or functions that coordinate domain objects to fulfil one use case (`UpdateSeasonService`, `BuyDriverService`, …)
- **Application DTOs** — input/output shapes that cross the use-case boundary if needed

Knows the domain intimately. Knows **nothing** about how data is persisted or how requests arrive. Receives all infrastructure dependencies via constructor injection typed against domain Protocols.

### Infrastructure
The technical implementation layer. Contains:
- **Repository implementations** — concrete SQLModel queries that satisfy domain repository Protocols (`DriversRepository`, `TeamsRepository`, …)
- **External service clients** — `FastF1Client`, any HTTP clients, email senders, etc.
- **ORM / persistence config** — session factories, migration helpers
- **Season context** — `SeasonContextController` (wraps FastF1 + DB queries)
- **Data ingestion functions** — `get_event_data`, `get_session_results`, etc.

Knows the domain (imports entities and Protocols). Knows **nothing** about HTTP routes or FastAPI.

### Presentation
The delivery layer. Contains:
- **FastAPI routers** — `APIRouter`, route functions, request/response models
- **Dependency wiring** — the only place that imports concrete infrastructure classes and passes them into application services

Knows everything. It is the composition root.

---

## Layer Order (innermost → outermost)

```
domain  →  application  →  infrastructure  →  presentation
```

Each layer may only import from layers **to its left**. Never from layers to its right.

---

## The Rules

### 1. Domain imports nothing from this project
`domain/` files may only import from:
- The Python standard library
- Third-party libraries (e.g. `sqlmodel`, `pydantic`)
- Other `domain/` modules within the same or another feature

**Never:**
```python
# domain/models.py — VIOLATION
from f1_api.features.admin.infrastructure.persistence.x import Y  ❌
from f1_api.features.admin.application.services import Z          ❌
```

---

### 2. Application imports only from domain
`application/` files may import from:
- Their own feature's `domain/`
- Another feature's `domain/` (cross-feature domain access)
- The Python standard library / third-party libraries

**Never:**
```python
# application/services.py — VIOLATION
from f1_api.features.admin.infrastructure.data_ingestion import x  ❌
from f1_api.core.f1_data.infrastructure.season_context import y    ❌
```

If the application layer needs a concrete infrastructure object, it must define a **Protocol** (interface) in `domain/interfaces.py` and receive the concrete impl via constructor injection.

---

### 3. Infrastructure imports from domain (and application where needed)
`infrastructure/` files may import from:
- Their own feature's `domain/` and `application/`
- Another feature's `domain/` (e.g. to persist a foreign entity)
- Third-party libraries

This is the **correct direction** — infrastructure exists to serve the domain.

```python
# infrastructure/persistence/session_results_repository.py — CORRECT
from f1_api.core.f1_data.domain.models import SessionResult  ✅
```

---

### 4. Presentation is the wiring layer — it may import everything
`presentation/routes.py` is the **only place** allowed to import concrete infrastructure implementations and pass them into application services.

```python
# presentation/routes.py — CORRECT
from f1_api.features.admin.infrastructure.data_ingestion import get_event_data  ✅
from f1_api.core.f1_data.infrastructure.season_context import SeasonContextController  ✅

service = UpdateSeasonService(engine, get_event_data=get_event_data, ...)  ✅
```

---

### 5. Cross-feature rules
A feature's **application** layer must not import from another feature's **application or infrastructure** layer.

| From \ To         | domain ✅ | application ❌ | infrastructure ❌ | presentation ❌ |
|-------------------|-----------|----------------|-------------------|----------------|
| **domain**        | same only | ❌             | ❌                | ❌             |
| **application**   | ✅        | ❌             | ❌                | ❌             |
| **infrastructure**| ✅        | ✅             | same only         | ❌             |
| **presentation**  | ✅        | ✅             | ✅                | same only      |

---

## How to Detect Violations

Run this PowerShell command from `f1_api/`:

```powershell
Get-ChildItem . -Recurse -Filter "*.py" |
  Where-Object { $_.FullName -notlike "*__pycache__*" -and $_.FullName -notlike "*.venv*" } |
  Select-String "from f1_api.*infrastructure" |
  Where-Object { $_.Path -like "*\application\*" -or $_.Path -like "*\domain\*" } |
  ForEach-Object { "$($_.Path)  L$($_.LineNumber): $($_.Line.Trim())" }
```

Also check for cross-feature application imports:

```powershell
Get-ChildItem . -Recurse -Filter "*.py" |
  Where-Object { $_.FullName -notlike "*__pycache__*" -and $_.FullName -notlike "*.venv*" } |
  Select-String "from f1_api.*application" |
  Where-Object { $_.Path -like "*\application\*" } |
  ForEach-Object { "$($_.Path)  L$($_.LineNumber): $($_.Line.Trim())" }
```

> False positives: a feature's own `application/` importing from itself is fine. Filter by checking that the import path and the file path reference **different features**.

---

## Fixing a Violation

When application layer `A` needs concrete infrastructure `B`:

1. Define a `Protocol` in `A`'s `domain/interfaces.py` describing what `B` does
2. Add the protocol type to `A`'s service constructor
3. In `A`'s `presentation/routes.py`, import `B` and pass it in

```python
# domain/interfaces.py
class IGetEventData(Protocol):
    def __call__(self, session: Session, year: int) -> list[Events]: ...

# application/services.py
class MyService:
    def __init__(self, get_event_data: IGetEventData): ...

# presentation/routes.py
from f1_api.features.admin.infrastructure.data_ingestion import get_event_data
service = MyService(get_event_data=get_event_data)
```
