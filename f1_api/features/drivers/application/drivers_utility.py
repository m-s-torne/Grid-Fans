import os
import unicodedata
from sqlmodel import select
from f1_api.features.drivers.domain.models import DriverTeamLink
from f1_api.features.teams.domain.models import Teams

class DriversUtility:
    @staticmethod
    def create_driver_id(full_name) -> str:
        full_name = unicodedata.normalize("NFKD", full_name).encode("ascii", "ignore").decode("utf-8")
        full_name = full_name.lower().strip()
        parts = full_name.split()
        if len(parts) < 2:
            raise ValueError("Error in create_driver_id, name and surname needed")
        first, last = parts[0], parts[-1]
        driver_id = first[:3] + last[:3] + "01"
        return driver_id

    @staticmethod
    def get_driver_headshot_url(year,team_name,driver_id):
        base = os.environ.get("HEADSHOT_URL_BASE")
        path = f"/common/f1/{year}/{team_name}/{driver_id}/{year}{team_name}{driver_id}right.webp"
        final_url = f"{base}{path}"
        return final_url
    
    @staticmethod
    def get_driver_stats(all_results):
        """
        Maps stats for all drivers
        """
        stats = {}
        for r in all_results:
            driver_id = r.driver_id
            if driver_id not in stats:
                stats[driver_id] = {
                    "poles": 0,
                    "podiums": 0,
                    "fastest_laps": 0,
                    "victories": 0,
                    "sprint_podiums": 0,
                    "sprint_victories": 0,
                    "sprint_poles": 0,
                    "finish_positions": [],
                    "grid_positions": [],
                    "pole_victories": 0,
                    "overtakes": [],
                }
            if r.session_number == 5:
                if r.grid_position == 1:
                    stats[driver_id]["poles"] += 1
                    if r.position == "1":
                        stats[driver_id]["pole_victories"] += 1
                if r.grid_position and isinstance(r.grid_position, int):
                    stats[driver_id]["grid_positions"].append(r.grid_position)
                if r.position in ["1", "2", "3"]:
                    stats[driver_id]["podiums"] += 1
                if r.position and r.position.isdigit():
                    stats[driver_id]["finish_positions"].append(int(r.position))
                else:
                    stats[driver_id]["finish_positions"].append(20)
                if r.position == "1":
                    stats[driver_id]["victories"] += 1
                if r.fastest_lap == 1:
                    stats[driver_id]["fastest_laps"] += 1
                if r.position and r.position.isdigit() and r.grid_position and isinstance(r.grid_position, int):
                    stats[driver_id]["overtakes"].append(int(r.position) - r.grid_position)
                else:
                    stats[driver_id]["overtakes"].append(0)
            if r.session_number == 3:
                if r.position in ["1", "2", "3"]:
                    stats[driver_id]["sprint_podiums"] += 1
                if r.position == "1":
                    stats[driver_id]["sprint_victories"] += 1
                if r.grid_position == 1:
                    stats[driver_id]["sprint_poles"] += 1
        return stats
    
    @staticmethod
    def get_drivers_mapped(max_round,stats,points_map,available_points,drivers_sorted,session):
        """
        Drivers final result
        """
        drivers = []

        for d in drivers_sorted:
            driver_dict = d.model_dump()
            team_id = session.exec(
                select(DriverTeamLink.team_id)
                .where((DriverTeamLink.driver_id == d.id) & (DriverTeamLink.round_number == max_round))
            ).first()
            team_name = session.exec(
                select(Teams.team_name)
                .where(Teams.id == team_id)
            ).first() if team_id else None
            if team_id is None:
                team_id = session.exec(
                    select(DriverTeamLink.team_id)
                    .where((DriverTeamLink.driver_id == d.id))
                ).first()
                team_name = session.exec(
                    select(Teams.team_name)
                    .where(Teams.id == team_id)
                ).first()
            driver_dict["team_name"] = team_name
            driver_stats = stats.get(d.id, {})
            finishes = driver_stats.get("finish_positions", None)
            grids = driver_stats.get("grid_positions", None)
            pole_victories = driver_stats.get("pole_victories", None)
            poles = driver_stats.get("poles", 0)
            points = points_map.get(d.id, 0)
            podiums = driver_stats.get("podiums", 0)
            victories = driver_stats.get("victories", 0)
            overtakes = driver_stats.get("overtakes", 0)
            driver_dict["season_results"] = {
                "points": points,
                "poles": poles,
                "podiums": podiums,
                "fastest_laps": driver_stats.get("fastest_laps", 0),
                "victories": victories,
                "sprint_podiums": driver_stats.get("sprint_podiums", 0),
                "sprint_victories": driver_stats.get("sprint_victories", 0),
                "sprint_poles": driver_stats.get("sprint_poles", 0)
            }
            driver_dict["fantasy_stats"] = {
                "avg_finish": round(sum(finishes) / len(finishes), 1) if finishes else 0,
                "avg_grid_position": round(sum(grids) / len(grids), 1) if grids else 0,
                "pole_win_conversion": round(((pole_victories * 100) / poles ), 1) if poles else 0,
                "price": round(1000000 + (points * 1000) + (podiums * 5000) + (victories * 10000), 0),
                "overtake_efficiency": round(sum(overtakes) / len(overtakes), 1) if overtakes else 0,
                "available_points_percentatge": round(points * 100 / available_points, 1) if available_points > 0 else 0,
            }
            drivers.append(driver_dict)
        return drivers
