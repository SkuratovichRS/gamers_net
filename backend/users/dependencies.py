from backend.core.database import DbSession
from backend.users.service import Service


def create_service() -> Service:
    return Service(DbSession())
