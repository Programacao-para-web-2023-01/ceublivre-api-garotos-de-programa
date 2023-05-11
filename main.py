from typing import Annotated, Union
from fastapi import FastAPI, HTTPException, File, UploadFile
from pydantic import BaseModel
from deta import Deta


app = FastAPI()

deta = Deta("e0h2cutqoow_Qgi1mF4jpgxHGhDsS3mNj8MWttvPwiUa")
db = deta.Base("Products") #Base de produtos(ativos)
drive = deta.Drive("Images") # Drive de Imagens (ativos)
dbInactive = deta.Base("ProductDatabase")# Base de produtos(Inativos)

class BaseProduct(BaseModel):
    name: str
    description: str
    category: str
    price: float
    image: str
    weight: float

class Product(BaseModel):
    key: str | None
    first_key: str| None
    name: str
    description: str
    category: str
    price: float
    image: str
    version: int
    active: int
    weight: float

### Todos produtos cadastrados, busca no banco de produtos ativos e não-ativos
@app.get("/product")
async def list_products():
    res = db.fetch()
    all_items = res.items
# fetch until last is 'None'
    while res.last:
        res = db.fetch(last=res.last)
        all_items += res.items

    res = dbInactive.fetch()
    all_items += res.items
# fetch until last is 'None'
    while res.last:
        res = db.fetch(last=res.last)
        all_items += res.items
    return all_items

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
    product = db.get(key)
    if product:
        return product
    raise HTTPException(status_code=404, detail="product not found")

### Novo produto
@app.post('/product')
async def post_product(baseproduct: BaseProduct):
    
    product: Product
    product = baseproduct
    product.active = 1
    product.version = 1

    inserted = db.put(product.dict)
    product.key = inserted.key
    product.first_key = inserted.key
    inserted = db.update(product.dict, product.key)
    
    return inserted

### Inserção de Imagens
### ****Ainda necessário integrar o JSON do registro de produto****
@app.put('/product')
async def insert_image(file: Union[UploadFile, None] = None):
    if not file:
      return {"message": "No upload file sent"}
    else:
        f = drive.put(file.filename, file.file)
        if f != file.filename:
            return {"message": "upload failed"}
        else:
            return {"filename": file.filename}


### Alterar produto 
@app.put("/product/{key}")
async def update_product(product: Product, key: str):
    
    if product.key != key:
        raise HTTPException(status_code=400, detail="Body ID does not match PATH ID")

    updated = db.update(product.dict(exclude={'key'}), key)
    if updated != None:
        raise HTTPException(status_code=404, detail="Product not found")
    return product

### Desabilitar produto
@app.patch("/product/disable/{key}")
async def disable_product(key: str):
    
    product = db.get(key)
    if product == None:
        raise HTTPException(status_code=404, detail="Product not found in the active products list")
    dbInactive.put(product,expire_in=10368000) ## Expira em 120 dias
    disabled = dbInactive.update({"active":0}, key)
    db.delete(key)

    if disabled == None:
        return "Product disabled"


### Habilitar produto
@app.patch("/product/enable/{key}")
async def enable_product(key: str):
    
    product = dbInactive.get(key)
    if product == None:
        raise HTTPException(status_code=404, detail="Product not found in the inactive products list")
    db.put(product)
    
    enabled = db.update({"active":1}, key, expire_in= 600)
    #db.update({"__expires":None},key)
    dbInactive.delete(key)

    if enabled == None:
        return "Product enabled"

### Deleta produto do banco de inativos
@app.delete("/product/{key}")
async def delete_product(key:str):
    dbInactive.delete(key)
    return "Product deleted"