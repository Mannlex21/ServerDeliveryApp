from fastapi import FastAPI
import sqlite3

app = FastAPI()

@app.get('/get')
async def get():
    conn = sqlite3.connect("database.db")
    cur = conn.execute("select*from prueba")
    prueba = cur.fetchall()
    result_prueba = []
    print(prueba)
    for i in prueba:
        single_prueba = {}
        single_prueba["id"] = i[0]
        result_prueba.append(single_prueba)
    return result_prueba
