from fastapi import FastAPI, UploadFile, File, HTTPException
from fastapi.responses import FileResponse
import os
from pathlib import Path

app = FastAPI()

# Директория для сохранения файлов
UPLOAD_DIR = "./uploads"
os.makedirs(UPLOAD_DIR, exist_ok=True)

@app.post("/upload/")
async def upload_file(file: UploadFile = File(...)):
    try:
        # Сохранение файла
        file_path = Path(UPLOAD_DIR) / Path(file.filename).name
        with open(file_path, "wb") as buffer:
            buffer.write(await file.read())
        
        return {"status": "success", "filename": file.filename, "path": str(file_path)}
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/download/{filename}")
async def download_file(filename: str):
    file_path = Path(UPLOAD_DIR) / filename
    if not file_path.exists():
        raise HTTPException(status_code=404, detail="File not found")
    
    return FileResponse(file_path, filename=filename)

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8001)