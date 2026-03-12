# DDD Fix – Phase 6c: Fix self-wiring and concrete imports in market initialization use cases

## Context

Stack: Python 3.12, FastAPI, SQLModel. Workspace root: `c:\Users\Marc\Documents\ITA\Grid Fans`. `.venv` is at `f1_api/.venv`. All imports use the `f1_api.` prefix.

Phases 6a and 6b are complete. This phase targets two initialization use cases that violate DI by constructing their own repositories inside `__init__`, and four query use cases that accept the concrete `DriversRepository` class instead of the `DriversRepository` Protocol from the domain.

---

## Problem A — Self-constructing use cases

### `features/market/application/use_cases/initialize_league_ownership.py`

```python
def __init__(self, session: Session):
    self.session = session
    self.ownership_repo = OwnershipRepository(session)         # ← builds its own repo
```

It also constructs a `DriversRepository` inside `execute()`:
```python
drivers_repo = DriversRepository(self.session, season_year)   # ← inside execute()
```

### `features/market/application/use_cases/initialize_user_team.py`

```python
def __init__(self, session: Session):
    self.session = session
    self.ownership_repo = OwnershipRepository(session)            # ← builds its own repo
    self.transactions_repo = MarketTransactionsRepository(session) # ← builds its own repo
    self.user_teams_repo = UserTeamsRepositoryImpl(session)        # ← builds its own repo
    self.drivers_repo = DriversRepository(session, CURRENT_SEASON) # ← builds its own repo
```

---

## Problem B — Query use cases accept concrete `DriversRepository`

The `DriversRepository` Protocol already exists at `f1_api/features/drivers/domain/interfaces.py`. Four use cases import the concrete class instead:

```
features/market/application/use_cases/get_free_drivers.py        L6
features/market/application/use_cases/get_drivers_for_sale.py    L6
features/market/application/use_cases/get_user_drivers.py        L6
features/market/application/use_cases/initialize_league_ownership.py  L9
```

Each contains:
```python
from f1_api.features.drivers.infrastructure.persistence import DriversRepository
```

`get_drivers_for_sale.py` also has:
```python
from f1_api.features.user.infrastructure.repositories import UserRepositoryImpl  # L9
```
A `UserRepository` Protocol already exists at `f1_api/features/user/domain/interfaces.py`.

---

## Fix

### Step 1 — Fix query use cases (Problem B): `get_free_drivers`, `get_drivers_for_sale`, `get_user_drivers`

For each file, replace:
```python
from f1_api.features.drivers.infrastructure.persistence import DriversRepository
```
with:
```python
from f1_api.features.drivers.domain.interfaces import DriversRepository
```

For `get_drivers_for_sale.py` also replace:
```python
from f1_api.features.user.infrastructure.repositories import UserRepositoryImpl
```
with:
```python
from f1_api.features.user.domain.interfaces import UserRepository
```
and update the `__init__` type hint from `UserRepositoryImpl` to `UserRepository`.

---

### Step 2 — Fix `InitializeLeagueOwnershipUseCase`

**Read the file in full first** to get exact signatures.

The fix: accept repos via constructor instead of building them; accept a `DriversRepository` Protocol rather than constructing one inside `execute()`.

Target `__init__` signature:
```python
from f1_api.features.market.domain.interfaces import IOwnershipRepository
from f1_api.features.drivers.domain.interfaces import DriversRepository as IDriversRepository

def __init__(
    self,
    ownership_repo: IOwnershipRepository,
    drivers_repo: IDriversRepository,
):
    self.ownership_repo = ownership_repo
    self.drivers_repo = drivers_repo
```

Remove the `session: Session` parameter entirely. Remove internal `OwnershipRepository(session)` construction. Replace `DriversRepository(self.session, season_year)` inside `execute()` with `self.drivers_repo`.

> **Note**: `DriversRepository` in `drivers/domain/interfaces.py` does **not** take `season: int` in `__init__` because it's a Protocol — the concrete class does. The caller (routes layer) passes a pre-constructed `DriversRepository(session, season_year)`.

---

### Step 3 — Fix `InitializeUserTeamUseCase`

**Read the file in full first.**

Target `__init__` signature:
```python
from f1_api.features.market.domain.interfaces import IOwnershipRepository, ITransactionRepository
from f1_api.features.user_teams.domain.interfaces import UserTeamsRepository
from f1_api.features.drivers.domain.interfaces import DriversRepository as IDriversRepository

def __init__(
    self,
    ownership_repo: IOwnershipRepository,
    transactions_repo: ITransactionRepository,
    user_teams_repo: UserTeamsRepository,
    drivers_repo: IDriversRepository,
):
    self.ownership_repo = ownership_repo
    self.transactions_repo = transactions_repo
    self.user_teams_repo = user_teams_repo
    self.drivers_repo = drivers_repo
```

Remove the `session: Session` parameter. Remove all internal repo construction. Remove imports of concrete classes (`OwnershipRepository`, `MarketTransactionsRepository`, `UserTeamsRepositoryImpl`, `DriversRepository` from infrastructure). Also remove the `DriverOwnershipModel` and `MarketTransactionModel` imports from infrastructure if they are only used as return type annotations — check if domain entity equivalents exist in `market/domain/entities/`.

> **Note on `MarketTransactionsRepository`**: Check whether a domain Protocol exists for it. If not, add one to `features/leagues/domain/interfaces.py` (it is a market-transactions concern sitting under leagues infrastructure currently) before updating this use case.

---

### Step 4 — Update callers

The callers that construct these use cases are:

1. `features/leagues/application/services.py` — `CreateLeagueService.__init__` accepts injected `IInitializeLeagueOwnershipUseCase` and `IInitializeUserTeamUseCase`; the concrete instances are built in the routes layer.
2. `features/leagues/presentation/routes.py` — currently instantiates both use cases as:
   ```python
   InitializeLeagueOwnershipUseCase(session)
   InitializeUserTeamUseCase(session)
   ```
   After the fix these need repos passed in:
   ```python
   CURRENT_SEASON = 2025
   InitializeLeagueOwnershipUseCase(
       ownership_repo=OwnershipRepository(session),
       drivers_repo=DriversRepository(session, CURRENT_SEASON),
   )
   InitializeUserTeamUseCase(
       ownership_repo=OwnershipRepository(session),
       transactions_repo=MarketTransactionsRepository(session),
       user_teams_repo=UserTeamsRepositoryImpl(session),
       drivers_repo=DriversRepository(session, CURRENT_SEASON),
   )
   ```
   Add the missing infrastructure imports at the top of routes.py.

---

### Step 5 — Verify

```powershell
Get-ChildItem "c:\Users\Marc\Documents\ITA\Grid Fans\f1_api\features\market\application" -Recurse -Filter "*.py" |
  Where-Object { $_.FullName -notlike "*__pycache__*" } |
  Select-String "from f1_api.*infrastructure" |
  Select-Object @{N="File";E={$_.Path.Replace("C:\Users\Marc\Documents\ITA\Grid Fans\f1_api\","")}}, LineNumber, @{N="Line";E={$_.Line.Trim()}}
```

Should return zero results. Then:

```powershell
cd "c:\Users\Marc\Documents\ITA\Grid Fans\f1_api"
& ".\.venv\Scripts\python.exe" -c "import sys; sys.path.insert(0, '..'); from f1_api.main import app; print('OK')"
```
