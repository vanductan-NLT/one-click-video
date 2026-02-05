from abc import ABC, abstractmethod
from typing import List, Optional
from uuid import UUID
from .entities import VideoJob

class IVideoRepository(ABC):
    @abstractmethod
    async def save(self, job: VideoJob) -> None:
        pass

    @abstractmethod
    async def get_by_id(self, job_id: UUID) -> Optional[VideoJob]:
        pass

    @abstractmethod
    async def get_by_user_id(self, user_id: int) -> List[VideoJob]:
        pass

    @abstractmethod
    async def delete(self, job_id: UUID) -> None:
        pass

    @abstractmethod
    async def find_by_status(self, status: str) -> List[VideoJob]:
        pass
