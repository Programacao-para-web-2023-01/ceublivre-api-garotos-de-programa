from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import mysql.connector

connection = mysql.connector.connect(user='root', database='product_List', password='123456')
app = FastAPI()

class Product(BaseModel):
    id_tabela: int | None
    id_produto: int
    name: str
    description: str
    category: str
    price: float
    image: str
    version: int
    active: int


@app.get("/list_products")
async def list_products(product: Product):
    cursor = connection.cursor(dictionary=True)
    statment = 'select * from `products`'
    
    cursor.execute(statment)

    return cursor.fetchall()

