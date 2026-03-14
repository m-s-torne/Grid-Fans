"""Admin domain interfaces."""
from typing import Protocol
from sqlmodel import Session
from f1_api.core.f1_data.domain.models import Events, Sessions, SessionResult
from f1_api.core.f1_data.domain.interfaces import ISeasonContext, DriverTeamLinkRepository as IDriverTeamLinkRepository
from f1_api.features.teams.domain.models import Teams
from f1_api.features.drivers.domain.models import Drivers, DriverTeamLink
from f1_api.features.drivers.domain.interfaces import DriversRepository as IDriversRepository
from f1_api.features.teams.domain.interfaces import TeamsRepository as ITeamsRepository


class IGetEventData(Protocol):
    def __call__(self, session: Session, year: int) -> list[Events]: ...


class IGetSessionData(Protocol):
    def __call__(self, session: Session, year: int) -> list[Sessions]: ...


class IGetSessionResults(Protocol):
    def __call__(self, year: int, session: Session) -> list[SessionResult]: ...


class IGetTeamData(Protocol):
    def __call__(self, session: Session) -> list[Teams]: ...


class IGetDriverData(Protocol):
    def __call__(
        self,
        session: Session,
        driver_repo: IDriversRepository,
        season_context: ISeasonContext,
    ) -> list[Drivers]: ...


class IGetAllDriverTeamLinks(Protocol):
    def __call__(
        self,
        year: int,
        driver_repo: IDriversRepository,
        team_repo: ITeamsRepository,
        link_repo: IDriverTeamLinkRepository,
        season_context: ISeasonContext,
    ) -> list[DriverTeamLink]: ...


class IReconcileDriverTeamLinks(Protocol):
    async def __call__(
        self,
        session: Session,
        year: int,
        driver_repo: IDriversRepository,
        team_repo: ITeamsRepository,
        link_repo: IDriverTeamLinkRepository,
        season_context: ISeasonContext,
    ) -> list[DriverTeamLink]: ...
