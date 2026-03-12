# User Teams DDD Migration - Complete

## ✅ Migration Status: COMPLETED

Fecha: 16 de diciembre de 2025

---

## 📁 Estructura DDD Creada

```
features/user_teams/
├── domain/
│   ├── __init__.py          ✅ Creado
│   ├── models.py            ✅ UserTeams entity con constraints
│   └── interfaces.py        ✅ UserTeamsRepository Protocol (7 métodos)
│
├── application/
│   ├── __init__.py          ✅ Creado
│   ├── dtos.py              ✅ 3 DTOs (Create, Update, Response)
│   └── services.py          ✅ 2 Services (CreateOrUpdate, GetMyTeam)
│
├── infrastructure/
│   ├── __init__.py          ✅ Creado
│   └── repositories.py      ✅ UserTeamsRepositoryImpl (implementa Protocol)
│
└── presentation/
    ├── __init__.py          ✅ Creado
    └── routes.py            ✅ 2 endpoints DDD
```

---

## 🎯 Endpoints Migrados

### 1. POST `/api/user-teams/leagues/{league_id}/teams`
- **Legacy**: `routers/user_teams_router.py::create_or_update_user_team`
- **DDD**: `features/user_teams/presentation/routes.py::create_or_update_team`
- **Service**: `CreateOrUpdateTeamService`
- **Lógica**:
  - Valida usuario existe y es miembro de la liga
  - Valida drivers únicos
  - Calcula presupuesto basado en precios de drivers/constructor
  - Crea nuevo team o actualiza existente

### 2. GET `/api/user-teams/leagues/{league_id}/teams/me`
- **Legacy**: `routers/user_teams_router.py::get_my_team`
- **DDD**: `features/user_teams/presentation/routes.py::get_my_team`
- **Service**: `GetMyTeamService`
- **Lógica**:
  - Valida usuario existe
  - Devuelve team activo o None

### 3. POST `/api/user-teams/leagues/{league_id}/teams/swap-reserve`
- **Legacy**: `routers/leagues_router.py::swap_reserve_driver`
- **DDD**: `features/user_teams/presentation/routes.py::swap_reserve_driver`
- **Service**: `SwapReserveDriverService`
- **Lógica**:
  - Identifica slot del driver a hacer reserva
  - Intercambia con el reserva actual
  - Actualiza timestamps

### 4. GET `/api/users/my-teams`
- **Legacy**: `controllers/user/user_teams_controller_new.py::get_my_teams_service`
- **DDD**: `features/user/presentation/routes.py::get_my_teams` (usando `GetAllMyTeamsService`)
- **Service**: `GetAllMyTeamsService`
- **Lógica**:
  - Obtiene TODOS los teams del usuario en todas las ligas
  - Enriquece con información de liga, drivers (headshots), constructor (logo)

---

## 🔧 Componentes Creados

### Domain Layer

#### **models.py** - UserTeams Entity
```python
class UserTeams(SQLModel, table=True):
    __tablename__ = "user_teams"
    
    # 12 campos:
    id, user_id, league_id, team_name,
    driver_1_id, driver_2_id, driver_3_id, reserve_driver_id,
    constructor_id, total_points, budget_remaining,
    is_active, created_at, updated_at
    
    # Constraint único: (user_id, league_id)
```

#### **interfaces.py** - UserTeamsRepository Protocol
```python
class UserTeamsRepository(Protocol):
    def get_by_id(team_id: int) -> UserTeams | None
    def get_by_league_and_user(league_id: int, user_id: int) -> UserTeams | None
    def has_active_team(league_id: int, user_id: int) -> bool
    def create(team_data: UserTeamCreateDTO) -> UserTeams
    def update(team_id: int, team_data: UserTeamUpdateDTO) -> UserTeams
    def soft_delete(team_id: int) -> bool
    def hard_delete(team_id: int) -> bool
```

### Application Layer

#### **dtos.py** - Data Transfer Objects
1. **UserTeamCreateDTO** (9 campos): Para creación (incluye reserve_driver_id y budget_remaining)
2. **UserTeamUpdateDTO** (6 campos): Para actualización con validación (añadido budget_remaining opcional)
3. **SwapReserveDriverDTO** (2 campos): Para swap request (user_id, driver_id)
4. **UserTeamResponseDTO** (14 campos): Para respuesta API

#### **services.py** - Business Logic
1. **CreateOrUpdateTeamService**:
   - Dependency injection: session, user_teams_repo, user_repo, league_link_repo
   - Calcula precio de drivers: `10M + (puntos × 10k) + (podios × 50k) + (victorias × 100k)`
   - Calcula presupuesto restante: `100M - (costos drivers + constructor)`
   - Crea o actualiza team según exista
   - Commits explícitos por operación

2. **GetMyTeamService**:
   - Dependency injection: user_teams_repo, user_repo
   - Validación de usuario
   - Retorna team o None

3. **GetAllMyTeamsService**:
   - Dependency injection: session, user_repo
   - Obtiene TODOS los teams activos del usuario
   - Enriquece con información de liga, drivers (headshots), constructor (logo)
   - Devuelve lista de diccionarios con datos completos

4. **SwapReserveDriverService**:
   - Dependency injection: session, user_teams_repo
   - Identifica slot del driver actual (1, 2, 3)
   - Intercambia con reserva actual
   - Commit explícito después del swap

### Infrastructure Layer

