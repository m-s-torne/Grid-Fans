````prompt
# DDD Cleanup – Phase 5: Fix remaining structural gaps

## Context

Stack: Python 3.12, FastAPI, SQLModel. Workspace root: `c:\Users\Marc\Documents\ITA\Grid Fans`. `.venv` is at `f1_api/.venv`. All imports use the `f1_api.` prefix.

Phase 4 is complete. The app loads cleanly (`from f1_api.main import app` prints `OK`). Four architectural rough edges remain.

---

## Rough Edge 1 — `features/f1_data/` is a hollow shell

### Problem

`f1_api/features/f1_data/` has all four DDD layer directories (application/use_cases, domain/services, infrastructure/external+models+persistence, presentation/routers) but contains **zero Python files**. The real F1 data logic lives in `f1_api/core/f1_data/`. This directory is structural noise.

### Fix

Delete the empty shell entirely:

```powershell
Remove-Item "c:\Users\Marc\Documents\ITA\Grid Fans\f1_api\features\f1_data" -Recurse -Force
```

Verify no Python file anywhere imports from `f1_api.features.f1_data`:

```powershell
Get-ChildItem "c:\Users\Marc\Documents\ITA\Grid Fans\f1_api" -Recurse -Filter "*.py" |
  Where-Object { $_.FullName -notlike "*__pycache__*" } |
  Select-String "f1_api\.features\.f1_data"
```

If the search returns any hits, update those imports to use `f1_api.core.f1_data` instead, then delete the directory.

---

## Rough Edge 2 — `features/drivers/domain/interfaces.py` is incomplete and misnamed

### Problem

The protocol currently declares only:

```python
class DriversRepository(Protocol):
    def get_driver_results(self) -> dict: ...
```

The concrete `DriversRepository` in `f1_api/features/drivers/infrastructure/persistence/drivers_repository.py` exposes these public methods:
- `get_by_ids(self, driver_ids: list[int]) -> list[Drivers]`
- `get_team_assignments(self) -> Dict[int, str]`
- `get_driver_results_data(self) -> dict`  ← note: `_data` suffix, not `get_driver_results`

The protocol is missing two methods and the one method it has uses the wrong name (`get_driver_results` vs `get_driver_results_data`).

### Fix

**Step 1** — Read `f1_api/features/drivers/infrastructure/persistence/drivers_repository.py` in full to get exact signatures for all public methods.

**Step 2** — Rewrite `f1_api/features/drivers/domain/interfaces.py` to declare all public methods with correct names and type signatures. Use the concrete class as the source of truth.

**Step 3** — Search for any code that calls `.get_driver_results(` (without `_data`) and rename those call sites to `.get_driver_results_data(`:

```powershell
Get-ChildItem "c:\Users\Marc\Documents\ITA\Grid Fans\f1_api" -Recurse -Filter "*.py" |
  Where-Object { $_.FullName -notlike "*__pycache__*" } |
  Select-String "\.get_driver_results\b" |
  Select-Object @{N="File";E={$_.Path.Replace("C:\Users\Marc\Documents\ITA\Grid Fans\f1_api\","")}}, LineNumber, @{N="Line";E={$_.Line.Trim()}}
```

---

## Rough Edge 3 — `features/admin/` has no domain layer

### Problem

`f1_api/features/admin/` has application + infrastructure + presentation layers but **no `domain/` directory**. `UpdateSeasonService` in the application layer directly imports infrastructure functions:

```python
from f1_api.features.admin.infrastructure.data_ingestion import (
    get_session_results, get_team_data, get_event_data, get_session_data,
)
```

This violates DIP — the application layer depends on infrastructure, not on abstractions.

### Fix

**Step 1** — Create `f1_api/features/admin/domain/__init__.py` (empty).

**Step 2** — Create `f1_api/features/admin/domain/interfaces.py` with Protocol stubs for each function imported from `data_ingestion.py`. Read `f1_api/features/admin/infrastructure/data_ingestion.py` first to determine exact signatures. The protocols should be function-level interfaces (plain `Protocol` classes with a single `__call__` method, or typed callables using `Protocol`).

