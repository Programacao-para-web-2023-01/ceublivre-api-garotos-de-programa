from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from deta import Deta

deta = Deta("e0h2cutqoow_Qgi1mF4jpgxHGhDsS3mNj8MWttvPwiUa")

app = FastAPI()

db = deta.Base("Products") #Base de produtos(ativos)

class Product(BaseModel):
    key: str | None
    name: str
    description: str
    category: str
    price: float
    image: str
    version: int
    active: int

@app.put("/product/{key}")
async def update_product(product: Product, key: str):
    
    updated = db.update(product.dict(exclude={'key'}), key)

    if updated != None:
        raise HTTPException(status_code=404, detail="Product not found")

    return product