from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from endpoints import user, role, customer, bid, project

app = FastAPI()
app.include_router(user.router)
app.include_router(role.router)
app.include_router(customer.router)
app.include_router(bid.router)
app.include_router(project.router)

origins = [
    "http://localhost:5173",
    # TODO - add deployed app url to allow traffic from it
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/")
async def root():
    return {"message": "Hello Bigger Applications!"}
