from fastapi import FastAPI
from routes.user import user

app = FastAPI(
    title="Simple API CRUD",
    description="API CRUD with FastAPI & SQLAlchemy",
    version = "0.0.1",
    openapi_tags=[{
        "name": "users",
        "description": "Users routes",
    }]
)
app.include_router(user)