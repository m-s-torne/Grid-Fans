# Archivos Legacy Pendientes de Eliminación

Este documento lista los archivos legacy que pueden ser eliminados de forma segura una vez completada la migración a DDD.

## ✅ User Feature - Completamente Migrado

### Archivos a eliminar:

- [x] **f1_api/routers/users_router.py**
  - **Razón**: Reemplazado por `features/user/presentation/routes.py`
  - **Verificación**: No referenciado en `main.py` ni en ningún otro archivo
  - **Estado**: ✅ Seguro eliminar

- [x] **f1_api/controllers/user/user_controller.py**
  - **Razón**: Lógica migrada a `features/user/application/services.py`
  - **Verificación**: No referenciado en ningún archivo del proyecto
  - **Estado**: ✅ Seguro eliminar

- [x] **f1_api/controllers/user/__init__.py**
  - **Razón**: Solo exporta funciones legacy no usadas
  - **Verificación**: Verificar que no se importe desde controllers.user
  - **Estado**: ⚠️ Revisar antes de eliminar (puede tener exports de user_teams_controller_new)

---

## ⏳ Leagues Feature - Parcialmente Migrado

### Archivos a eliminar (después de completar migración):

- [ ] **f1_api/routers/leagues_router.py**
  - **Razón**: Será reemplazado por `features/leagues/presentation/routes.py`
  - **Estado actual**: 🔄 En uso como "leagues_router_legacy"
  - **Endpoints pendientes de migrar**: 
    - GET `/leagues/{id}` (get by ID)
    - DELETE `/leagues/{id}/leave` (leave league)
    - GET `/leagues/{id}/participants` (get participants)
    - 30+ market endpoints
    - Team endpoints
  - **Estado**: ❌ NO eliminar hasta completar migración

- [ ] **f1_api/controllers/leagues/league_controller.py**
  - **Razón**: Lógica será migrada a `features/leagues/application/services.py`
  - **Estado actual**: 🔄 En uso por leagues_router_legacy
  - **Estado**: ❌ NO eliminar hasta completar migración

---

## � User Teams Feature - Completamente Migrado a DDD

### Archivos a eliminar:

- [ ] **f1_api/routers/user_teams_router.py**
  - **Razón**: Reemplazado por `features/user_teams/presentation/routes.py`
  - **Verificación**: Registrado en main.py como "user_teams_router_legacy"
  - **Endpoints migrados**:
    - POST `/user-teams/leagues/{league_id}/teams` (create/update team)
    - GET `/user-teams/leagues/{league_id}/teams/me` (get my team)
  - **Estado**: ⚠️ Revisar que endpoints DDD funcionen antes de eliminar

- [ ] **f1_api/features/user_teams/controllers.py**
  - **Razón**: Lógica migrada a `features/user_teams/application/services.py`
  - **Verificación**: No debería estar referenciado después de migración
  - **Métodos migrados**:
    - create_or_update_team → CreateOrUpdateTeamService
    - get_my_team → GetMyTeamService
    - swap_reserve_driver → SwapReserveDriverService
  - **Estado**: ⚠️ Revisar referencias antes de eliminar

- [ ] **f1_api/controllers/user/user_teams_controller_new.py**
  - **Razón**: Duplicado de `features/user_teams/controllers.py`, toda lógica migrada a DDD
  - **Verificación**: Verificar que no se importe desde ningún archivo
  - **Funciones migradas**:
    - get_my_teams_service → GetAllMyTeamsService (usado ahora en /users/my-teams DDD)
    - swap_reserve_driver → SwapReserveDriverService
  - **Estado**: ⚠️ Revisar referencias antes de eliminar

- [ ] **f1_api/features/user_teams/models.py**
  - **Razón**: Modelos migrados a `features/user_teams/domain/models.py` y DTOs a `application/dtos.py`
  - **Verificación**: Verificar imports en todo el proyecto
  - **Estado**: ⚠️ Revisar referencias antes de eliminar

- [ ] **f1_api/models/repositories/user_teams_repository.py**
  - **Razón**: Lógica migrada a `features/user_teams/infrastructure/repositories.py`
  - **Verificación**: Verificar que no se importe desde ningún archivo
  - **Estado**: ⚠️ Revisar referencias antes de eliminar

---

## �📋 Otros Features - No Migrados

### Teams Feature
- **Estado**: ❌ No migrado a DDD
- **Archivos**: Mantener todos hasta migración

### Market Feature  
- **Estado**: ❌ No migrado a DDD
- **Archivos**: Mantener todos hasta migración

### Drivers Feature
- **Estado**: ❌ No migrado a DDD
- **Archivos**: Mantener todos hasta migración

---

## 📝 Notas

### Criterios para eliminación segura:
1. ✅ Feature completamente migrado a DDD
2. ✅ Todos los endpoints servidos desde `features/*/presentation/routes.py`
3. ✅ No hay imports del archivo legacy en ninguna parte del proyecto
4. ✅ Tests pasando (cuando existan)

### Proceso de eliminación:
1. Verificar con `grep` que no hay referencias
2. Comentar el import en archivos relevantes
3. Probar que el servidor arranca y funciona
4. Eliminar archivo
5. Commit con mensaje descriptivo

---

**Última actualización**: 16 de diciembre de 2025
