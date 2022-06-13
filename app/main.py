from itertools import product
from fastapi import FastAPI
from .routers import user, auth, photo, product
from fastapi.middleware.cors import CORSMiddleware

# Raouf : uncomment this line if you want to add a new model 
#         if you modify and existing model, you need alembic to update database
#models.Base.metadata.create_all(bind=engine)

app = FastAPI()

# Raouf : FIX IT Later after deploying the front end, allow only our web server instead of all "*"  
origins = [
    "*"
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(user.router)
app.include_router(auth.router)
app.include_router(photo.router)
app.include_router(product.router)
@app.get("/")
def root():
    return {"message": "Welcome to projet backend !"}
