from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from deta import Deta

deta = Deta("e0h2cutqoow_Qgi1mF4jpgxHGhDsS3mNj8MWttvPwiUa")

app = FastAPI()

db = deta.Base("Products")

class Product(BaseModel):
    key: str | None
    name: str
    description: str
    category: str
    price: float
    image: str
    version: int
    active: int

@app.post('/product')
async def post_product(product: Product):
    
    inserted = db.insert(product.dict(exclude={'key'}))

    
    return inserted