# DDD Fix – Phase 6d: Fix DIP violations in `admin/application/` and `core/f1_data/application/`

## Context

Stack: Python 3.12, FastAPI, SQLModel. Workspace root: `c:\Users\Marc\Documents\ITA\Grid Fans`. `.venv` is at `f1_api/.venv`. All imports use the `f1_api.` prefix.

Phases 6a–6c are complete. This is the final DIP-cleanup phase. Two areas remain where the application layer imports directly from infrastructure:

1. `features/admin/application/services.py` — imports four infrastructure functions from `data_ingestion.py`
2. `core/f1_data/application/driver_team_link_service.py` and `core/f1_data/application/driver_team_link_reconciliation.py` — construct concrete repos inline

After this phase, **no application-layer file should import from any `*.infrastructure.*` path** (except the `features/leagues/application/services.py` import of `UserTeamsRepositoryImpl` which is used only for type passthrough in `LeaveLeagueService` and is intentional).

---

## Part 1 — `features/admin/application/services.py`

### Problem

```python
from f1_api.features.admin.infrastructure.data_ingestion import (
    get_session_results,
    get_team_data,
    get_event_data,
    get_session_data,
)
```

`UpdateSeasonService.execute()` calls these four functions directly. The domain interfaces were already created in Phase 5 at `f1_api/features/admin/domain/interfaces.py`:

```python
class IGetEventData(Protocol):
    def __call__(self, session: Session, year: int) -> list[Events]: ...

class IGetSessionData(Protocol):
    def __call__(self, session: Session, year: int) -> list[Sessions]: ...

class IGetSessionResults(Protocol):
    def __call__(self, year: int, session: Session) -> list[SessionResult]: ...

class IGetTeamData(Protocol):
    def __call__(self, session: Session) -> list[Teams]: ...
```

### Fix

**Step 1** — Read `features/admin/application/services.py` and `features/admin/presentation/routes.py` in full.

**Step 2** — Update `UpdateSeasonService.__init__` to accept the four callables as optional constructor parameters (defaulting to `None`, resolved to concrete functions in the routes layer):

```python
from f1_api.features.admin.domain.interfaces import (
    IGetEventData, IGetSessionData, IGetSessionResults, IGetTeamData,
)

class UpdateSeasonService:
    def __init__(
        self,
        engine,
        get_event_data: IGetEventData | None = None,
        get_session_data: IGetSessionData | None = None,
        get_session_results: IGetSessionResults | None = None,
        get_team_data: IGetTeamData | None = None,
    ):
        self.engine = engine
        self._get_event_data = get_event_data
        self._get_session_data = get_session_data
        self._get_session_results = get_session_results
        self._get_team_data = get_team_data
```

**Step 3** — Inside `execute()`, replace every direct call `get_event_data(session, year)` with `self._get_event_data(session, year)`. Add `assert self._get_event_data is not None` guards (same pattern used in `leagues/application/services.py`).

**Step 4** — Remove the `from f1_api.features.admin.infrastructure.data_ingestion import (...)` import block from `services.py`.

**Step 5** — Update the routes layer (`features/admin/presentation/routes.py`) to import the concrete functions and pass them in:

```python
from f1_api.features.admin.infrastructure.data_ingestion import (
    get_event_data, get_session_data, get_session_results, get_team_data,
)
...
service = UpdateSeasonService(
    engine,
    get_event_data=get_event_data,
    get_session_data=get_session_data,
    get_session_results=get_session_results,
    get_team_data=get_team_data,
)
```

---

## Part 2 — `core/f1_data/application/driver_team_link_service.py`

### Problem

`DriverTeamLinkController.__init__` constructs three repos directly:

```python
self.driver_repository = DriversRepository(session, year)        # concrete
self.team_repository = TeamsRepository(session)                  # concrete
self.repository = DriverTeamLinkRepository(session)              # concrete
```

### Fix

**Step 1** — Read `core/f1_data/application/driver_team_link_service.py` in full.

