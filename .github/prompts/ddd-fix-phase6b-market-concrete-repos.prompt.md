# DDD Fix – Phase 6b: Replace concrete `UserTeamsRepositoryImpl` with Protocol in market use cases

## Context

Stack: Python 3.12, FastAPI, SQLModel. Workspace root: `c:\Users\Marc\Documents\ITA\Grid Fans`. `.venv` is at `f1_api/.venv`. All imports use the `f1_api.` prefix.

Phase 6a is complete. Application-layer use cases must depend on **abstractions (Protocols)**, not on concrete infrastructure classes. The `UserTeamsRepository` Protocol already exists at `f1_api/features/user_teams/domain/interfaces.py`. Three market use cases bypass it and accept the concrete `UserTeamsRepositoryImpl` instead.

---

## Problem

The following three files import and type-hint against the concrete class:

```
features/market/application/use_cases/purchase_driver.py     L19
features/market/application/use_cases/purchase_from_user.py  L19
features/market/application/use_cases/sell_to_market.py      L15
```

Each contains:
```python
from f1_api.features.user_teams.infrastructure.repositories import UserTeamsRepositoryImpl
```

And uses `UserTeamsRepositoryImpl` as the type in `__init__`:
```python
def __init__(self, ownership_repo, transaction_repo, user_teams_repo: UserTeamsRepositoryImpl):
```

The `UserTeamsRepository` Protocol in `user_teams/domain/interfaces.py` already declares all the methods these use cases need (`get_by_league_and_user`, `update`).

---

## Fix

**For each of the three files** (`purchase_driver.py`, `purchase_from_user.py`, `sell_to_market.py`):

**Step 1** — Replace the infrastructure import:
```python
# Remove:
from f1_api.features.user_teams.infrastructure.repositories import UserTeamsRepositoryImpl

# Add:
from f1_api.features.user_teams.domain.interfaces import UserTeamsRepository
```

**Step 2** — Update the `__init__` type hint:
```python
# Change:
user_teams_repo: UserTeamsRepositoryImpl

# To:
user_teams_repo: UserTeamsRepository
```

**Step 3** — Check the `UserTeamsRepository` Protocol has every method these use cases call. Read each use case to find all `self.user_teams_repo.<method>` calls. The current Protocol stubs are:
- `get_by_id`
- `get_by_league_and_user`
- `has_active_team`
- `create`
- `update`
- `soft_delete`
- `hard_delete`

If any called method is missing from the Protocol, **add it to `user_teams/domain/interfaces.py`** before updating the use cases.

**Step 4** — Confirm the infrastructure class still satisfies the Protocol (no action needed — structural typing handles this automatically).

**Step 5** — Verify no remaining concrete imports in market use cases:

```powershell
Get-ChildItem "c:\Users\Marc\Documents\ITA\Grid Fans\f1_api\features\market" -Recurse -Filter "*.py" |
  Where-Object { $_.FullName -notlike "*__pycache__*" } |
  Select-String "infrastructure.*repositories.*import" |
  Select-Object @{N="File";E={$_.Path.Replace("C:\Users\Marc\Documents\ITA\Grid Fans\f1_api\","")}}, LineNumber, @{N="Line";E={$_.Line.Trim()}}
```

Then confirm app loads:

```powershell
cd "c:\Users\Marc\Documents\ITA\Grid Fans\f1_api"
& ".\.venv\Scripts\python.exe" -c "import sys; sys.path.insert(0, '..'); from f1_api.main import app; print('OK')"
```
