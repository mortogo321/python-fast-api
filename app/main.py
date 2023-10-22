from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.models.baseModel import Response

app = FastAPI()

origins = [
    "http://localhost:8080",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/", response_model=Response)
async def welcome():
    return Response(success=True, message="OK")
