from datetime import datetime
from enum import Enum
from typing import List, Optional
from uuid import UUID, uuid4
from pydantic import BaseModel, Field

class JobStatus(str, Enum):
    UPLOADED = "Uploaded"
    QUEUED = "Queued"
    PROCESSING = "Processing"
    COMPLETED = "Completed"
    FAILED = "Failed"

class WordSegment(BaseModel):
    word: str
    start: float
    end: float
    confidence: float

class Transcript(BaseModel):
    full_text: str
    words: List[WordSegment] = []
    
class RenderConfig(BaseModel):
    resolution: str = "1920x1080"
    format: str = "mp4"

class VideoJob(BaseModel):
    id: UUID = Field(default_factory=uuid4)
    user_id: int
    input_file_path: str
    status: JobStatus = JobStatus.UPLOADED
    transcript: Optional[Transcript] = None
    render_config: RenderConfig = RenderConfig()
    output_file_paths: List[str] = []
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)

    def mark_as_queued(self):
        self.status = JobStatus.QUEUED
        self.updated_at = datetime.utcnow()

    def mark_as_processing(self):
        self.status = JobStatus.PROCESSING
        self.updated_at = datetime.utcnow()

    def mark_as_completed(self, output_paths: List[str]):
        self.status = JobStatus.COMPLETED
        self.output_file_paths = output_paths
        self.updated_at = datetime.utcnow()

    def mark_as_failed(self):
        self.status = JobStatus.FAILED
        self.updated_at = datetime.utcnow()
