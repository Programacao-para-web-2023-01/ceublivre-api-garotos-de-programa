from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from deta import Deta

deta = Deta("e0h2cutqoow_Qgi1mF4jpgxHGhDsS3mNj8MWttvPwiUa")

app = FastAPI()

db = deta.Base('Products')

db_prod_outdated = deta.Base('ProductDatabase')

class BaseProduct(BaseModel):
    name: str
    description: str
    price: float
    image: str
    weight: float

class Product(BaseModel):
    key: str | None
    first_key: str | None
    name: str
    description: str
    price: float
    image: str
    version: int
    active: int
    weight: float

@app.post('/outdated_Products')
async def outdated_products(product: Product, first_key: str):
    create = db_prod_outdated.insert(product.dict(exclude={'key'}))

    return create

@app.put('/update_product/{key}')
async def constrol_update_product(product: Product, key: str, first_key: str): 
    update = db.update(product.dict(exclude={'key'}), key)

    if  update != None:
        raise HTTPException(status_code=404, detail="Product not found")
    
    outdated_products(product, first_key)
    return product

@app.post("/creat_product_version/{first_key}")#usa a first key do produto que sera alterado
async def product_variation(first_key: str, value: str):#o element_changed é o elemento que será alterado.o value e o valor novo valor do campo alterado, estes valores serao envidos pelo front-end
    
    new_variation: Product
    new_variation = get_products_by_first_key(first_key)

    new_variation.name = value

    inserted = db.put(new_variation.dict)
    new_variation.key = inserted.key
    inserted = db.update(new_variation.dict, new_variation.key) 
#     resolver o erro: new_variation.name = value
#                      AttributeError: 'coroutine' object has no attribute 'name'

    return inserted

async def get_products_by_first_key(first_key: str):
    product = db.get(first_key)
    if product:
        return product
    else: 
        return print("product not found")