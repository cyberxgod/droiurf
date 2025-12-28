from fastapi import FastAPI
from fastapi.responses import FileResponse, JSONResponse
import os

app = FastAPI()

DB_PATH = "/var/data/data.db"

@app.get("/")
def home():
    return {
        "status": "running ✅",
        "download": "/download-db"
    }

@app.get("/download-db")
def download_db():
    if not os.path.exists(DB_PATH):
        return JSONResponse(
            status_code=404,
            content={"error": "data.db not found"}
        )

    return FileResponse(
        path=DB_PATH,
        media_type="application/octet-stream",
        filename="data.db"
    )
