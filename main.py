from fastapi import FastAPI
from endpoints import user, role, customer, bid

app = FastAPI()
app.include_router(user.router)
app.include_router(role.router)
app.include_router(customer.router)
app.include_router(bid.router)


@app.get("/")
async def root():
    return {"message": "Hello Bigger Applications!"}
