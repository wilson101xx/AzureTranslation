import logging
import shutil
import os
from zipfile import ZipFile
from fastapi import APIRouter, UploadFile, File, Query, HTTPException, BackgroundTasks
from fastapi.responses import FileResponse
from typing import List
from src.modules.translate_documents import document_translation, get_language_code

# Configure Logging
logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)
logger.addHandler(logging.StreamHandler())

router = APIRouter()

UPLOAD_DIR = "uploaded_files"
os.makedirs(UPLOAD_DIR, exist_ok=True)

def remove_file(file_path: str):
    """Removes a file and logs the action."""
    try:
        os.remove(file_path)
        logger.info(f"Removed file: {file_path}")
    except Exception as e:
        logger.error(f"Error removing file {file_path}: {e}")

@router.post("/upload")
async def create_upload_file(
    background_tasks: BackgroundTasks,
    file: UploadFile = File(...),
    source_language: str = Query(...), 
    target_languages: List[str] = Query(...)
):
    """Upload a document for translation and receive translated files."""
    file_path = os.path.join(UPLOAD_DIR, file.filename)

    logger.info(f"Received file upload request: {file.filename} | Source Language: {source_language} | Target Languages: {target_languages}")

    try:
        with open(file_path, "wb") as buffer:
            shutil.copyfileobj(file.file, buffer)
        logger.info(f"Saved uploaded file to: {file_path}")

        translations = []
        source_language_code = get_language_code(source_language)
        if not source_language_code:
            logger.error(f"Invalid source language: {source_language}")
            raise HTTPException(status_code=400, detail="Invalid source language")

        for target_language in target_languages:
            target_language_code = get_language_code(target_language)
            if not target_language_code:
                logger.error(f"Invalid target language: {target_language}")
                continue

            translated_file_path = document_translation(file_path, source_language_code, target_language_code)
            if translated_file_path:
                translations.append(translated_file_path)
                logger.info(f"Translation completed: {translated_file_path}")
            else:
                logger.error(f"Translation failed for target language: {target_language}")

        # Schedule deletion of translated files
        for t_file in translations:
            background_tasks.add_task(remove_file, t_file)
        background_tasks.add_task(remove_file, file_path)

        if len(translations) == 1:
            logger.info(f"Returning single translated file: {translations[0]}")
            return FileResponse(translations[0], media_type="application/octet-stream", filename=os.path.basename(translations[0]))

        # Create ZIP file if multiple translations exist
        zip_file_path = os.path.join(UPLOAD_DIR, "translated_files.zip")
        with ZipFile(zip_file_path, "w") as zipf:
            for translated_file in translations:
                zipf.write(translated_file, arcname=os.path.basename(translated_file))

        background_tasks.add_task(remove_file, zip_file_path)
        logger.info(f"Returning ZIP archive with translated files: {zip_file_path}")
        return FileResponse(zip_file_path, media_type="application/zip", filename="translated_files.zip")

    except Exception as e:
        logger.exception(f"Error processing translation: {e}")
        background_tasks.add_task(remove_file, file_path)
        raise HTTPException(status_code=500, detail=str(e))
