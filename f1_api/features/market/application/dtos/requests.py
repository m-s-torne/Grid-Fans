"""Market request DTOs"""
from pydantic import BaseModel, Field, field_validator, model_validator
from typing import Optional


class PurchaseDriverRequest(BaseModel):
    """Request to purchase a driver from the market"""
    
    driver_id: int = Field(..., gt=0, description="ID of driver to purchase")
    league_id: int = Field(..., gt=0, description="ID of league")
    user_id: int = Field(..., gt=0, description="ID of purchasing user")
    
    class Config:
        json_schema_extra = {
            "example": {
                "driver_id": 1,
                "league_id": 1,
                "user_id": 1,
            }
        }


class PurchaseFromUserRequest(BaseModel):
    """Request to purchase a driver from another user"""
    
    driver_id: int = Field(..., gt=0, description="ID of driver to purchase")
    league_id: int = Field(..., gt=0, description="ID of league")
    buyer_id: int = Field(..., gt=0, description="ID of buying user")
    seller_id: int = Field(..., gt=0, description="ID of selling user")
    
    @model_validator(mode='after')
    def buyer_cannot_be_seller(self):
        if self.buyer_id == self.seller_id:
            raise ValueError("Buyer and seller cannot be the same user")
        return self
    
    class Config:
        json_schema_extra = {
            "example": {
                "driver_id": 1,
                "league_id": 1,
                "buyer_id": 1,
                "seller_id": 2,
            }
        }


class ListDriverForSaleRequest(BaseModel):
    """Request to list a driver for sale"""
    
    driver_id: int = Field(..., gt=0, description="ID of driver to list")
    league_id: int = Field(..., gt=0, description="ID of league")
    user_id: int = Field(..., gt=0, description="ID of owner")
    asking_price: Optional[float] = Field(
        None,
        gt=0,
        description="Asking price (defaults to acquisition price if not provided)"
    )
    
    @field_validator('asking_price')
    @classmethod
    def validate_asking_price(cls, v):
        if v is not None and v < 100_000:
            raise ValueError("Asking price must be at least 100,000")
        if v is not None and v > 100_000_000:
            raise ValueError("Asking price cannot exceed 100,000,000")
        return v
    
    class Config:
        json_schema_extra = {
            "example": {
                "driver_id": 1,
                "league_id": 1,
                "user_id": 1,
                "asking_price": 5000000,
            }
        }


class UnlistDriverRequest(BaseModel):
    """Request to remove driver from sale listings"""
    
    driver_id: int = Field(..., gt=0, description="ID of driver to unlist")
    league_id: int = Field(..., gt=0, description="ID of league")
    user_id: int = Field(..., gt=0, description="ID of owner")
    
    class Config:
        json_schema_extra = {
            "example": {
                "driver_id": 1,
                "league_id": 1,
                "user_id": 1,
            }
        }


class SellToMarketRequest(BaseModel):
    """Request to sell driver back to market"""
    
    driver_id: int = Field(..., gt=0, description="ID of driver to sell")
    league_id: int = Field(..., gt=0, description="ID of league")
    user_id: int = Field(..., gt=0, description="ID of owner")
    
    class Config:
        json_schema_extra = {
            "example": {
                "driver_id": 1,
                "league_id": 1,
                "user_id": 1,
            }
        }


class BuyoutClauseRequest(BaseModel):
    """Request to activate buyout clause"""
    
    driver_id: int = Field(..., gt=0, description="ID of driver to buyout")
    league_id: int = Field(..., gt=0, description="ID of league")
    buyer_id: int = Field(..., gt=0, description="ID of buying user")
    victim_id: int = Field(..., gt=0, description="ID of user being bought out from")
    season_year: int = Field(..., ge=2000, le=2100, description="Current season year")
    
    @model_validator(mode='after')
    def buyer_cannot_be_victim(self):
        if self.buyer_id == self.victim_id:
            raise ValueError("Cannot buyout your own driver")
        return self
    
    class Config:
        json_schema_extra = {
            "example": {
                "driver_id": 1,
                "league_id": 1,
                "buyer_id": 1,
                "victim_id": 2,
                "season_year": 2024,
            }
        }


class EmergencyAssignmentRequest(BaseModel):
    """Request for emergency driver assignment (admin only)"""
    
    driver_id: int = Field(..., gt=0, description="ID of driver to assign")
    league_id: int = Field(..., gt=0, description="ID of league")
    user_id: int = Field(..., gt=0, description="ID of user receiving driver")
    admin_id: int = Field(..., gt=0, description="ID of admin authorizing assignment")
    reason: str = Field(
        ...,
        min_length=10,
        max_length=500,
        description="Reason for emergency assignment"
    )
    override_price: Optional[float] = Field(
        None,
        ge=0,
        description="Optional price override (defaults to discounted rate)"
    )
    
    class Config:
        json_schema_extra = {
            "example": {
                "driver_id": 1,
                "league_id": 1,
                "user_id": 1,
                "admin_id": 100,
                "reason": "Driver retirement - compensating affected user",
                "override_price": None,
            }
        }


class MarketFilterRequest(BaseModel):
    """Request to filter market listings"""
    
    league_id: int = Field(..., gt=0, description="ID of league")
    user_id: Optional[int] = Field(None, gt=0, description="Filter by user")
    min_price: Optional[float] = Field(None, ge=0, description="Minimum price")
    max_price: Optional[float] = Field(None, ge=0, description="Maximum price")
    tier: Optional[str] = Field(None, description="Filter by tier (S, A, B, C, D)")
    is_locked: Optional[bool] = Field(None, description="Filter by lock status")
    is_for_sale: Optional[bool] = Field(None, description="Filter by sale status")
    
    @field_validator('tier')
    @classmethod
    def validate_tier(cls, v):
        if v is not None and v.upper() not in ['S', 'A', 'B', 'C', 'D']:
            raise ValueError("Tier must be S, A, B, C, or D")
        return v.upper() if v else None
    
    @model_validator(mode='after')
    def max_price_greater_than_min(self):
        if self.max_price is not None and self.min_price is not None:
            if self.max_price < self.min_price:
                raise ValueError("max_price must be greater than min_price")
        return self
    
    class Config:
        json_schema_extra = {
            "example": {
                "league_id": 1,
                "user_id": None,
                "min_price": 1000000,
                "max_price": 10000000,
                "tier": "A",
                "is_locked": False,
                "is_for_sale": True,
            }
        }
