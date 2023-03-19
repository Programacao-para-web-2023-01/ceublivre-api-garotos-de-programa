from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import mysql.connector

connection = mysql.connector.connect(user="user", database="catalago_produtos")

app = FastAPI()


