import shutil

from fastapi import APIRouter, File, HTTPException, UploadFile

router = APIRouter(prefix="/media", tags=["Media"])

# Assign the function call to a module-level variable
DEFAULT_FILE = File(None)


@router.post("/upload")
async def upload(file: UploadFile = DEFAULT_FILE):
    if not file or not file.filename:
        raise HTTPException(status_code=400, detail="No file uploaded")

    # Save the uploaded file to a directory (e.g., "media")
    file_path = f"media/{file.filename}"
    with open(file_path, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)

    return {
        "detail": f"File '{file.filename}' uploaded successfully",
        "path": file_path,
    }