Example shape:
```python
"""Admin domain interfaces."""
from typing import Protocol
from sqlmodel import Session
from f1_api.core.f1_data.domain.models import Events, Sessions, SessionResult
from f1_api.features.teams.domain.models import Teams

class IGetEventData(Protocol):
    def __call__(self, session: Session, year: int) -> list[Events]: ...

class IGetSessionData(Protocol):
    def __call__(self, session: Session, year: int) -> list[Sessions]: ...

# ... etc for get_team_data, get_session_results
```

No callers need updating — this is purely additive.

---

## Rough Edge 4 — Inline imports inside application-layer service methods

### Problem

Two files use inline imports inside method bodies as a circular-dependency workaround. This breaks dependency injection and makes the services untestable in isolation.

#### File 1: `f1_api/features/leagues/application/services.py`

- Line ~75: `from f1_api.features.market.application.use_cases import InitializeLeagueOwnershipUseCase` (inside `CreateLeagueService.execute()`)
- Line ~90: `from f1_api.features.market.application.use_cases import InitializeUserTeamUseCase` (inside `CreateLeagueService.execute()`)
- Line ~181: `from f1_api.features.market.application.use_cases import InitializeUserTeamUseCase` (inside `JoinLeagueService.execute()`)

#### File 2: `f1_api/features/user_teams/application/services.py`

- Line ~214: `from f1_api.features.user_teams.domain.models import UserTeams` (inside `GetAllUserTeamsService.execute()`)
- Line ~267: `from f1_api.features.user_teams.domain.models import UserTeams` (inside `SwapReserveDriverService.execute()`)

### Fix

**Step 1** — Fix `f1_api/features/user_teams/application/services.py`: Move the two inline `from f1_api.features.user_teams.domain.models import UserTeams` lines to the top-level imports block. This is a pure intra-feature import with no circular dependency — the inline placement was unnecessary.

**Step 2** — Fix `f1_api/features/leagues/application/services.py` circular dependency properly:

Read the file fully first. The circular chain is:
`leagues.application.services` → `market.application.use_cases` → `leagues.infrastructure` (or back to leagues somehow).

To break the cycle without inline imports, inject the use cases as constructor arguments typed against a Protocol:

2a. In `f1_api/features/leagues/domain/interfaces.py`, add two new Protocol stubs:
```python
from typing import Protocol

class IInitializeLeagueOwnershipUseCase(Protocol):
    def execute(self, league_id: int, season: int) -> int: ...

class IInitializeUserTeamUseCase(Protocol):
    def execute(self, user_id: int, league_id: int) -> dict: ...
```

2b. Update `CreateLeagueService.__init__` to accept optional parameters:
```python
def __init__(self, league_repo, user_repo, membership_repo, session,
             initialize_ownership=None, initialize_user_team=None):
    ...
    self.initialize_ownership = initialize_ownership
    self.initialize_user_team = initialize_user_team
```

2c. In `CreateLeagueService.execute()`, replace the inline imports with `self.initialize_ownership` / `self.initialize_user_team` calls. If `None`, fall back to importing lazily (preserve runtime behaviour while making injection possible for tests).

2d. Apply the same pattern to `JoinLeagueService`.

2e. Update `f1_api/features/leagues/presentation/routes.py` to pass the concrete use-case instances when constructing `CreateLeagueService` and `JoinLeagueService` (import at route level where there's no circular risk).

**Step 3** — Verify: after changes, running:
```powershell
Get-ChildItem "c:\Users\Marc\Documents\ITA\Grid Fans\f1_api" -Recurse -Filter "*.py" |
  Where-Object { $_.FullName -notlike "*__pycache__*" -and $_.FullName -like "*application*" } |
  Select-String "^\s+from f1_api\."
```
should return zero results.
````
