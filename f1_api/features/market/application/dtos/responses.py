"""Market response DTOs"""
from pydantic import BaseModel, Field
from typing import Optional
from datetime import datetime


class DriverOwnershipResponse(BaseModel):
    """Response model for driver ownership data"""
    
    driver_id: int
    league_id: int
    owner_id: Optional[int] = None
    is_listed_for_sale: bool
    acquisition_price: float
    asking_price: Optional[float] = None
    locked_until: Optional[datetime] = None
    created_at: datetime
    updated_at: datetime
    
    # Enriched fields
    driver_name: Optional[str] = None
    team_name: Optional[str] = None
    tier: Optional[str] = None
    season_points: Optional[float] = None
    is_free_agent: bool
    is_locked: bool
    potential_profit: Optional[float] = None
    days_until_unlock: Optional[int] = None
    status_message: Optional[str] = None
    
    # Formatted values
    acquisition_price_formatted: Optional[str] = None
    asking_price_formatted: Optional[str] = None
    
    class Config:
        json_schema_extra = {
            "example": {
                "driver_id": 1,
                "league_id": 1,
                "owner_id": 1,
                "is_listed_for_sale": True,
                "acquisition_price": 10000000,
                "asking_price": 12000000,
                "locked_until": None,
                "created_at": "2024-01-15T10:30:00",
                "updated_at": "2024-01-20T14:45:00",
                "driver_name": "Max Verstappen",
                "team_name": "Red Bull Racing",
                "tier": "S",
                "season_points": 250.0,
                "is_free_agent": False,
                "is_locked": False,
                "potential_profit": 2000000,
                "days_until_unlock": None,
                "status_message": "Listed for sale at $12.0M",
                "acquisition_price_formatted": "$10.0M",
                "asking_price_formatted": "$12.0M",
            }
        }


class MarketTransactionResponse(BaseModel):
    """Response model for market transaction"""
    
    id: Optional[int] = None
    driver_id: int
    league_id: int
    seller_id: Optional[int] = None
    buyer_id: int
    transaction_price: float
    transaction_type: str
    transaction_date: datetime
    
    # Enriched fields
    driver_name: Optional[str] = None
    buyer_name: Optional[str] = None
    seller_name: Optional[str] = None
    transaction_price_formatted: Optional[str] = None
    
    class Config:
        json_schema_extra = {
            "example": {
                "id": 123,
                "driver_id": 1,
                "league_id": 1,
                "seller_id": 2,
                "buyer_id": 1,
                "transaction_price": 10000000,
                "transaction_type": "buy_from_user",
                "transaction_date": "2024-01-20T14:45:00",
                "driver_name": "Max Verstappen",
                "buyer_name": "User One",
                "seller_name": "User Two",
                "transaction_price_formatted": "$10.0M",
            }
        }


class BuyoutHistoryResponse(BaseModel):
    """Response model for buyout clause history"""
    
    id: Optional[int] = None
    league_id: int
    buyer_id: int
    victim_id: int
    driver_id: int
    buyout_price: float
    buyout_date: datetime
    season_year: int
    
    # Enriched fields
    driver_name: Optional[str] = None
    buyer_name: Optional[str] = None
    victim_name: Optional[str] = None
    buyout_price_formatted: Optional[str] = None
    
    class Config:
        json_schema_extra = {
            "example": {
                "id": 45,
                "league_id": 1,
                "buyer_id": 1,
                "victim_id": 2,
                "driver_id": 1,
                "buyout_price": 13000000,
                "buyout_date": "2024-01-20T14:45:00",
                "season_year": 2024,
                "driver_name": "Max Verstappen",
                "buyer_name": "User One",
                "victim_name": "User Two",
                "buyout_price_formatted": "$13.0M",
            }
        }


class MarketListingResponse(BaseModel):
    """Response model for market listing (driver for sale)"""
    
    driver_id: int
    driver_name: str
    team_name: Optional[str] = None
    tier: Optional[str] = None
    owner_id: int
    owner_name: Optional[str] = None
    asking_price: float
    acquisition_price: float
    potential_profit: float
    roi_percentage: float
    season_points: Optional[float] = None
    locked_until: Optional[datetime] = None
    is_locked: bool
    liquidity_score: int = Field(..., ge=0, le=100, description="How quickly it would sell (0-100)")
    
    # Formatted values
    asking_price_formatted: str
    acquisition_price_formatted: str
    
    class Config:
        json_schema_extra = {
            "example": {
                "driver_id": 1,
                "driver_name": "Max Verstappen",
                "team_name": "Red Bull Racing",
                "tier": "S",
                "owner_id": 1,
                "owner_name": "User One",
                "asking_price": 12000000,
                "acquisition_price": 10000000,
                "potential_profit": 2000000,
                "roi_percentage": 20.0,
                "season_points": 250.0,
                "locked_until": None,
                "is_locked": False,
                "liquidity_score": 75,
                "asking_price_formatted": "$12.0M",
                "acquisition_price_formatted": "$10.0M",
            }
        }


