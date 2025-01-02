from abc import ABC
from dataclasses import dataclass

from src.repositories.database.base import DatabaseRepositories


@dataclass
class Repositories(ABC):
    database: DatabaseRepositories | None = None