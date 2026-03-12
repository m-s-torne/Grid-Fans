"""Admin domain interfaces."""
from typing import Protocol
from sqlmodel import Session
from f1_api.core.f1_data.domain.models import Events, Sessions, SessionResult
from f1_api.features.teams.domain.models import Teams


class IGetEventData(Protocol):
    def __call__(self, session: Session, year: int) -> list[Events]: ...


class IGetSessionData(Protocol):
    def __call__(self, session: Session, year: int) -> list[Sessions]: ...


class IGetSessionResults(Protocol):
    def __call__(self, year: int, session: Session) -> list[SessionResult]: ...


class IGetTeamData(Protocol):
    def __call__(self, session: Session) -> list[Teams]: ...