class MarketStatsResponse(BaseModel):
    """Response model for market statistics"""
    
    league_id: int
    total_drivers: int
    free_agents: int
    drivers_for_sale: int
    total_transactions: int
    
    # Price statistics
    average_price: float
    median_price: float
    min_price: float
    max_price: float
    
    # Transaction statistics
    total_volume: float  # Total value of all transactions
    avg_transaction_price: float
    transactions_last_24h: int
    transactions_last_7d: int
    
    # Tier distribution
    tier_distribution: dict = Field(
        default_factory=dict,
        description="Count of drivers by tier"
    )
    
    # Most active
    most_active_buyer_id: Optional[int] = None
    most_active_seller_id: Optional[int] = None
    most_traded_driver_id: Optional[int] = None
    
    # Formatted values
    average_price_formatted: str
    total_volume_formatted: str
    
    class Config:
        json_schema_extra = {
            "example": {
                "league_id": 1,
                "total_drivers": 60,
                "free_agents": 10,
                "drivers_for_sale": 8,
                "total_transactions": 145,
                "average_price": 5500000,
                "median_price": 5000000,
                "min_price": 500000,
                "max_price": 15000000,
                "total_volume": 150000000,
                "avg_transaction_price": 6000000,
                "transactions_last_24h": 3,
                "transactions_last_7d": 18,
                "tier_distribution": {"S": 5, "A": 10, "B": 15, "C": 20, "D": 10},
                "most_active_buyer_id": 1,
                "most_active_seller_id": 2,
                "most_traded_driver_id": 15,
                "average_price_formatted": "$5.5M",
                "total_volume_formatted": "$150.0M",
            }
        }


class PurchaseResultResponse(BaseModel):
    """Response model for successful purchase"""
    
    success: bool
    message: str
    ownership: DriverOwnershipResponse
    transaction: MarketTransactionResponse
    budget_remaining: float
    budget_remaining_formatted: str
    
    class Config:
        json_schema_extra = {
            "example": {
                "success": True,
                "message": "Successfully purchased driver for $10.0M",
                "ownership": {
                    "driver_id": 1,
                    "league_id": 1,
                    "owner_id": 1,
                    "is_listed_for_sale": False,
                    "acquisition_price": 10000000,
                    "asking_price": None,
                    "locked_until": "2024-01-27T14:45:00",
                    "created_at": "2024-01-20T14:45:00",
                    "updated_at": "2024-01-20T14:45:00",
                    "driver_name": "Max Verstappen",
                    "is_free_agent": False,
                    "is_locked": True,
                    "days_until_unlock": 7,
                },
                "transaction": {
                    "id": 123,
                    "driver_id": 1,
                    "league_id": 1,
                    "seller_id": None,
                    "buyer_id": 1,
                    "transaction_price": 10000000,
                    "transaction_type": "buy_from_market",
                    "transaction_date": "2024-01-20T14:45:00",
                },
                "budget_remaining": 90000000,
                "budget_remaining_formatted": "$90.0M",
            }
        }


class ValidationErrorResponse(BaseModel):
    """Response model for validation errors"""
    
    success: bool = False
    error: str
    error_code: Optional[str] = None
    details: Optional[dict] = None
    
    class Config:
        json_schema_extra = {
            "example": {
                "success": False,
                "error": "Insufficient budget. Need $10,000,000, have $5,000,000. Short by $5,000,000.",
                "error_code": "INSUFFICIENT_BUDGET",
                "details": {
                    "required": 10000000,
                    "available": 5000000,
                    "shortage": 5000000,
                },
            }
        }


class BudgetHealthResponse(BaseModel):
    """Response model for budget health check"""
    
    current_budget: float
    starting_budget: float
    minimum_reserve: float
    budget_percentage: float
    status: str = Field(..., description="Budget status: critical, warning, low, moderate, healthy")
    status_message: str
    max_affordable: float
    
    # Formatted values
    current_budget_formatted: str
    max_affordable_formatted: str
    
    class Config:
        json_schema_extra = {
            "example": {
                "current_budget": 45000000,
                "starting_budget": 100000000,
                "minimum_reserve": 5000000,
                "budget_percentage": 45.0,
                "status": "moderate",
                "status_message": "Budget at moderate level.",
                "max_affordable": 40000000,
                "current_budget_formatted": "$45.0M",
                "max_affordable_formatted": "$40.0M",
            }
        }