#### **repositories.py** - UserTeamsRepositoryImpl
- Implementa UserTeamsRepository Protocol
- 7 métodos concretos usando SQLModel
- Logging de operaciones
- Flush después de create para obtener ID
- Updated_at automático en updates

### Presentation Layer

#### **routes.py** - HTTP Endpoints
- Prefix: `/api/user-teams`
- Dependency injection para repositories
- Error handling con HTTPException
- Logging de operaciones
- Rollback en errores
- **3 endpoints**: create_or_update_team, get_my_team, swap_reserve_driver

---

## 🔄 Cambios en Archivos Existentes

### **main.py**
```python
# Imports
from f1_api.routers.user_teams_router import router as user_teams_router_legacy
from f1_api.features.user_teams.presentation.routes import router as user_teams_router

# Registros
app.include_router(user_teams_router, tags=["User Teams - DDD"])
app.include_router(user_teams_router_legacy, prefix="/api", tags=["User Teams - Legacy"])
```

### **features/user/presentation/routes.py**
- **Eliminado** import de `get_my_teams_service` desde controllers legacy
- **Añadido** import de `GetAllMyTeamsService` desde user_teams DDD
- **Actualizado** endpoint `/users/my-teams` para usar servicio DDD con dependency injection

### **issue_eliminate.md**
- Añadida sección "User Teams Feature - Completamente Migrado a DDD"
- Listados 4 archivos legacy para eliminar después de verificación:
  1. `routers/user_teams_router.py`
  2. `features/user_teams/controllers.py`
  3. `features/user_teams/models.py`
  4. `models/repositories/user_teams_repository.py`
- **AÑADIDO**: `controllers/user/user_teams_controller_new.py` (duplicado de controllers)

---

## 🎨 Patrones DDD Aplicados

### 1. **Separation of Concerns**
- Domain: Entidades y contratos (sin dependencias externas)
- Application: Lógica de negocio y orquestación
- Infrastructure: Implementación de persistencia
- Presentation: HTTP y serialización

### 2. **Dependency Inversion**
- Application depende de interfaces (Protocol), no implementaciones
- Infrastructure implementa interfaces de Domain
- Presentation inyecta dependencias via FastAPI Depends

### 3. **Repository Pattern**
- Interface en Domain layer
- Implementación en Infrastructure layer
- Abstrae lógica de persistencia

### 4. **Service Pattern**
- Servicios en Application layer
- Orquestan domain models y repositories
- Contienen reglas de negocio

### 5. **DTO Pattern**
- Separación entre entidades de dominio y API
- Validación en capa de presentación
- Transformación explícita entre capas

---

## 🧪 Verificación

### Compilación
- ✅ Sin errores en `main.py`
- ⚠️ Warnings de Pylance (relative imports) - son falsos positivos
- ⚠️ Warnings de logging formatting - no críticos

### Estructura
- ✅ Todos los archivos `__init__.py` creados
- ✅ Imports correctos entre capas
- ✅ Todos los módulos exportan lo necesario

---

## 📋 Próximos Pasos

### Antes de Eliminar Legacy:
1. ⚠️ **PROBAR** endpoints DDD funcionan correctamente:
   - POST team creation/update
   - GET my team
   - Validación de presupuesto
   - Validación de drivers únicos

2. ⚠️ **VERIFICAR** no hay imports de archivos legacy:
   ```bash
   grep -r "from f1_api.features.user_teams.controllers" .
   grep -r "from f1_api.features.user_teams.models" .
   grep -r "from f1_api.models.repositories.user_teams_repository" .
   grep -r "from f1_api.routers.user_teams_router" .
   ```

3. ⚠️ **ACTUALIZAR** frontend si usa endpoints legacy:
   - Cambiar rutas a nuevos endpoints DDD
   - Verificar contratos de DTOs

### Después de Verificación:
4. ✅ Eliminar archivos legacy listados en `issue_eliminate.md`
5. ✅ Eliminar imports de legacy en `main.py`
6. ✅ Commit con mensaje descriptivo

---

## 📝 Notas Técnicas

### Diferencias con Legacy Controller:

**Transaction Management**:
- Legacy: Context manager con auto-commit en `__exit__`
- DDD: Explicit commits en services después de operaciones

**Dependency Injection**:
- Legacy: Session pasado a constructor
- DDD: Session + repositories inyectados via FastAPI Depends

**Error Handling**:
- Legacy: HTTPException en controller
- DDD: HTTPException en services (lógica de negocio) + routes (HTTP layer)

**Budget Calculation**:
- Ambos usan misma fórmula (consistencia ✅)
- DDD usa logger.debug en vez de print

---

## ✅ Checklist de Migración

- [x] Domain models creados
- [x] Domain interfaces (Protocols) creados
- [x] Application DTOs creados (4 DTOs: Create, Update, Swap, Response)
- [x] Application services creados (4 Services)
- [x] Infrastructure repositories creados
- [x] Presentation routes creados (3 endpoints)
- [x] __init__.py modules creados
- [x] Registrado en main.py
- [x] issue_eliminate.md actualizado
- [x] Endpoint /users/my-teams migrado a DDD
- [x] Lógica de controllers completamente migrada
- [ ] Tests funcionando (PENDIENTE - probar manualmente)
- [ ] Frontend actualizado (PENDIENTE)
- [ ] Legacy files eliminados (PENDIENTE)

---

**Status**: ✅ Migración técnica 100% completa (incluyendo toda la lógica de controllers), pendiente de testing y eliminación de legacy
