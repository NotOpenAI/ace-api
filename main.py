from fastapi import FastAPI
from endpoints import user, role

app = FastAPI()
app.include_router(user.router)
app.include_router(role.router)


@app.get("/")
async def root():
    return {"message": "Hello Bigger Applications!"}
