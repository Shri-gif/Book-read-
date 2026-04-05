from fastapi import FastAPI, UploadFile, File, Form, HTTPException
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
import uuid
import os
from celery import Celery
from .config import settings
from .processors import pipeline_processor
from .utils.excel_parser import ExcelMetadataParser

app = FastAPI(title="AI eBook Pipeline")
app.mount("/static", StaticFiles(directory="static"), name="static")

celery_app = Celery("tasks", broker=settings.REDIS_URL)

@app.post("/process")
async def process_files(
    files: list[UploadFile] = File(...),
    metadata_file: UploadFile = File(...),
    rewrite_percent: int = Form(0),
    generate_content: bool = Form(False)
):
    """Main processing endpoint"""
    batch_id = str(uuid.uuid4())
    work_dir = f"/tmp/{batch_id}"
    os.makedirs(work_dir, exist_ok=True)
    
    try:
        # Save files
        file_paths = []
        for file in files:
            path = f"{work_dir}/{file.filename}"
            with open(path, "wb") as f:
                f.write(await file.read())
            file_paths.append(path)
        
        # Parse Excel metadata dynamically
        parser = ExcelMetadataParser(metadata_file.file)
        metadata = parser.parse_dynamic()
        
        # Queue processing task
        task = pipeline_processor.delay(
            file_paths=file_paths,
            metadata=metadata,
            work_dir=work_dir,
            rewrite_percent=rewrite_percent,
            generate_content=generate_content
        )
        
        return {"batch_id": batch_id, "task_id": task.id, "status": "queued"}
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/status/{task_id}")
async def get_status(task_id: str):
    task = celery_app.AsyncResult(task_id)
    return {"status": task.status, "result": task.result}


# Add at TOP
import os
os.environ['TESSERACT_CMD'] = '/usr/bin/tesseract'

# Add Health endpoint (line 20 ke baad)
@app.get("/health")
async def health():
    return {"status": "healthy", "tesseract": os.popen('tesseract --version').read()[:100]}

# Fix Redis URL
app.celery_app.conf.broker_url = "redis://localhost:6379/0"
