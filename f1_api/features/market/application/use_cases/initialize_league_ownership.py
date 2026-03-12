"""Use case: Initialize driver ownership for a newly created league."""
import logging
from datetime import datetime
from fastapi import HTTPException

from f1_api.features.market.domain.interfaces import IOwnershipRepository
from f1_api.features.market.domain.entities import DriverOwnership
from f1_api.features.drivers.domain.interfaces import DriversRepository as IDriversRepository
from f1_api.features.drivers.application.drivers_utility import DriversUtility

logger = logging.getLogger(__name__)


class InitializeLeagueOwnershipUseCase:
    """
    Initializes driver ownership records for a newly created league.
    Creates one DriverOwnership per active driver, all as free agents.
    """

    def __init__(
        self,
        ownership_repo: IOwnershipRepository,
        drivers_repo: IDriversRepository,
    ):
        self.ownership_repo = ownership_repo
        self.drivers_repo = drivers_repo

    def execute(self, league_id: int, season_year: int) -> int:
        """
        Create DriverOwnership records for all active drivers in season_year.

        Returns:
            Number of records created.
        Raises:
            HTTPException 500 on failure.
        """
        try:
            active_driver_ids = self.drivers_repo.get_active_driver_ids_for_season(season_year)
            if not active_driver_ids:
                logger.warning("No active drivers found for season %s", season_year)
                return 0

            drivers = self.drivers_repo.get_by_ids(active_driver_ids)
            enriched_drivers = self._calculate_driver_prices(drivers, self.drivers_repo)

            created_count = 0
            now = datetime.now()

            for enriched in enriched_drivers:
                driver_id = enriched["id"]
                existing = self.ownership_repo.get_by_driver_and_league(driver_id, league_id)
                if not existing:
                    fantasy_price = enriched.get("fantasy_stats", {}).get("price", 10_000_000)
                    ownership = DriverOwnership(
                        driver_id=driver_id,
                        league_id=league_id,
                        owner_id=None,
                        is_listed_for_sale=False,
                        acquisition_price=fantasy_price,
                        asking_price=None,
                        locked_until=None,
                        created_at=now,
                        updated_at=now,
                    )
                    self.ownership_repo.create(ownership)
                    created_count += 1

            logger.info("Initialized %d ownership records for league %d", created_count, league_id)
            return created_count

        except Exception as e:
            logger.error("Failed to initialize league ownership: %s", e)
            raise HTTPException(status_code=500, detail=f"Failed to initialize driver ownership: {e}") from e

    def _calculate_driver_prices(self, drivers: list, drivers_repo: IDriversRepository) -> list[dict]:
        utility = DriversUtility()
        database_data = drivers_repo.get_driver_results_data()
        stats = utility.get_driver_stats(database_data["all_results"])
        points_map = {r.driver_id: r.total_points for r in database_data["results"]}

        enriched = []
        for driver in drivers:
            driver_stats = stats.get(driver.id, {})
            points = points_map.get(driver.id, 0)
            podiums = driver_stats.get("podiums", 0)
            victories = driver_stats.get("victories", 0)
            price = 10_000_000 + (int(points) * 10_000) + (podiums * 50_000) + (victories * 100_000)
            enriched.append({"id": driver.id, "fantasy_stats": {"price": price}})
        return enriched
