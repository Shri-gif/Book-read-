import pytest
from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

def test_process_files():
    with open("tests/sample.docx", "rb") as f1, \
         open("tests/metadata.xlsx", "rb") as f2:
        
        response = client.post("/process", files={
            "files": ("test.docx", f1, "application/vnd.openxmlformats"),
            "metadata_file": ("metadata.xlsx", f2, "application/vnd.ms-excel")
        })
    
    assert response.status_code == 200
    assert "batch_id" in response.json()

# More tests for OCR, conversion, AI processing...
