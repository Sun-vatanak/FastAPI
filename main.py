from fastapi import FastAPI,Path,Query,HTTPException
from typing import Optional
from pydantic import BaseModel
app = FastAPI()


@app.get("/")
def home():
    return {"message": "Hello, World!"}
@app.get("/about")

def about():
    return {"message": "This is the about page"}
class Item(BaseModel):
     name: str
     price: float
     age:int
     mes:Optional[str]=None
class UpdateItem(BaseModel):
     name:Optional[str]=None
     price:Optional[float]=None
     age:Optional[int]=None
     mes:Optional[str]=None
data={
    "1":Item(name="item1",price=10.5,age=20),
}

@app.get("/users-get-by-all")
def read_user():
    return data
# get by id
@app.get("/users-get-by-item/{user_id}")
def read_user(user_id: int=Path(description="the is of the item ")):
    return data[user_id]
# get by name 
@app.get("/users-get-by-name/{user_id}")
def read_user(* ,user_id:int, test:int ,name: Optional[str]=None):
    # loop data 
    for item_id in data:
        if data[item_id]["name"] == name:
            return data[item_id]
        raise HTTPException(status_code=400,detail="get data not found")
# Crate 
@app.get("/users-get-by-name/")
def get_user_by_name(name: str = Query(..., description="Name to search for")):
    for user_id, item in data.items():
        if item.name == name:
            return item
    raise HTTPException(status_code=404, detail="User not found")
@app.post("/users-create/{user_id}")
def create_user(user_id:int,item:Item):
    if user_id in data:
        return {"message": "User already exists"}
    # carte data 
    data[user_id]=item
# {'name':item.name,'price':item.price,'age':item.age,'mse':item.mes}
    return {"message": "User created successfully", "user": data[user_id]}
# update 
@app.put("/users-update/{user_id}")
def update_user(user_id: int, item:UpdateItem):
    if user_id not in data:
        raise HTTPException(status_code=404, detail="User update not found")
    # update data
    # data[user_id] = item
    if item.name !=None:
        data[user_id].name=item.name
    if item.price !=None:
        data[user_id].price=item.price
    if item.age !=None:
        data[user_id].age=item.age
    if item.mes !=None:
        data[user_id].mes=item.mes

    return {"message": "User updated successfully", "user": data[user_id]}
#  delect 
@app.delete("/user-delete")
def delete_user(user_id: int=Query(...,description="input your id you wnat delete ")):
    if user_id not in data:
        raise HTTPException(status_code=404, detail="User delete not found")
    # delete data
    del data[user_id]
    return {"message": "User deleted successfully"}