**Step 2** — Check whether a Protocol for `DriverTeamLinkRepository` exists in `core/f1_data/domain/`. If not, create `f1_api/core/f1_data/domain/interfaces.py` with a stub:

```python
from typing import Protocol
from f1_api.features.drivers.domain.models import DriverTeamLink

class IDriverTeamLinkRepository(Protocol):
    def get_existing_links(self) -> set: ...
    def add(self, link: DriverTeamLink) -> None: ...
```

Read the concrete `DriverTeamLinkRepository` first to get exact method signatures.

**Step 3** — Update `DriverTeamLinkController.__init__` to accept repos via constructor injection:

```python
from f1_api.features.drivers.domain.interfaces import DriversRepository as IDriversRepository
from f1_api.features.teams.domain.interfaces import TeamsRepository as ITeamsRepository
from f1_api.core.f1_data.domain.interfaces import IDriverTeamLinkRepository

class DriverTeamLinkController:
    def __init__(
        self,
        driver_repository: IDriversRepository,
        team_repository: ITeamsRepository,
        repository: IDriverTeamLinkRepository,
        season_context: ...,   # use the existing SeasonContextController type
    ):
        self.driver_repository = driver_repository
        self.team_repository = team_repository
        self.repository = repository
        self.season_context = season_context
```

**Step 4** — Find all callers of `DriverTeamLinkController(session, year)` and update them to pass pre-constructed repos. The caller is the free function `get_all_driver_team_links` in the same file — update its signature to accept and pass through the repos, or construct them there since it is already in the application layer being called from `admin/application/services.py`.

---

## Part 3 — `core/f1_data/application/driver_team_link_reconciliation.py`

### Problem

`reconcile_driver_team_links(session, year)` constructs four repos inline:

```python
driver_repo = DriversRepository(session, year)           # concrete
team_repo = TeamsRepository(session)                     # concrete
link_repo = DriverTeamLinkRepository(session)            # concrete
```

### Fix

**Step 1** — Read the file in full.

**Step 2** — Change the function signature to accept repos and season context as parameters:

```python
async def reconcile_driver_team_links(
    session: Session,
    year: int,
    driver_repo: IDriversRepository,
    team_repo: ITeamsRepository,
    link_repo: IDriverTeamLinkRepository,
):
```

Remove internal repo construction. All repos are now passed in from outside.

**Step 3** — Update the caller (`features/admin/application/services.py` calls `reconcile_driver_team_links(session, year)`) to construct and pass the repos. Since that caller is itself being fixed in Part 1 above, construct the repos at the same point as the other infrastructure dependencies — either by adding them to the `IGetSessionResults`-style injection pattern, or by constructing them directly inside the routes layer and passing them via the service.

The simplest acceptable approach: construct the repos inside `UpdateSeasonService.execute()` using `self.engine` (consistent with how it creates sessions), since these reconciliation repos are purely administrative and don't require injection for testing purposes. This is a pragmatic trade-off — document it with a comment.

---

## Verification

After all changes:

```powershell
Get-ChildItem "c:\Users\Marc\Documents\ITA\Grid Fans\f1_api" -Recurse -Filter "*.py" |
  Where-Object { $_.FullName -notlike "*__pycache__*" -and $_.FullName -notlike "*.venv*" } |
  Select-String "from f1_api.*infrastructure" |
  Where-Object { $_.Path -like "*application*" -or $_.Path -like "*\domain\*" } |
  Select-Object @{N="File";E={$_.Path.Replace("C:\Users\Marc\Documents\ITA\Grid Fans\f1_api\","")}}, LineNumber, @{N="Line";E={$_.Line.Trim()}} |
  Format-Table -AutoSize
```

Should return zero results (or only the `features/leagues/application/services.py` `UserTeamsRepositoryImpl` import if that intentional reference remains). Then:

```powershell
cd "c:\Users\Marc\Documents\ITA\Grid Fans\f1_api"
& ".\.venv\Scripts\python.exe" -c "import sys; sys.path.insert(0, '..'); from f1_api.main import app; print('OK')"
```
