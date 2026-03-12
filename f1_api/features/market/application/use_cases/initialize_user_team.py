"""Use case: Initialize user team when joining a league."""
import logging
import random
from datetime import datetime
from fastapi import HTTPException
from sqlmodel import Session, select

from f1_api.features.market.domain.interfaces import IOwnershipRepository, ITransactionRepository
from f1_api.features.market.domain.entities import MarketTransaction
from f1_api.features.user_teams.domain.interfaces import UserTeamsRepository
from f1_api.features.drivers.domain.interfaces import DriversRepository as IDriversRepository
from f1_api.features.teams.domain.models import Teams
from f1_api.features.user_teams.domain.models import UserTeams

logger = logging.getLogger(__name__)

INITIAL_BUDGET = 100_000_000
CURRENT_SEASON = 2025  # TODO: Get dynamically


class InitializeUserTeamUseCase:
    """
    Initializes a user's team when they join a league.
    Assigns 3 random Tier C drivers (free), creates UserTeams record with 100M budget.
    """

    def __init__(
        self,
        ownership_repo: IOwnershipRepository,
        transactions_repo: ITransactionRepository,
        user_teams_repo: UserTeamsRepository,
        drivers_repo: IDriversRepository,
        session: Session,  # TODO: move Teams lookup and UserTeams creation behind repo interfaces
    ):
        self.ownership_repo = ownership_repo
        self.transactions_repo = transactions_repo
        self.user_teams_repo = user_teams_repo
        self.drivers_repo = drivers_repo
        self.session = session

    def execute(self, user_id: int, league_id: int) -> dict:
        """
        Returns dict with team_id, assigned_drivers, constructor_id, total_cost, budget_remaining.
        Raises HTTPException on validation failure or insufficient drivers.
        """
        if self.user_teams_repo.has_active_team(league_id, user_id):
            raise HTTPException(400, "User already has a team in this league")

        free_ownerships = self.ownership_repo.get_free_drivers_in_league(league_id)
        if len(free_ownerships) < 3:
            raise HTTPException(500, "Not enough free drivers available to initialize team")

        database_data = self.drivers_repo.get_driver_results_data()
        points_map = {r.driver_id: r.total_points for r in database_data["results"]}

        drivers_with_points = [(o.driver_id, points_map.get(o.driver_id, 0)) for o in free_ownerships]
        tiers = self._classify_drivers_by_tier(drivers_with_points)

        available_low_tier = tiers["tier_c"] + tiers["tier_b"]
        if len(available_low_tier) < 3:
            available_low_tier = [d[0] for d in drivers_with_points]

        selected_driver_ids = random.sample(available_low_tier, 3)
        assigned_drivers = []

        for driver_id in selected_driver_ids:
            ownership = next((o for o in free_ownerships if o.driver_id == driver_id), None)
            if not ownership:
                continue
            ownership.owner_id = user_id
            ownership.is_listed_for_sale = False
            ownership.locked_until = None
            ownership.updated_at = datetime.now()
            self.ownership_repo.update(ownership)
            assigned_drivers.append(driver_id)

            transaction = MarketTransaction(
                driver_id=driver_id,
                league_id=league_id,
                seller_id=None,
                buyer_id=user_id,
                transaction_price=0,
                transaction_type="emergency_assignment",
                transaction_date=datetime.now(),
            )
            self.transactions_repo.create(transaction)

        default_constructor = self.session.exec(select(Teams)).first()
        if not default_constructor:
            raise HTTPException(500, "No constructors available")

        new_team = UserTeams(
            user_id=user_id,
            league_id=league_id,
            team_name=f"Team {user_id}",
            driver_1_id=assigned_drivers[0],
            driver_2_id=assigned_drivers[1],
            driver_3_id=assigned_drivers[2],
            reserve_driver_id=None,
            constructor_id=default_constructor.id,
            total_points=0,
            budget_remaining=INITIAL_BUDGET,
            is_active=True,
        )
        self.session.add(new_team)
        self.session.flush()

        return {
            "team_id": new_team.id,
            "assigned_drivers": assigned_drivers,
            "constructor_id": default_constructor.id,
            "total_cost": 0,
            "budget_remaining": INITIAL_BUDGET,
        }

    def _classify_drivers_by_tier(self, drivers_with_points: list) -> dict:
        if not drivers_with_points:
            return {"tier_a": [], "tier_b": [], "tier_c": []}
        sorted_drivers = sorted(drivers_with_points, key=lambda x: x[1], reverse=True)
        max_points = sorted_drivers[0][1] if sorted_drivers[0][1] > 0 else 1
        tiers: dict[str, list] = {"tier_a": [], "tier_b": [], "tier_c": []}
        for driver_id, points in sorted_drivers:
            pct = (points / max_points) * 100
            if pct >= 70:
                tiers["tier_a"].append(driver_id)
            elif pct >= 40:
                tiers["tier_b"].append(driver_id)
            else:
                tiers["tier_c"].append(driver_id)
        return tiers
