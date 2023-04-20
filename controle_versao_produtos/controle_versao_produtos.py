from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from deta import Deta

deta = Deta("e0h2cutqoow_Qgi1mF4jpgxHGhDsS3mNj8MWttvPwiUa")

app = FastAPI

db = deta.base('ProductDatabase')

db_prod_outdated = deta.base('OutdatedProducts')

class Product(BaseModel):
    key: str | None
    first_vesion_key: str
    name: str
    description: str
    price: float
    image: str
    version: int
    active: int
    weight: float

#pensar em onde adicionar as versoes anteriores do produto
@app.post('/outdated_products')

async def outdated_products(product: Product):
    create = db_prod_outdated.insert(product.dict(exclude={'key'}))

    return create

@app.put('/update_product/{key}')

async def constrol_update_product(product: Product, key: str):
    update = db.update(product.dict(exclude={'key'}), key)
    
    if  update != None:
        raise HTTPException(status_code=404, detail="Product not found")
    
    outdated_products(product)
    return product