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

### Todos produtos cadastrados        
        
@app.get("/product")
async def list_products():
    res = db.fetch()
    all_items = res.items

# fetch until last is 'None'
    while res.last:
        res = db.fetch(last=res.last)
        all_items += res.items

    return res.items

### Produtos ativos


@app.get("/product/active")
async def get_active_products():
    res = db.fetch({"active": 1})
    all_items = res.items

    # fetch until last is 'None'
    while res.last:
        res = db.fetch(last=res.last)
        all_items += res.items

    return all_items


### Produto por key


@app.get("/product/{key}")
async def get_products_by_id(key: str):
    product = db.get(id)
    if product:
        return product

    raise HTTPException(status_code=404, detail="product not found")
    
    
