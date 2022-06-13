from typing import Optional, List
from fastapi import FastAPI, Response, Depends, status, HTTPException, APIRouter
from sqlalchemy import func

from app.models import photo
from .. import models, schemas
from ..database import get_db
from sqlalchemy.orm import Session
from app import oauth2

router = APIRouter(
    prefix="/photo",
    tags=['Photos']
)
@router.post("/", status_code=status.HTTP_201_CREATED, response_model=schemas.PhotoOut)
def add_photo(photo: schemas.PhotoCreate, db: Session = Depends(get_db), current_user: int = Depends(oauth2.get_current_user)):

    dog = db.query(models.Dog).filter(models.Dog.id == photo.dog_id).first()

    if not dog:
        return schemas.PhotoOut(status=status.HTTP_404_NOT_FOUND,
                                message="Dog does not exist")   

    new_photo = models.Photo(**photo.dict())
                    
    db.add(new_photo)
    db.commit()
    db.refresh(new_photo)

    return schemas.PhotoOut(**new_photo.__dict__, 
                status=status.HTTP_201_CREATED,
                message="Photo added successfully"
            )
@router.get("/{id}", response_model=schemas.PhotoOut)
def get_photo_by_id(id: int, db: Session = Depends(get_db), current_user: int = Depends(oauth2.get_current_user)):
    photo = db.query(models.Photo).filter(models.Photo.id == id).first()
    if not photo:
       return schemas.PhotoOut( 
                status=status.HTTP_404_NOT_FOUND,
                message="Photo not found"
            ) 
    return schemas.PhotoOut(**photo.__dict__,
                message=f"photo with id: {id}",
                status=status.HTTP_200_OK)

@router.get("/", response_model=schemas.PhotosOut)
def get_photos(db: Session = Depends(get_db), current_user: int = Depends(oauth2.get_current_user), limit: int = 10, skip: int = 0, dog_id: Optional[int] = None):
    
    photos = db.query(models.Photo)
    if dog_id:
        photos = photos.filter(models.Photo.dog_id == dog_id)

    photos = photos.limit(limit).offset(skip).all()
    
    return schemas.PhotosOut(list=[schemas.PhotoOut(**photo.__dict__) for photo in  photos],
                message="all photos",
                status=status.HTTP_200_OK
                )

@router.put("/{id}", status_code=status.HTTP_200_OK, response_model=schemas.PhotoOut)
def update_photo(id: int, photo: schemas.PhotoCreate, db: Session = Depends(get_db), current_user: int = Depends(oauth2.get_current_user)):

    photo_to_update_query = db.query(models.Photo).filter(models.Photo.id == id)

    if not photo_to_update_query.first():
       return schemas.PhotoOut( 
                status=status.HTTP_404_NOT_FOUND,
                message="Photo not found"
            ) 

    photo_to_update_query.update({**photo.dict()}, synchronize_session=False)
    db.commit()

    return schemas.PhotoOut(**photo_to_update_query.first().__dict__, 
                status=status.HTTP_200_OK,
                message="photo updated successfully"
            )

@router.delete("/{id}", status_code=status.HTTP_200_OK, response_model=schemas.PhotoOut)
def delete_photo(id: int, db: Session = Depends(get_db), current_user: int = Depends(oauth2.get_current_user)):
    photo_query = db.query(models.Photo).filter(models.Photo.id == id)
    if not photo_query:
       return schemas.PhotoOut( 
                status=status.HTTP_404_NOT_FOUND,
                message="Photo not found"
            ) 
    photo_query.delete(synchronize_session=False)
    db.commit()
    return schemas.PhotoOut(
                status=status.HTTP_200_OK,
                message="Photo deleted successfully"
            )
