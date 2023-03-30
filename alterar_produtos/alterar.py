from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import mysql.connector

connection = mysql.connector.connect(user="root", database="product_List", password = "123456")
app = FastAPI()

class Product(BaseModel):
    id: int | None
    name: str
    description: str
    category: str
    price: float
    image: str
    version: int
    active: int

@app.put("/product/{id}")
async def update_product(id: int, product: Product):
    cursor = connection.cursor(dictionary=True)
    statement = "UPDATE `products` SET product_name = %s, product_description = %s, product_category = %s, product_price = %s , product_image = %s, product_version = %s, product_active = %s"\
                    "WHERE product_id = %s"

    value = (product.name, product.description, product.category, product.price, product.image, product.version, product.active, product.id)

    cursor.execute(statement, value)
    connection.commit()

    if cursor.rowcount == 0:
        raise HTTPException(status_code=404, detail="Product not found")

    return product