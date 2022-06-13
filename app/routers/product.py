from multiprocessing import synchronize
from fastapi import Depends, status, APIRouter
from .. import models, schemas
from ..database import get_db
from sqlalchemy.orm import Session
from app import oauth2

router = APIRouter(
    prefix = "/product",
    tags = ['Products']
)
def check_valid_quantity(quantity):
    if quantity>=0:
        return schemas.ProductOut(
            status = status.HTTP_200_OK,
            message = "valid quantity"
        )
    return schemas.ProductOut(
        status = status.HTTP_406_NOT_ACCEPTABLE,
        message = "Invalid quantity"
    )
@router.post("/", status_code = status.HTTP_201_CREATED, response_model = schemas.ProductOut)
def add_product(product: schemas.ProductCreate, db: Session = Depends(get_db), current_user: int = Depends(oauth2.get_current_user)):
    response = check_valid_quantity(product.quantity)
    if response.status == status.HTTP_406_NOT_ACCEPTABLE:
        return response
    new_product = models.Product(**product.dict())
    db.add(new_product)
    db.commit()
    db.refresh(new_product)
    return schemas.ProductOut(**new_product.__dict__,
            status = status.HTTP_201_CREATED,
            message = "Product added successfully"
        )

@router.get("/{id}", response_model = schemas.ProductOut)
def get_product_by_id(id: int, db: Session = Depends(get_db), current_user: int = Depends(oauth2.get_current_user)):
    product = db.query(models.Product).filter(models.Product.id == id).first()
    if not product:
        return schemas.ProductOut(
            status = status.HTTP_404_NOT_FOUND,
            message = "No Product Found"
        )
    return schemas.ProductOut( **product.__dict__,
        message = "Product with id: {id}",
        status = status.HTTP_200_OK
    )

@router.get("/", response_model = schemas.ProductsOut)
def get_products(db: Session = Depends(get_db), limit: int = 10, skip: int = 0, current_user: int = Depends(oauth2.get_current_user)):
    products = db.query(models.Product).limit(limit).offset(skip).all()
    return schemas.ProductsOut(list=[schemas.ProductOut(** product.__dict__) for product in products],
        message="all products",
        status=status.HTTP_200_OK
    )

@router.put("/{id}", status_code = status.HTTP_200_OK, response_model = schemas.ProductOut)
def update_product(id: int, product: schemas.ProductCreate, db: Session = Depends (get_db), current_user: int = Depends(oauth2.get_current_user)):
    product_to_update_query = db.query(models.Product).filter(models.Product.id == id)
    if not product_to_update_query.first():
        return schemas.ProductOut(
            status = status.HTTP_404_NOT_FOUND,
            message= "Product Not Found "
        )
    response = check_valid_quantity(product.quantity)
    if response.status == status.HTTP_406_NOT_ACCEPTABLE:
        return response 
    product_to_update_query.update({**product.dict()}, synchronize_session=False)
    db.commit()
    return schemas.ProductOut(**product_to_update_query.first().__dict__,
            status = status.HTTP_200_OK,
            message = "Product updated successfully"
    )

@router.delete("/{id}", status_code = status.HTTP_200_OK, response_model = schemas.ProductOut)
def delete_product(id: int, db: Session = Depends(get_db), current_user: int = Depends(oauth2.get_current_user)):
    query = db.query(models.Product).filter(models.Product.id == id)
    if not query:
        return schemas.ProductOut(
            status = status.HTTP_404_NOT_FOUND,
            message = "Product Not Found"
        ) 
    query.delete(synchronize_session = False)
    db.commit()
    return schemas.ProductOut(
        message = "Product successfully deleted ",
        status = status.HTTP_200_OK
    )
