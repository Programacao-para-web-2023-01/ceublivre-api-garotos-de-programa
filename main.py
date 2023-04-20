from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import mysql.connector
from dotenv import load_dotenv
load_dotenv()
import os
import MySQLdb

connection = MySQLdb.connect(
  host= os.getenv("HOST"),
  user=os.getenv("USERNAME"),
  passwd= os.getenv("PASSWORD"),
  db= os.getenv("DATABASE"),
  ssl_mode = "VERIFY_IDENTITY",
  ssl      = {
    "ca": "./etc/ssl/ca.pem"
  }
  
)

##connection = mysql.connector.connect(user="root", database="classroom", password = "123456")
app = FastAPI()

"""
class Product(BaseModel):
    id: int | None
    name: str
    description: str
    category: str
    price: float
"""
@app.get("/products")
async def list_products():
    return "Hello World"

"""
@app.put("/product/{id}")
async def update_product(id: int, product: Product):
    cursor = connection.cursor(dictionary=True)
    statement = "UPDATE `products` SET product_name = %s, product_description = %s, product_category = %s, product_price = %s "\
                    "WHERE product_id = %s"

    value = (product.name, product.description, product.category, product.price, product.id)

    cursor.execute(statement, value)
    connection.commit()

    if cursor.rowcount == 0:
        raise HTTPException(status_code=404, detail="Product not found")

    return product
"""