from app.main import celery_app
from app.processors.converter import EbookPipeline
from app.config import settings

@celery_app.task
def pipeline_processor(file_paths, metadata, work_dir, rewrite_percent, generate_content):
    pipeline = EbookPipeline(settings)
    results = pipeline.process_batch(
        file_paths, metadata, work_dir, 
        rewrite_percent, generate_content
    )
    return results
