from typing import Annotated, Union
from fastapi import FastAPI, HTTPException, File, UploadFile
from pydantic import BaseModel
from deta import Deta


app = FastAPI()

deta = Deta("e0h2cutqoow_Qgi1mF4jpgxHGhDsS3mNj8MWttvPwiUa")
db = deta.Base("Products") #Base de produtos(ativos)
db_prod_outdated = deta.Base("ProductDatabase") #Base de produtos(versões anteriores)
drive = deta.Drive("Images") # Drive de Imagens (ativos)

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

### Novo produto
@app.post('/product')
async def post_product(product: Product):
    
    inserted = db.insert(product.dict(exclude={'key'}))
    return inserted

### Inserção de Imagens
### Ainda necessário integrar o JSON do registro de produto
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
    
    updated = db.update(product.dict(exclude={'key'}), key)
    if updated != None:
        raise HTTPException(status_code=404, detail="Product not found")
    return product
