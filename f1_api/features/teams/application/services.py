"""Teams application services"""
import logging
from typing import Dict
from f1_api.features.teams.domain.interfaces import TeamsRepository
from f1_api.features.teams.domain.models import Teams

logger = logging.getLogger(__name__)


class GetTeamsWithStatsService:
    """
    Service for retrieving F1 teams with their season statistics.
    
    Enriches team data with calculated season performance metrics
    including total points and driver counts.
    """
    
    def __init__(self, teams_repo: TeamsRepository):
        self.teams_repo = teams_repo
    
    def execute(self) -> list:
        """
        Get all teams with their season statistics.
        
        Retrieves team data from the repository and enriches it with calculated
        season performance metrics including total points and driver counts.
        Teams are returned sorted by total points in descending order.

        Returns:
            list: Teams with calculated points and rankings, empty list on error
        """
        try:
            teams = self.teams_repo.get_all_teams()
            team_points_data = self.teams_repo.get_team_points_data()
            team_stats = self._calculate_team_statistics(team_points_data)
            result = self._build_teams_with_stats(teams, team_stats)

            return result
        except Exception as e:
            logger.warning("Teams service execution interrupted: %s", e)
            return []
    
    def _calculate_team_statistics(self, team_points_data: list) -> Dict[int, Dict]:
        """
        Calculate team statistics from raw points data.
        
        Aggregates points and driver information for each team from the raw
        database results, providing total points and unique driver counts.
        
        Args:
            team_points_data: Raw team points data from repository
            
        Returns:
            Dict mapping team_id to statistics dictionary containing:
                - total_points: Accumulated points for the team
                - drivers: Set of unique driver IDs for the team
        """
        team_stats = {}

        for team_id, driver_id, round_number, round_points in team_points_data:
            if team_id not in team_stats:
                team_stats[team_id] = {
                    "total_points": 0,
                    "drivers": set()
                }
            
            team_stats[team_id]["total_points"] += round_points or 0
            team_stats[team_id]["drivers"].add(driver_id)
        
        return team_stats
    
    def _build_teams_with_stats(self, teams: list[Teams], team_stats: Dict) -> list:
        """
        Combine team data with calculated statistics.
        
        Merges raw team information with calculated statistics, creating
        enriched team objects with season performance metrics and rankings.
        
        Args:
            teams: List of team entities from repository
            team_stats: Calculated statistics dictionary
            
        Returns:
            List of team dictionaries with embedded season results,
            sorted by points in descending order
        """
        result = []
        for team in teams:
            team_dict = team.model_dump()
            stats = team_stats.get(team.id, {"total_points": 0, "drivers": set()})
            team_dict["season_results"] = {
                "points": stats["total_points"],
                "driver_count": len(stats["drivers"])
            }
            result.append(team_dict)
        result.sort(key=lambda t: t["season_results"]["points"], reverse=True)
        return result
