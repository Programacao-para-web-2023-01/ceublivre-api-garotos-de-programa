from typing import Annotated, Union
from fastapi import FastAPI, HTTPException, File, UploadFile
from pydantic import BaseModel
from deta import Deta

deta = Deta("e0h2cutqoow_Qgi1mF4jpgxHGhDsS3mNj8MWttvPwiUa")

app = FastAPI()

db = deta.Base("Products")
drive = deta.Drive("Images")

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


## Ainda necessário integrar o JSON do registro de produto
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