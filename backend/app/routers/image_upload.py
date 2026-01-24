"""
Image Upload Router
Handles image upload for fraud detection
"""
from fastapi import APIRouter, UploadFile, File, HTTPException
from typing import List
import os
import uuid
from datetime import datetime

router = APIRouter()

# Upload directory
UPLOAD_DIR = "app/uploads"

# Allowed image types
ALLOWED_EXTENSIONS = {".jpg", ".jpeg", ".png", ".webp"}
MAX_FILE_SIZE = 10 * 1024 * 1024  # 10MB


def validate_image(file: UploadFile) -> bool:
    """Validate image file type"""
    if not file.filename:
        return False
    
    ext = os.path.splitext(file.filename)[1].lower()
    return ext in ALLOWED_EXTENSIONS


@router.post("/upload-images")
async def upload_images(files: List[UploadFile] = File(...)):
    """
    Upload multiple images for fraud detection
    
    Args:
        files: List of image files
        
    Returns:
        dict: Uploaded file information with paths
    """
    if not files:
        raise HTTPException(status_code=400, detail="No files provided")
    
    if len(files) > 10:
        raise HTTPException(status_code=400, detail="Maximum 10 images allowed")
    
    uploaded_files = []
    
    for file in files:
        # Validate file type
        if not validate_image(file):
            raise HTTPException(
                status_code=400,
                detail=f"Invalid file type: {file.filename}. Allowed: JPG, PNG, WEBP"
            )
        
        # Generate unique filename
        ext = os.path.splitext(file.filename)[1].lower()
        unique_filename = f"{uuid.uuid4()}{ext}"
        file_path = os.path.join(UPLOAD_DIR, unique_filename)
        
        # Save file
        try:
            contents = await file.read()
            
            # Check file size
            if len(contents) > MAX_FILE_SIZE:
                raise HTTPException(
                    status_code=400,
                    detail=f"File too large: {file.filename}. Maximum 10MB"
                )
            
            with open(file_path, "wb") as f:
                f.write(contents)
            
            uploaded_files.append({
                "original_filename": file.filename,
                "saved_filename": unique_filename,
                "file_path": file_path,
                "size_bytes": len(contents)
            })
            
        except Exception as e:
            raise HTTPException(
                status_code=500,
                detail=f"Error uploading {file.filename}: {str(e)}"
            )
    
    return {
        "status": "success",
        "uploaded_count": len(uploaded_files),
        "files": uploaded_files
    }


@router.get("/upload-status")
async def get_upload_status():
    """Get upload service status"""
    return {
        "status": "operational",
        "upload_dir": UPLOAD_DIR,
        "max_files": 10,
        "max_size_mb": 10,
        "allowed_types": list(ALLOWED_EXTENSIONS)
    }
