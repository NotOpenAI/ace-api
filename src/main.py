from fastapi import FastAPI, status

app = FastAPI()


@app.get("/items/{item_id}")
async def read_item(item_id: int):
    return {"item_id": item_id}

@app.get(
    "/init_tables",
    status_code=status.HTTP_200_OK,
    name="init_tables"
)
async def init_tables():
    create_tables()