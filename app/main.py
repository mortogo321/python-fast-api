from fastapi import FastAPI

app = FastAPI()


@app.get("/")
async def welcome():
    return {"success": True, "message": "OK"}
