from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from deta import Deta

deta = Deta("e0h2cutqoow_Qgi1mF4jpgxHGhDsS3mNj8MWttvPwiUa")

app = FastAPI()

db = deta.Base('Product')

db_prod_outdated = deta.Base('ProductDatabase')

class Product(BaseModel):
    key: str | None
    first_key: str
    name: str
    description: str
    price: float
    image: str
    version: int
    active: int
    weight: float

#pensar em onde adicionar as versoes anteriores do produto
@app.post('/outdated_Products')
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


@app.post('/product_variation')

async def product_variation(product: Product):
    create = db.insert(product.dict(exclude={'key'}))
    
    return create
