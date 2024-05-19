from fastapi import FastAPI

from routers.dev_router import dev_router

app = FastAPI()

app.include_router(dev_router)

@app.get("/")
async def root():
    return {"message": "Hello, World!"}
