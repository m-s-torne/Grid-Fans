# Issue: Cálculo incorrecto de Profit/Loss en "List for Sale"

## Descripción
El cálculo de profit/loss en el modal de "List for Sale" presenta un comportamiento erróneo cuando el usuario establece un precio de venta (asking price) superior al +20% del precio de adquisición.

## Comportamiento actual
- Cuando el asking price supera el +20% sobre el acquisition price, el **profit se convierte en loss**
- A medida que el usuario aumenta el asking price, el **loss aparente aumenta** en lugar de incrementar el profit
- Este comportamiento es claramente incorrecto desde la perspectiva de lógica de negocio

## Comportamiento esperado
- El profit debería aumentar proporcionalmente cuando el asking price supera el acquisition price
- No debería existir un punto de inflexión donde el profit se convierta en loss al aumentar el precio
- La fórmula de cálculo debería ser: `profit = asking_price - acquisition_price`

## Ubicación probable del error
- **Frontend**: Modal de "List for Sale" 
- **Componente**: Probablemente en `frontend/src/features/Market/` 
- **Cálculo**: La lógica de profit/loss calculation en el componente del modal

## Pasos para reproducir
1. Abrir el mercado de una liga
2. Seleccionar un piloto propio (My Drivers)
3. Hacer clic en "List for Sale"
4. Establecer un asking price del +20% sobre acquisition price → Verificar profit correcto
5. Aumentar el asking price por encima del +20% → **BUG**: El profit se convierte en loss
6. Continuar aumentando el asking price → **BUG**: El loss aparente aumenta

## Impacto
- **Severidad**: Media
- **Impacto UX**: Alto - Los usuarios no pueden calcular correctamente su ganancia potencial
- **Área afectada**: Market system - List for sale functionality

## Notas técnicas
Posibles causas:
- Error en la fórmula de cálculo (inversión de signos)
- Condición incorrecta en un if/else que maneja diferentes rangos de precios
- Uso incorrecto de valores absolutos o comparaciones
- Variable mal nombrada o intercambiada (profit/loss)

## Estado
- [ ] Identificado
- [ ] Investigado
- [ ] Corregido
- [ ] Testeado
- [ ] Desplegado

---
**Fecha de reporte**: 16 de diciembre de 2025  
**Reportado por**: Marc (Usuario)  
**Prioridad**: Media-Alta

---

# Issue: Interdependencia incorrecta entre capas DDD - Presentation importa Infrastructure de otras features

## Descripción
La capa de Presentation (routes.py) de `features/leagues` importa directamente repositorios de Infrastructure de `features/user`, violando los principios de separación de capas en Domain-Driven Design.

## Problema arquitectural
```python
# features/leagues/presentation/routes.py
from f1_api.features.user.infrastructure.repositories import UserRepositoryImpl  # ❌ INCORRECTO
```

**Violaciones:**
- La capa de **Presentation** no debería conocer detalles de **Infrastructure**
- Rompe la encapsulación entre features
- Acopla directamente implementaciones concretas en lugar de usar interfaces

## Solución propuesta

### Opción 1: Dependency Container (Ideal)
Crear un módulo de composición que centralice la construcción de dependencias:

```python
# features/leagues/dependencies.py
from sqlmodel import Session
from .infrastructure.repositories import LeagueRepositoryImpl, UserLeagueLinkRepositoryImpl
from f1_api.features.user.infrastructure.repositories import UserRepositoryImpl

def get_league_repositories(session: Session):
    """Compone todas las dependencias necesarias para los servicios de League"""
    return {
        "league_repo": LeagueRepositoryImpl(session),
        "user_repo": UserRepositoryImpl(session),
        "user_link_repo": UserLeagueLinkRepositoryImpl(session)
    }
```

Uso en routes:
```python
# features/leagues/presentation/routes.py
from .dependencies import get_league_repositories

@router.post("/")
def create_league(
    league: LeagueCreateDTO, 
    admin_user_id: str,
    session: Session = Depends(get_db_session)
):
    repos = get_league_repositories(session)
    service = CreateLeagueService(**repos, session=session)
    return service.execute(admin_user_id, league)
```

### Opción 2: FastAPI Dependency Injection
Usar el sistema de dependencias de FastAPI:

```python
# features/leagues/dependencies.py
def get_user_repository(session: Session = Depends(get_db_session)):
    return UserRepositoryImpl(session)

# routes.py
@router.post("/")
def create_league(
    league: LeagueCreateDTO,
    session: Session = Depends(get_db_session),
    user_repo = Depends(get_user_repository)
):
    # ...
```

## Archivos afectados
- `features/leagues/presentation/routes.py` - Línea 23
- Posiblemente otros routers con dependencias cross-feature

## Impacto
- **Severidad**: Baja (funciona correctamente)
- **Deuda técnica**: Alta (viola principios DDD)
- **Mantenibilidad**: Media (dificulta testing y refactoring)

## Beneficios de la corrección
1. ✅ Mejor separación de capas
2. ✅ Facilita testing (mock de dependencias)
3. ✅ Reduce acoplamiento entre features
4. ✅ Sigue principios SOLID (Dependency Inversion)
5. ✅ Composición centralizada más mantenible

## Estado
- [x] Identificado
- [ ] Investigado
- [ ] Diseñada solución
- [ ] Implementado
- [ ] Testeado

---
**Fecha de reporte**: 18 de diciembre de 2025  
**Reportado por**: Code Review  
**Prioridad**: Baja (deuda técnica, no bug funcional)
