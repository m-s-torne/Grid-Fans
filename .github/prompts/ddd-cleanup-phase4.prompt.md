# DDD Cleanup – Phase 4: Consolidate misplaced TeamsRepository and add missing domain interfaces

## Context

Stack: Python 3.12, FastAPI, SQLModel. Workspace root: `c:\Users\Marc\Documents\ITA\Grid Fans`. `.venv` is at `f1_api/.venv`. All imports use the `f1_api.` prefix.

The DDD migration is structurally complete: `models/` is fully deleted, all 7 features use the domain/application/infrastructure/presentation layout, and `main.py` registers only DDD routers. Two architectural rough edges remain:

---

## Rough Edge 1 — `TeamsRepository` is misplaced in the `drivers` feature

### Problem

`f1_api/features/drivers/infrastructure/persistence/teams_repository.py` contains a `TeamsRepository` class that queries `Teams`, `DriverTeamLink`, and `SessionResult`. It is exported from `features/drivers/infrastructure/persistence/__init__.py` alongside `DriversRepository` and is imported in 8 files via:

```python
from f1_api.features.drivers.infrastructure.persistence import TeamsRepository
```

Consumer files:
- `f1_api/core/f1_data/application/driver_team_link_reconciliation.py`
- `f1_api/core/f1_data/application/driver_team_link_service.py`
- `f1_api/features/admin/infrastructure/data_ingestion.py`
- `f1_api/features/drivers/application/services.py`
- `f1_api/features/drivers/presentation/routes.py`
- `f1_api/features/leagues/presentation/routes.py` (imported 3 times in the same file)
- `f1_api/features/market/application/use_cases/get_drivers_for_sale.py`
- `f1_api/features/market/application/use_cases/get_free_drivers.py`
- `f1_api/features/market/application/use_cases/get_user_drivers.py`
- `f1_api/features/market/application/use_cases/initialize_league_ownership.py`
- `f1_api/features/market/application/use_cases/initialize_user_team.py`

Meanwhile `f1_api/features/teams/infrastructure/repositories.py` already has `TeamsRepositoryImpl` with `get_all_teams()` and `get_team_points_data()`. The misplaced class adds two extra methods: `get_team_id_map()` and `get_existing_teams()`.

### Fix

**Step 1** — Read `f1_api/features/drivers/infrastructure/persistence/teams_repository.py` in full.

**Step 2** — Merge `get_team_id_map()` and `get_existing_teams()` into `f1_api/features/teams/infrastructure/repositories.py` (the `TeamsRepositoryImpl` class). Do not alter existing methods; add the two missing ones at the bottom of the class.

**Step 3** — Update `f1_api/features/teams/infrastructure/repositories.py` exports: rename the class to `TeamsRepository` (drop the `Impl` suffix) so all existing callers of the misplaced class can point here without a name change. Update the module docstring accordingly.

**Step 4** — Update `f1_api/features/teams/domain/interfaces.py`: the `TeamsRepository` protocol currently only declares `get_all_teams()` and `get_team_points_data()`. Add protocol stubs for `get_team_id_map()` and `get_existing_teams()` to keep the interface complete.

**Step 5** — Update all imports that currently use `from f1_api.features.drivers.infrastructure.persistence import TeamsRepository` to instead use:
```python
from f1_api.features.teams.infrastructure.repositories import TeamsRepository
```
This applies to all consumer files listed above.

**Step 6** — Remove `teams_repository.py` from drivers:
```powershell
Remove-Item "c:\Users\Marc\Documents\ITA\Grid Fans\f1_api\features\drivers\infrastructure\persistence\teams_repository.py" -Force
```

**Step 7** — Update `f1_api/features/drivers/infrastructure/persistence/__init__.py` to remove the `TeamsRepository` export:
```python
# Remove:
from .teams_repository import TeamsRepository
# And remove "TeamsRepository" from __all__
```

---

## Rough Edge 2 — `DriverTeamLinkRepository` has no domain interface

### Problem

`f1_api/core/f1_data/infrastructure/persistence/driver_team_link_repository.py` contains `DriverTeamLinkRepository` with one public method:

```python
def get_existing_links(self) -> set[tuple]:
    ...
```

There is no protocol/interface for it. `core/f1_data/domain/interfaces.py` does not exist.

### Fix

**Step 1** — Create `f1_api/core/f1_data/domain/interfaces.py`:
```python
"""Core F1 data domain interfaces."""
from typing import Protocol


class DriverTeamLinkRepository(Protocol):
    """Repository interface for DriverTeamLink persistence operations."""

    def get_existing_links(self) -> set[tuple]:
        """
        Get set of (driver_id, team_id, round_number) tuples for all existing links.
        Used as a guard to avoid duplicate inserts during ingestion.
        """
        ...
```

No callers need updating — this is purely additive.

---

## Validation (after all steps)

```powershell
cd "c:\Users\Marc\Documents\ITA\Grid Fans\f1_api"
& ".\.venv\Scripts\python.exe" -c "import sys; sys.path.insert(0, '..'); from f1_api.main import app; print('OK')"
```

Must print `OK`.

Also run a grep check after Rough Edge 1:
```powershell
Get-ChildItem -Path "c:\Users\Marc\Documents\ITA\Grid Fans\f1_api" -Recurse -Filter "*.py" |
  Select-String "from f1_api.features.drivers.infrastructure.persistence import TeamsRepository" |
  Where-Object { $_.Path -notlike "*__pycache__*" }
```

Must return zero matches.

---

## What is NOT changing

- `f1_api/features/drivers/infrastructure/persistence/drivers_repository.py` — stays as is
- `f1_api/features/teams/application/services.py` — stays as is (uses `TeamsRepository` protocol from domain interfaces, already correct)
- `f1_api/features/teams/presentation/routes.py` — stays as is
- All market, user, user_teams, admin, leagues features — no structural changes beyond import updates for Rough Edge 1
- `f1_api/config/sql_init.py` — no changes needed
- Frontend code — not in scope
