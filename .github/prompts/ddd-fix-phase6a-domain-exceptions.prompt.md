# DDD Fix – Phase 6a: Remove `HTTPException` from the domain layer

## Context

Stack: Python 3.12, FastAPI, SQLModel. Workspace root: `c:\Users\Marc\Documents\ITA\Grid Fans`. `.venv` is at `f1_api/.venv`. All imports use the `f1_api.` prefix.

`HTTPException` is a FastAPI presentation-layer concern. Raising it inside a domain service couples the domain to the web framework, making the domain untestable without a running FastAPI application and violating the Dependency Inversion Principle.

---

## Problem

`f1_api/features/user_teams/domain/services.py` imports and raises `HTTPException` in three places:

```python
from fastapi import HTTPException
...
raise HTTPException(status_code=400, detail="All drivers must be unique")
raise HTTPException(400, "Driver is already in reserve slot")
raise HTTPException(400, "Driver not found in team")
```

The domain must not know about HTTP. It should raise plain Python exceptions; the presentation layer converts them.

---

## Fix

### Step 1 — Create a domain exceptions module

Create `f1_api/features/user_teams/domain/exceptions.py`:

```python
"""User Teams domain exceptions."""


class DuplicateDriverError(ValueError):
    """Raised when the same driver appears in more than one team slot."""


class DriverNotInTeamError(ValueError):
    """Raised when a requested driver is not found in the team."""


class DriverAlreadyReserveError(ValueError):
    """Raised when the driver to swap is already the reserve driver."""
```

### Step 2 — Update `domain/services.py`

- Remove `from fastapi import HTTPException`
- Add `from f1_api.features.user_teams.domain.exceptions import DuplicateDriverError, DriverNotInTeamError, DriverAlreadyReserveError`
- Replace each `raise HTTPException(...)` with the appropriate domain exception:

| Old | New |
|-----|-----|
| `raise HTTPException(status_code=400, detail="All drivers must be unique")` | `raise DuplicateDriverError("All drivers must be unique")` |
| `raise HTTPException(400, "Driver is already in reserve slot")` | `raise DriverAlreadyReserveError("Driver is already in reserve slot")` |
| `raise HTTPException(400, "Driver not found in team")` | `raise DriverNotInTeamError("Driver not found in team")` |

### Step 3 — Update callers in the application / presentation layers

Search for all places that call the domain services and catch `HTTPException` from them. Wrap the domain exceptions into `HTTPException` at the presentation level instead.

```powershell
Get-ChildItem "c:\Users\Marc\Documents\ITA\Grid Fans\f1_api" -Recurse -Filter "*.py" |
  Where-Object { $_.FullName -notlike "*__pycache__*" } |
  Select-String "validate_unique_drivers|validate_driver_in_team" |
  Select-Object @{N="File";E={$_.Path.Replace("C:\Users\Marc\Documents\ITA\Grid Fans\f1_api\","")}}, LineNumber, @{N="Line";E={$_.Line.Trim()}}
```

For each caller in an application service, add a `try/except` that catches the domain exception and re-raises as `HTTPException`. The pattern:

```python
from f1_api.features.user_teams.domain.exceptions import DuplicateDriverError, DriverNotInTeamError

try:
    self.validation_service.validate_unique_drivers(...)
except DuplicateDriverError as e:
    raise HTTPException(status_code=400, detail=str(e)) from e
```

### Step 4 — Verify

```powershell
Get-ChildItem "c:\Users\Marc\Documents\ITA\Grid Fans\f1_api" -Recurse -Filter "*.py" |
  Where-Object { $_.FullName -notlike "*__pycache__*" -and $_.FullName -like "*domain*" } |
  Select-String "HTTPException" |
  Select-Object @{N="File";E={$_.Path.Replace("C:\Users\Marc\Documents\ITA\Grid Fans\f1_api\","")}}, LineNumber, @{N="Line";E={$_.Line.Trim()}}
```

Should return zero results.

Then confirm the app still loads:

```powershell
cd "c:\Users\Marc\Documents\ITA\Grid Fans\f1_api"
& ".\.venv\Scripts\python.exe" -c "import sys; sys.path.insert(0, '..'); from f1_api.main import app; print('OK')"
```
