from fastapi import FastAPI, HTTPException, UploadFile
from fastapi.responses import Response
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from deta import Deta



app = FastAPI()

#configurando os links que podem consultar a api:
origins = [
    "http://localhost:3000"
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["GET", "POST", "PUT", "DELETE"],
    allow_headers=["*"],
)

deta = Deta("e0h2cutqoow_Qgi1mF4jpgxHGhDsS3mNj8MWttvPwiUa")
db = deta.Base("Products") #Base de produtos(ativos)
drive = deta.Drive("Images") # Drive de Imagens (ativos)
dbInactive = deta.Base("ProductDatabase")# Base de produtos(Inativos)
dbCat = deta.Base("Categories")

class BaseProduct(BaseModel):
    name: str
    description: str
    category: str
    price: float
    image: str
    weight: float

class Product(BaseModel):
    key: str 
    first_key: str
    name: str
    description: str
    category: str
    price: float
    image: str
    version: int
    active: int
    weight: float

class Category(BaseModel):
    key:str
    name: str

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
@app.patch('/product/image/{prod_key}')
async def insert_image(prod_key: str, file: UploadFile):
    if not file:
      raise HTTPException(status_code=400, detail="File not sent")
    else:
        if (file.content_type == 'image/jpg') | (file.content_type == 'image/jpeg'):
            filename = file.filename
            f = drive.put(filename, file.file)
            if f != filename:
                return {"message": "upload failed"}
            else:
                db.update({"image": filename}, prod_key)
                return {"filename": filename, "product_key":prod_key}
        else: 
            raise HTTPException(status_code=400, detail="Only files in jpg or jpeg format are accepted")

### Consulta de Imagens
@app.get('/product/image/{prod_key}')
async def get_image(prod_key: str):
    product = db.get(prod_key)
    if product:
        response = drive.get(product['image'])
        image = response.read()
        return Response(content=image, media_type='image/jpeg')
    raise HTTPException(status_code=404, detail="product not found")


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
    
    enabled = db.update({"active":1, "__expires": db.util.trim()}, key)
    dbInactive.delete(key)

    if enabled == None:
        return "Product enabled"

### Deleta produto do banco de inativos
@app.delete("/product/{key}")
async def delete_product(key:str):
    dbInactive.delete(key)
    return "Product deleted"

# Create category
@app.post("/category")
async def create_category(category: Category):
    inserted = dbCat.put(category.dict(exclude={'key'}))
    
    return inserted

## Update category
@app.put("/category/{key}")
async def update_category(category: Category, key: str):
    
    if category.key != key:
        raise HTTPException(status_code=400, detail="Body ID does not match PATH ID")

    updated = dbCat.update(category.dict(exclude={'key'}), key)
    if updated != None:
        raise HTTPException(status_code=404, detail="Product not found")
    return category


### Delete category
@app.delete("/category/{key}")
async def delete_category(key:str):
    
    res = db.fetch({"category": key})
    all_items = res.items
    # fetch until last is 'None'
    while res.last:
        res = db.fetch(last=res.last)
        all_items += res.items

    for item in all_items:
        db.update({"category": db.util.trim()}, item["key"])
        
    dbCat.delete(key)
    return "Category deleted"


### função patch Insert category p/ produtos
@app.patch("/product/category/{key}")
async def insert_category(cat_key:str, key:str):
    
    category = dbCat.get(cat_key)
    if category == None:
        raise HTTPException(status_code=404, detail="Category not found")
    updated = db.update({"category":cat_key}, key)

    if updated == None:
        return "Category inserted"

### Remove category
@app.patch("/product/category/remove/{key}")
async def remove_category( key:str):
    db.update({"category": db.util.trim()}, key)
    return "category removed"

### Lista todas as categorias
@app.get("/category")
async def list_categories():
    res = dbCat.fetch()
    all_items = res.items
# fetch until last is 'None'
    while res.last:
        res = dbCat.fetch(last=res.last)
        all_items += res.items
    return all_items

### Busca categoria por Key
@app.get("/category/{key}")
async def get_category_by_id(key: str):
    category = dbCat.get(key)
    if category:
        return category
    raise HTTPException(status_code=404, detail="category not found")
