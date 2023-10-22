from fastapi import FastAPI

from app.models.baseModel import Response

app = FastAPI()


@app.get("/", response_model=Response)
async def welcome():
    return Response(success=True, message="OK")
