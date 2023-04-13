from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from deta import Deta

deta = Deta("e0h2cutqoow_Qgi1mF4jpgxHGhDsS3mNj8MWttvPwiUa")

app = FastAPI

db = deta.base('Products')

class Product(BaseModel):
    key: str | None
    name: str
    description: str
    price: float
    image: str
    version: int
    active: int

@app.put('/update_product/{key}')

async def constrol_update_product(product: Product, key: str):
    update = db.update(product.dict(exclude={'key'}), key)
    
    if  update != None:
        raise HTTPException(status_code=404, detail="Product not found")
    
    return product
#pensar em onde adicionar as versoes anteriores do produto
# @app.post('/produto_destualizado/{key}')

# async def 