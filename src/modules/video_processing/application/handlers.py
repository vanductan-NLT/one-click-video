from uuid import UUID
from typing import Optional
from .entities import VideoJob, JobStatus
from .repositories import IVideoRepository

class ProcessVideoJobUseCase:
    def __init__(self, video_repo: IVideoRepository):
        self.video_repo = video_repo

    async def execute(self, job_id: UUID) -> Optional[VideoJob]:
        job = await self.video_repo.get_by_id(job_id)
        if not job:
            return None
        
        # Placeholder for complex pipeline logic
        # silence detection -> ASR -> JSON -> B-roll -> text -> render
        
        job.mark_as_processing()
        await self.video_repo.save(job)
        
        return job

class CreateVideoJobUseCase:
    def __init__(self, video_repo: IVideoRepository):
        self.video_repo = video_repo

    async def execute(self, user_id: int, input_file_path: str) -> VideoJob:
        job = VideoJob(user_id=user_id, input_file_path=input_file_path)
        await self.video_repo.save(job)
        return job
