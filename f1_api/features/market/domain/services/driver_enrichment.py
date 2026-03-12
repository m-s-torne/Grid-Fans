"""Driver enrichment domain service"""
from typing import Dict, Any, Optional
import logging
from ..entities import DriverOwnership
from ..value_objects import DriverPrice, DriverTier

logger = logging.getLogger(__name__)


class DriverEnrichmentService:
    """
    Domain service for enriching driver ownership data.
    
    Adds calculated fields, market statistics, and derived information
    to driver ownership entities for presentation layer.
    """
    
    @classmethod
    def enrich_ownership(
        cls,
        ownership: DriverOwnership,
        driver_name: Optional[str] = None,
        team_name: Optional[str] = None,
        driver_tier: Optional[DriverTier] = None,
        season_points: Optional[float] = None,
    ) -> Dict[str, Any]:
        """
        Enrich ownership entity with calculated and external data.
        
        Args:
            ownership: DriverOwnership entity
            driver_name: Driver's name
            team_name: Driver's current team
            driver_tier: Driver's performance tier
            season_points: Driver's current season points
            
        Returns:
            Dictionary with enriched data
        """
        enriched = {
            # Core ownership data
            "driver_id": ownership.driver_id,
            "league_id": ownership.league_id,
            "owner_id": ownership.owner_id,
            "is_listed_for_sale": ownership.is_listed_for_sale,
            "acquisition_price": ownership.acquisition_price,
            "asking_price": ownership.asking_price,
            "locked_until": ownership.locked_until,
            
            # External data
            "driver_name": driver_name,
            "team_name": team_name,
            "tier": str(driver_tier) if driver_tier else None,
            "season_points": season_points,
            
            # Calculated fields
            "is_free_agent": ownership.is_free_agent(),
            "is_locked": ownership.is_locked(),
            "potential_profit": ownership.potential_profit,
            "days_until_unlock": ownership.days_until_unlock,
            
            # Formatted values
            "acquisition_price_formatted": cls._format_price(ownership.acquisition_price),
            "asking_price_formatted": cls._format_price(ownership.asking_price) if ownership.asking_price else None,
        }
        
        return enriched
    
    @classmethod
    def calculate_market_value(
        cls,
        ownership: DriverOwnership,
        tier: DriverTier,
        demand_multiplier: float = 1.0,
    ) -> float:
        """
        Calculate current market value of a driver.
        
        Args:
            ownership: DriverOwnership entity
            tier: Driver's tier
            demand_multiplier: Market demand adjustment (0.5 - 2.0)
            
        Returns:
            Estimated current market value
        """
        base_price = DriverPrice.from_tier(str(tier))
        
        # Apply demand multiplier
        market_price = base_price.apply_markup(demand_multiplier - 1.0)
        
        # If driver is owned, consider acquisition price as floor
        if not ownership.is_free_agent():
            return max(market_price.amount, ownership.acquisition_price * 0.8)
        
        return market_price.amount
    
    @classmethod
    def calculate_roi_percentage(
        cls,
        ownership: DriverOwnership,
    ) -> Optional[float]:
        """
        Calculate ROI if driver is listed for sale.
        
        Args:
            ownership: DriverOwnership entity
            
        Returns:
            ROI as percentage, None if not for sale
        """
        if not ownership.is_listed_for_sale or not ownership.asking_price:
            return None
        
        if ownership.acquisition_price == 0:
            return None
        
        profit = ownership.asking_price - ownership.acquisition_price
        roi = (profit / ownership.acquisition_price) * 100
        
        return round(roi, 2)
    
    @classmethod
    def estimate_liquidity_score(
        cls,
        ownership: DriverOwnership,
        tier: DriverTier,
    ) -> int:
        """
        Estimate how quickly driver would sell (0-100 score).
        
        Args:
            ownership: DriverOwnership entity
            tier: Driver's tier
            
        Returns:
            Liquidity score (higher = sells faster)
        """
        if not ownership.is_listed_for_sale:
            return 0
        
        score = 50  # Base score
        
        # Higher tier = higher liquidity
        tier_bonus = {"S": 30, "A": 20, "B": 10, "C": 0, "D": -10}
        score += tier_bonus.get(str(tier), 0)
        
        # Price relative to expected value affects liquidity
        if ownership.asking_price and ownership.acquisition_price:
            price_ratio = ownership.asking_price / ownership.acquisition_price
            
            if price_ratio < 1.0:  # Below acquisition (discount)
                score += 20
            elif price_ratio > 1.5:  # High markup
                score -= 30
        
        # Locked drivers can't be traded
        if ownership.is_locked():
            score = 0
        
        return max(0, min(100, score))
    
    @classmethod
    def get_ownership_status_message(
        cls,
        ownership: DriverOwnership,
    ) -> str:
        """
        Generate human-readable status message.
        
        Args:
            ownership: DriverOwnership entity
            
        Returns:
            Status message string
        """
        if ownership.is_free_agent():
            return "Available as free agent"
        
        if ownership.is_locked():
            days = ownership.days_until_unlock
            if days == 0:
                return "Locked (unlocks today)"
            elif days == 1:
                return "Locked (1 day remaining)"
            else:
                return f"Locked ({days} days remaining)"
        
        if ownership.is_listed_for_sale:
            return f"Listed for sale at {cls._format_price(ownership.asking_price)}"
        
        return "Owned (not for sale)"
    
    @staticmethod
    def _format_price(price: Optional[float]) -> Optional[str]:
        """Format price as currency string"""
        if price is None:
            return None
        
        if price >= 1_000_000:
            return f"${price / 1_000_000:.1f}M"
        elif price >= 1_000:
            return f"${price / 1_000:.0f}K"
        else:
            return f"${price:.0f}"
    
    @classmethod
    def enrich_driver_list(
        cls,
        drivers: list,  # List of Drivers SQLModel
        ownerships: list[DriverOwnership],
        driver_results_data: dict,
        drivers_utility,  # DriversUtility instance
        team_map: Dict[int, str],
        owner_names: Optional[Dict[int, str]] = None,
        is_owned: bool = False,
        is_owned_by_me: bool = False,
        is_free_agent: bool = False,
        is_for_sale: bool = False,
        include_owner_names: bool = False,
    ) -> list[dict]:
        """
        Enrich driver list with stats, ownership, and market metadata.
        
        Replicates legacy _build_driver_list_response + _enrich_drivers_with_stats format
        to maintain exact backward compatibility with frontend.
        
        Args:
            drivers: List of Driver SQLModel instances
            ownerships: List of DriverOwnership entities
            driver_results_data: Dict with max_round, sprint_rounds, results, all_results
            drivers_utility: DriversUtility instance for stats calculation
            team_map: Dict mapping driver_id to team_name
            owner_names: Dict mapping user_id to user_name (optional)
            is_owned: Whether these drivers are owned by someone
            is_owned_by_me: Whether these drivers are owned by the requesting user
            is_free_agent: Whether these are free agents
            is_for_sale: Whether these are listed for sale
            include_owner_names: Whether to include owner names in response
            
        Returns:
            List of enriched driver dictionaries matching legacy format
        """
        if not drivers:
            logger.warning("No drivers provided for enrichment")
            return []
        
        if not ownerships:
            logger.warning("No ownerships provided for enrichment")
            return []
        
        logger.debug("Enriching %d drivers with %d ownerships", len(drivers), len(ownerships))
        
        try:
            # Extract results data
            max_round = driver_results_data["max_round"]
            sprint_rounds = driver_results_data["sprint_rounds"]
            all_results = driver_results_data["all_results"]
            results = driver_results_data["results"]
            
            # Calculate stats using DriversUtility
            stats = drivers_utility.get_driver_stats(all_results)
            points_map = {r.driver_id: r.total_points for r in results}
            available_points = 25 * max_round + len(sprint_rounds) * 8
            
            # Enrich each driver
            enriched_drivers = []
            for driver in drivers:
                driver_stats = stats.get(driver.id, {})
                finishes = driver_stats.get("finish_positions", None)
                grids = driver_stats.get("grid_positions", None)
                pole_victories = driver_stats.get("pole_victories", None)
                poles = driver_stats.get("poles", 0)
                points = points_map.get(driver.id, 0)
                podiums = driver_stats.get("podiums", 0)
                victories = driver_stats.get("victories", 0)
                overtakes = driver_stats.get("overtakes", 0)
                
                enriched_driver = {
                    **driver.model_dump(),
                    "season_results": {
                        "points": points,
                        "poles": poles,
                        "podiums": podiums,
                        "fastest_laps": driver_stats.get("fastest_laps", 0),
                        "victories": victories,
                        "sprint_podiums": driver_stats.get("sprint_podiums", 0),
                        "sprint_victories": driver_stats.get("sprint_victories", 0),
                        "sprint_poles": driver_stats.get("sprint_poles", 0)
                    },
                    "fantasy_stats": {
                        "avg_finish": round(sum(finishes) / len(finishes), 1) if finishes else 0,
                        "avg_grid_position": round(sum(grids) / len(grids), 1) if grids else 0,
                        "pole_win_conversion": round(((pole_victories * 100) / poles), 1) if poles else 0,
                        "price": 10_000_000 + (int(points) * 10_000) + (podiums * 50_000) + (victories * 100_000),
                        "overtake_efficiency": round(sum(overtakes) / len(overtakes), 1) if overtakes else 0,
                        "available_points_percentatge": round(points * 100 / available_points, 1) if available_points > 0 else 0,
                    }
                }
                enriched_drivers.append(enriched_driver)
            
            # Build response with ownership info
            result = []
            for driver_dict in enriched_drivers:
                ownership = next((o for o in ownerships if o.driver_id == driver_dict['id']), None)
                
                driver_dict['team_name'] = team_map.get(driver_dict['id'])
                # Convert DriverOwnership entity to dict
                if ownership:
                    try:
                        driver_dict['ownership'] = {
                            'driver_id': ownership.driver_id,
                            'league_id': ownership.league_id,
                            'owner_id': ownership.owner_id,
                            'is_listed_for_sale': ownership.is_listed_for_sale,
                            'acquisition_price': ownership.acquisition_price,
                            'asking_price': ownership.asking_price,
                            'locked_until': ownership.locked_until.isoformat() if ownership.locked_until and hasattr(ownership.locked_until, 'isoformat') else None,
                            'created_at': ownership.created_at.isoformat() if ownership.created_at and hasattr(ownership.created_at, 'isoformat') else None,
                            'updated_at': ownership.updated_at.isoformat() if ownership.updated_at and hasattr(ownership.updated_at, 'isoformat') else None,
                        }
                    except Exception as e:
                        logger.error("Error converting ownership to dict for driver_id=%d: %s", ownership.driver_id, str(e))
                        driver_dict['ownership'] = None
                else:
                    driver_dict['ownership'] = None
                driver_dict['isOwned'] = is_owned
                driver_dict['isOwnedByMe'] = is_owned_by_me
                driver_dict['isFreeAgent'] = is_free_agent
                
                # Handle isForSale - override with ownership status for owned drivers
                if is_owned_by_me and ownership:
                    driver_dict['isForSale'] = ownership.is_listed_for_sale
                else:
                    driver_dict['isForSale'] = is_for_sale
                
                # Check if driver is locked
                driver_dict['isLocked'] = ownership.is_locked() if ownership else False
                driver_dict['canBuyout'] = False  # TODO: Implement buyout eligibility logic
                
                # Add owner name if needed
                if include_owner_names and owner_names:
                    driver_dict['ownerName'] = owner_names.get(ownership.owner_id) if ownership and ownership.owner_id else None
                else:
                    driver_dict['ownerName'] = None
                
                result.append(driver_dict)
            
            logger.debug("Enrichment complete: returning %d drivers", len(result))
            return result
            
        except Exception as e:
            logger.error("Error enriching driver list: %s", str(e), exc_info=True)
            # Return basic driver data without enrichment if stats calculation fails
            return [driver.model_dump() for driver in drivers]
