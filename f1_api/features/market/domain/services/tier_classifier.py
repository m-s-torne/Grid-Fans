"""Tier classifier domain service"""
from typing import Optional
from ..value_objects import DriverTier, TierLevel


class TierClassifier:
    """
    Domain service for classifying drivers into performance tiers.
    
    Uses championship points, race results, and team performance
    to assign appropriate tier level.
    """
    
    # Points thresholds for tier classification
    S_TIER_MIN_POINTS = 200
    A_TIER_MIN_POINTS = 100
    B_TIER_MIN_POINTS = 50
    C_TIER_MIN_POINTS = 10
    
    # Podium-based classification (alternative method)
    S_TIER_MIN_PODIUMS = 8
    A_TIER_MIN_PODIUMS = 4
    B_TIER_MIN_PODIUMS = 2
    
    @classmethod
    def classify_by_points(cls, total_points: float) -> DriverTier:
        """
        Classify driver based on championship points.
        
        Args:
            total_points: Total championship points accumulated
            
        Returns:
            DriverTier assignment
        """
        if total_points >= cls.S_TIER_MIN_POINTS:
            return DriverTier(TierLevel.S)
        elif total_points >= cls.A_TIER_MIN_POINTS:
            return DriverTier(TierLevel.A)
        elif total_points >= cls.B_TIER_MIN_POINTS:
            return DriverTier(TierLevel.B)
        elif total_points >= cls.C_TIER_MIN_POINTS:
            return DriverTier(TierLevel.C)
        else:
            return DriverTier(TierLevel.D)
    
    @classmethod
    def classify_by_podiums(cls, podium_count: int) -> DriverTier:
        """
        Classify driver based on podium finishes.
        
        Args:
            podium_count: Number of podium finishes (P1, P2, P3)
            
        Returns:
            DriverTier assignment
        """
        if podium_count >= cls.S_TIER_MIN_PODIUMS:
            return DriverTier(TierLevel.S)
        elif podium_count >= cls.A_TIER_MIN_PODIUMS:
            return DriverTier(TierLevel.A)
        elif podium_count >= cls.B_TIER_MIN_PODIUMS:
            return DriverTier(TierLevel.B)
        elif podium_count > 0:
            return DriverTier(TierLevel.C)
        else:
            return DriverTier(TierLevel.D)
    
    @classmethod
    def classify_by_average_position(cls, avg_position: float, races_count: int) -> DriverTier:
        """
        Classify driver based on average finishing position.
        
        Args:
            avg_position: Average finishing position
            races_count: Number of races participated
            
        Returns:
            DriverTier assignment
        """
        # Need minimum races to classify reliably
        if races_count < 5:
            return DriverTier(TierLevel.D)
        
        if avg_position <= 3.0:
            return DriverTier(TierLevel.S)
        elif avg_position <= 6.0:
            return DriverTier(TierLevel.A)
        elif avg_position <= 10.0:
            return DriverTier(TierLevel.B)
        elif avg_position <= 15.0:
            return DriverTier(TierLevel.C)
        else:
            return DriverTier(TierLevel.D)
    
    @classmethod
    def classify_comprehensive(
        cls,
        total_points: float,
        podium_count: int,
        avg_position: Optional[float] = None,
        races_count: int = 0,
    ) -> DriverTier:
        """
        Comprehensive classification using multiple factors.
        
        Uses weighted combination of points, podiums, and position.
        
        Args:
            total_points: Championship points
            podium_count: Podium finishes
            avg_position: Average finishing position (optional)
            races_count: Number of races (optional)
            
        Returns:
            DriverTier based on combined analysis
        """
        # Primary classification by points
        points_tier = cls.classify_by_points(total_points)
        
        # Secondary classification by podiums
        podium_tier = cls.classify_by_podiums(podium_count)
        
        # Tertiary classification by average position
        if avg_position is not None and races_count >= 5:
            position_tier = cls.classify_by_average_position(avg_position, races_count)
        else:
            position_tier = None
        
        # Take the best (highest) tier from available metrics
        tiers = [points_tier, podium_tier]
        if position_tier:
            tiers.append(position_tier)
        
        # Return highest tier (lowest rank number)
        return min(tiers, key=lambda t: t.rank)
    
    @classmethod
    def recommend_reclassification(
        cls,
        current_tier: DriverTier,
        recent_points: float,
        recent_races: int = 5,
    ) -> Optional[DriverTier]:
        """
        Recommend tier reclassification based on recent performance.
        
        Args:
            current_tier: Current assigned tier
            recent_points: Points in recent races
            recent_races: Number of recent races considered
            
        Returns:
            Recommended new tier if change needed, None otherwise
        """
        if recent_races < 3:
            return None  # Not enough data
        
        # Calculate points per race
        avg_points_per_race = recent_points / recent_races
        
        # Estimate full season points
        estimated_season_points = avg_points_per_race * 20  # ~20 races per season
        
        # Classify based on projected performance
        recommended_tier = cls.classify_by_points(estimated_season_points)
        
        # Only recommend change if it's significant (not just 1 tier)
        tier_difference = abs(current_tier.rank - recommended_tier.rank)
        
        if tier_difference >= 1:
            return recommended_tier
        
        return None
