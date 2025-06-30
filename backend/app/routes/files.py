from fastapi import APIRouter, HTTPException
from fastapi.responses import FileResponse
import os

router = APIRouter(prefix="/static/files", tags=["files"])

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
UPLOAD_DIR = os.path.join(BASE_DIR, "../../uploads")

@router.get("/{file_path:path}")
async def read_file(file_path: str):
    full_path = os.path.join(UPLOAD_DIR, file_path)

    if not os.path.isfile(full_path) or not os.path.realpath(full_path).startswith(os.path.realpath(UPLOAD_DIR)):
        raise HTTPException(status_code=404, detail="Fichier introuvable ou accès interdit")

    return FileResponse(full_path)