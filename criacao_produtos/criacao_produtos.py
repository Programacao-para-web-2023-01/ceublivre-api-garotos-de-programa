from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import mysql.connector

connection = mysql.connector.connect(user="user", database="product_List", password="123456")

app = FastAPI()

class Product(BaseModel):
    id: int | None
    name: str
    description: str
    category: str
    price: float

@app.post('/creat_product')
async def post_prosuct(product: Product):
    cursor = connection.cursor(dictionary=True)
    
    stantment = 'insert into `products` (`product_name`, `product_description`,`product_category`,`product_price`)'\
    'values (%s, %s, %s, %s)'

    values = (product.name, product.description, product.category, product.price)

    cursor.execute(stantment, values)

    product.id = cursor.lastrowid

    connection.commit()

    return product