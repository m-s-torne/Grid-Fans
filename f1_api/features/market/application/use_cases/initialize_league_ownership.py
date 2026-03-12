"""Use case: Initialize driver ownership for a newly created league."""
import logging
from datetime import datetime
from fastapi import HTTPException
from sqlmodel import Session

from f1_api.features.market.infrastructure.models.ownership_model import DriverOwnershipModel
from f1_api.features.market.infrastructure.persistence.ownership_repository import OwnershipRepository
from f1_api.features.drivers.infrastructure.persistence import DriversRepository
from f1_api.features.drivers.application.drivers_utility import DriversUtility

logger = logging.getLogger(__name__)


class InitializeLeagueOwnershipUseCase:
    """
    Initializes driver ownership records for a newly created league.
    Creates one DriverOwnershipModel per active driver, all as free agents.
    """

    def __init__(self, session: Session):
        self.session = session
        self.ownership_repo = OwnershipRepository(session)

    def execute(self, league_id: int, season_year: int) -> int:
        """
        Create DriverOwnershipModel records for all active drivers in season_year.

        Returns:
            Number of records created.
        Raises:
            HTTPException 500 on failure.
        """
        try:
            drivers_repo = DriversRepository(self.session, season_year)
            active_driver_ids = drivers_repo.get_active_driver_ids_for_season(season_year)
            if not active_driver_ids:
                logger.warning("No active drivers found for season %s", season_year)
                return 0

            drivers = drivers_repo.get_by_ids(active_driver_ids)
            enriched_drivers = self._calculate_driver_prices(drivers, drivers_repo)

            created_count = 0
            now = datetime.now()

            for enriched in enriched_drivers:
                driver_id = enriched["id"]
                existing = self.ownership_repo.get_by_driver_and_league(driver_id, league_id)
                if not existing:
                    fantasy_price = enriched.get("fantasy_stats", {}).get("price", 10_000_000)
                    ownership = DriverOwnershipModel(
                        driver_id=driver_id,
                        league_id=league_id,
                        owner_id=None,
                        is_listed_for_sale=False,
                        acquisition_price=fantasy_price,
                        created_at=now,
                        updated_at=now,
                    )
                    self.session.add(ownership)
                    created_count += 1

            logger.info("Initialized %d ownership records for league %d", created_count, league_id)
            return created_count

        except Exception as e:
            logger.error("Failed to initialize league ownership: %s", e)
            raise HTTPException(status_code=500, detail=f"Failed to initialize driver ownership: {e}") from e

    def _calculate_driver_prices(self, drivers: list, drivers_repo: DriversRepository) -> list[dict]:
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
