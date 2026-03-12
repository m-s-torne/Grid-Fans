# Market Feature - Domain-Driven Design Structure

## Overview
The Market feature manages driver ownership, transactions, and buyout operations within fantasy F1 leagues. This feature follows Domain-Driven Design (DDD) principles with clear separation of concerns across domain, application, infrastructure, and presentation layers.

## Architecture Decision: Market as Aggregate Root
**Key Decision:** Market is an independent aggregate root, not a subdomain of Leagues.

**Rationale:**
- Market logic is complex enough to warrant its own bounded context
- Market operations span multiple leagues but have independent business rules
- Separating market from leagues improves maintainability and testability

## Directory Structure

```
features/market/
├── domain/                          # Core business logic (framework-agnostic)
│   ├── entities/                    # Pure domain entities (dataclasses)
│   │   ├── driver_ownership.py     # Driver ownership aggregate root
│   │   ├── market_transaction.py   # Transaction records
│   │   └── buyout_history.py       # Buyout clause tracking
│   ├── value_objects/               # Immutable domain concepts
│   │   ├── driver_price.py         # Pricing logic
│   │   ├── driver_tier.py          # Driver classification
│   │   ├── lineup_slot.py          # Lineup positions
│   │   └── lock_period.py          # Time-based constraints
│   ├── services/                    # Domain services (complex operations)
│   │   ├── tier_classifier.py      # Driver tier classification
│   │   ├── driver_enrichment.py    # Data enrichment
│   │   ├── buyout_validator.py     # Buyout business rules
│   │   ├── budget_validator.py     # Budget constraints
│   │   └── emergency_assignment.py # Admin operations
│   └── interfaces/                  # Repository contracts (Protocol pattern)
│       ├── i_ownership_repository.py
│       ├── i_transaction_repository.py
│       └── i_buyout_repository.py
│
├── application/                     # Use cases and orchestration
│   ├── use_cases/                  # Business workflows
│   └── dtos/                       # Data transfer objects
│       ├── requests.py             # API request models
│       └── responses.py            # API response models
│
├── infrastructure/                  # External concerns (DB, APIs)
│   ├── models/                     # SQLModel database mappings
│   │   ├── ownership_model.py      # DriverOwnershipModel (SQLModel)
│   │   ├── transaction_model.py    # MarketTransactionModel (SQLModel)
│   │   └── buyout_model.py         # BuyoutClauseHistoryModel (SQLModel)
│   └── persistence/                # Repository implementations
│       ├── ownership_repository.py
│       ├── transaction_repository.py
│       └── buyout_repository.py
│
└── presentation/                    # API layer
    └── routes.py                   # FastAPI endpoints

# Legacy files (to be removed in Phase 4):
├── models.py                       # DEPRECATED - Use infrastructure.models
├── services.py                     # DEPRECATED - Use domain.entities
├── controllers.py                  # DEPRECATED - Use application.use_cases
└── driver_ownership_controller.py  # DEPRECATED - Use presentation.routes
```

## Design Patterns

### 1. Domain Entities (Pure Dataclasses)
- **Location:** `domain/entities/`
- **Pattern:** Pure Python dataclasses, no SQLModel inheritance
- **Purpose:** Business logic without infrastructure concerns
- **Example:** `DriverOwnership` entity with methods like `list_for_sale()`, `is_locked()`

### 2. Infrastructure Models (SQLModel)
- **Location:** `infrastructure/models/`
- **Pattern:** SQLModel/SQLAlchemy for ORM
- **Purpose:** Database persistence layer
- **Naming:** Suffix with "Model" (e.g., `DriverOwnershipModel`)

### 3. Repository Interfaces (Protocol)
- **Location:** `domain/interfaces/`
- **Pattern:** Protocol for structural subtyping (TYPE_CHECKING only)
- **Purpose:** Dependency inversion, testability
- **Benefit:** No runtime overhead, type-safe

### 4. Value Objects
- **Location:** `domain/value_objects/`
- **Pattern:** Immutable objects representing domain concepts
- **Examples:** DriverPrice, DriverTier, LockPeriod

### 5. Domain Services
- **Location:** `domain/services/`
- **Pattern:** Stateless services for complex domain operations
- **Purpose:** Logic that doesn't belong to a single entity

## Migration from Duplicate Models

### Problem Resolved
Previously, market models existed in two locations:
1. `features/market/models.py` (simple SQLModels)
2. `features/leagues/domain/market/models.py` (enriched with business logic)

### Resolution
- **Kept:** `features/leagues/domain/market/models.py` version (had business logic)
- **Created:** New pure domain entities in `features/market/domain/entities/`
- **Created:** New infrastructure models in `features/market/infrastructure/models/`
- **Deleted:** `features/leagues/domain/market/` subdomain entirely
- **Deprecated:** `features/market/models.py` (kept for backward compatibility)

