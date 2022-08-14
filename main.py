from fastapi import FastAPI, Body, Depends
from pymongo import MongoClient
from app.model import UserSchema
from app.model import UserSchema
from app.model import UserSchema, UserLoginSchema
from app.auth.jwt_handler import signJWT
from app.auth.jwt_beaerer import jwtBearer

#connection mongodb
# client = motor.motor_asyncio.AsyncIOMotorClient('mongodb://localhost:27017')
client = MongoClient('mongodb://localhost:27017')
db = client["manajemen_user"]
users=db.users


app=FastAPI()

# testing fastapi
@app.get('/', tags=["test"])
def test_API():
    return{"hello":"world!"}

#get Users
@app.get("/users", dependencies=[Depends(jwtBearer())], tags=["manajemen"])
def get_users():
    _user=[]
    data_user = users.find()
    for data in data_user:
        _user.append(data)
    return str(_user)

# get id User
@app.get('/users/{username}',dependencies=[Depends(jwtBearer())], tags=["manajemen"])
def get_id_users(username : str):
    try:
        result = users.find_one({'username':username})
        if result:
            return str(result)
        return {"Status" : "Data Tidak Ditemukan!"}
    except Exception as e:
        return {"Status" : "Data Tidak Ditemukan!"}

# add User
@app.post('/users',dependencies=[Depends(jwtBearer())], tags=["manajemen"])
def add_users(user : UserSchema):
    result=users.insert_one(user.dict()).inserted_id
    return {
        "status": "success",
        "data" : user
    }
    
# update User
@app.put('/users', dependencies=[Depends(jwtBearer())], tags=["manajemen"])
def edit_user(user:UserSchema):
    result = users.update_one({'username': user.username}, {'$set':{
        "nama" : user.nama,
        "email" : user.email,
        "phone" : user.phone,
        "address" : user.address,
        "username" : user.username,
        "password" : user.password,
        "status" : user.status,
        "created_time" : user.created_time,
        "updated_time" : user.updated_time,
        "updated_by" : user.updated_by
        }})
    return {
        "status" : "Update Success!",
        "data" : user
    }
    

# delete User
@app.delete('/users/{username}',dependencies=[Depends(jwtBearer())], tags=["manajemen"])
def user_delete(username:str):
    result = users.find_one({'username':username})
    if result:
        users.delete_one({'username':username})
        return {
            "status":"Delete Success!"
        }
    else:
        return {"Status" : "Data Tidak Ditemukan!"}
    
    
# user signup
@app.post('/user/signup', tags=["register&login"])
def user_signup(user : UserSchema =Body(default=None)):
    checkUsername = users.find_one({'username':user.username})
    if not checkUsername:
        result=users.insert_one(user.dict()).inserted_id
        return signJWT(user.id, user.username, user.email, user.phone)
    else:
        return {"Status" : "Username Sudah Terdaftar!"}

# user Login
@app.post('/user/login', tags=["register&login"])
def user_login(user: UserLoginSchema =Body(default=None)):
    checkUserLogin = users.find_one({'username':user.username})
    if (checkUserLogin):
        if user.username==checkUserLogin["username"] and  checkUserLogin["password"]==user.password and checkUserLogin["status"]==True:
            token = signJWT(str(checkUserLogin["_id"]), checkUserLogin["username"], checkUserLogin["email"], checkUserLogin["phone"])
            return {
                "status_code":200,
                "message":"Berhasil Login",
                "access_token": token,
                "data":{
                    "id":str(checkUserLogin["_id"]),
                    "nama":checkUserLogin["nama"]
                }
            }
        elif checkUserLogin["status"] == False:
            return {"status":"akun tidak aktif"}
        else:
            return {"status":"password salah"}
    else:
        return {"status":"user data tidak ditemukan"}





    