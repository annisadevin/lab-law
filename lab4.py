from datetime import date
from tokenize import Number 
from pydantic import BaseModel
from fastapi import FastAPI, HTTPException, UploadFile, File
from datetime import date
import os
import aiofiles as aiofiles

app = FastAPI()

try:
   os.makedirs("files")
except:
   pass

moneyExpense = {}
class MoneyExpense(BaseModel):
    id:int
    datetime: date
    category: str
    title: str
    expense: int

@app.get("/expense/{id}/")
def getExpense(id:int):
    try:
      expense = moneyExpense[id]
      return expense
    except:
      raise HTTPException(status_code=400, detail= "Tidak ada pengeluaran dengan id " + str(id))

@app.post("/expense/")
def postExpense(expense: MoneyExpense):
    if expense.id not in moneyExpense : 
        newExpense = MoneyExpense(id=expense.id, datetime=expense.datetime, category=expense.category, title=expense.title, expense=expense.expense)
        moneyExpense[expense.id] = newExpense
        return newExpense
    else :
        raise HTTPException(status_code=400, detail= "Pengeluaran dengan id " + str(expense.id) + " sudah ada")

@app.delete("/expense/{id}/")
def deleteExpense(id:int):
    try : 
        deletedExpense = moneyExpense[id]
        moneyExpense.pop(id)
        return {"message" : "Successfully deleted expense"}
    except :
        raise HTTPException(status_code=400, detail= "Pengeluaran dengan id " + str(id) + " tidak ada")

@app.put("/expense/")
def putExpense(expense: MoneyExpense):
    try : 
        updatedExpense = moneyExpense[expense.id]
        updatedExpense.datetime = expense.datetime
        updatedExpense.category = expense.category
        updatedExpense.title = expense.title
        updatedExpense.expense = expense.expense
        return updatedExpense
    except :
        raise HTTPException(status_code=400, detail= "Pengeluaran dengan id " + str(expense.id) + " tidak ada")

@app.post("/expense/uploadfiles/")
async def uploadFiles(file: UploadFile = File(...)):
    async with aiofiles.open(f"files/{file.filename}", 'wb') as fileout:
        content = await file.read()
        await fileout.write(content)
    return {"message" : "Successfully added file " + str(file.filename)}