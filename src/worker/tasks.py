from src.worker.celery_app import celery_app
import time
import structlog

logger = structlog.get_logger()

@celery_app.task(name="process_video_task")
def process_video_task(job_id: str):
    logger.info("Starting video processing task", job_id=job_id)
    
    # Simulate work
    time.sleep(5)
    
    logger.info("Video processing task completed", job_id=job_id)
    return {"status": "completed", "job_id": job_id}