### Import Updates
Files updated to use new location:
- `f1_api/models/repositories/market_transactions_repository.py`
- `f1_api/features/leagues/domain/market/interfaces.py`
- `f1_api/features/leagues/infrastructure/market/repositories.py`

**Old Import:**
```python
from f1_api.features.leagues.domain.market.models import DriverOwnership
```

**New Import (Infrastructure):**
```python
from f1_api.features.market.infrastructure.models import DriverOwnershipModel
```

**New Import (Domain):**
```python
from f1_api.features.market.domain.entities import DriverOwnership
```

## Business Rules (Domain)

### Driver Ownership
- One owner per driver per league (None = free agent)
- Drivers can be listed for sale (with asking price)
- Drivers are locked for 7 days after acquisition
- `acquisition_price` is immutable during listing (business rule)

### Market Transactions
- Records all market activity (audit trail)
- Types: buy_from_market, buy_from_user, sell_to_market, buyout_clause, emergency_assignment
- Tracks buyer, seller, price, and timestamp

### Buyout Clauses
- Limited buyouts per season between same users
- Buyout price typically higher than market value
- Separate history tracking for analytics

## Implementation Status

### ✅ Phase 1 Complete (Foundation)
- [x] Complete DDD directory structure (35+ files)
- [x] Repository interfaces using Protocol pattern
- [x] Domain entities as pure dataclasses
- [x] Infrastructure models (SQLModel)
- [x] Value object stubs
- [x] Domain service stubs
- [x] DTO stubs
- [x] Resolved model duplication
- [x] Updated imports (3 files)
- [x] Deleted `leagues/domain/market/` subdomain

### 🔲 Phase 2: Entity Logic
- [ ] Implement value objects (driver_price, driver_tier, lineup_slot, lock_period)
- [ ] Implement domain services (tier_classifier, driver_enrichment, etc.)
- [ ] Complete entity business methods
- [ ] Create DTOs for requests/responses

### 🔲 Phase 3: Use Cases
- [ ] Implement repository implementations
- [ ] Create use cases (purchase_driver, list_driver_for_sale, etc.)
- [ ] Add mappers between entities and models

### 🔲 Phase 4: Migration
- [ ] Migrate market_controller.py logic to use cases
- [ ] Update existing code to use new imports
- [ ] Remove deprecated files (models.py, services.py, controllers.py)

### 🔲 Phase 5: API Layer
- [ ] Create FastAPI routes in presentation/routes.py
- [ ] Add API documentation
- [ ] Integration tests

## Key Files

### Domain Layer (Business Logic)
- **driver_ownership.py** - 251 lines - Aggregate root with 12 business methods
- **market_transaction.py** - 53 lines - Transaction entity with helper methods
- **buyout_history.py** - 33 lines - Buyout tracking entity

### Infrastructure Layer (Persistence)
- **ownership_model.py** - 223 lines - SQLModel with backward-compatible methods
- **transaction_model.py** - 35 lines - Transaction database model
- **buyout_model.py** - 37 lines - Buyout database model

### Interfaces (Contracts)
- **i_ownership_repository.py** - 89 lines - 5 methods for ownership operations
- **i_transaction_repository.py** - 37 lines - 2 methods for transactions
- **i_buyout_repository.py** - 52 lines - 2 methods for buyout operations

## Testing Strategy

### Unit Tests
- Domain entities: Test business logic without database
- Domain services: Test complex operations in isolation
- Value objects: Test immutability and validation

### Integration Tests
- Repository implementations: Test database operations
- Use cases: Test end-to-end workflows

### API Tests
- Presentation layer: Test HTTP endpoints

## Dependencies

### Domain Layer
- **NO external dependencies** (pure Python)
- Only uses: `dataclasses`, `datetime`, `typing`

### Infrastructure Layer
- `sqlmodel` - ORM
- `sqlalchemy` - Database toolkit
- `pydantic` - Validation (via SQLModel)

### Application Layer
- `pydantic` - DTO validation

### Presentation Layer
- `fastapi` - Web framework
- `starlette` - ASGI toolkit

## Notes for Developers

1. **Backward Compatibility:** Old imports from `features/market/models.py` still work but are deprecated
2. **No Breaking Changes:** Existing controllers and routers continue to function
3. **Type Safety:** All interfaces use Protocol pattern with TYPE_CHECKING for zero runtime cost
4. **Database:** SQLModel tables remain unchanged (same table names and structure)
5. **Testing:** Domain layer can be tested without database setup

## Next Steps (Phase 2)

1. Implement value objects with proper validation
2. Implement domain services for complex operations
3. Complete business logic in domain entities
4. Create comprehensive DTOs for API layer
5. Add unit tests for domain layer

---

**Created:** Phase 1 - Foundation Setup  
**Last Updated:** Phase 1 Complete  
**Maintainer:** Development Team  
**Reference:** DDD principles, Clean Architecture patterns
