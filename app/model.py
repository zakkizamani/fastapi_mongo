from datetime import date, datetime
from pydantic import BaseModel, Field, EmailStr


class UserSchema(BaseModel):
    id: int = Field(default=None)
    nama : str = Field(default=None)
    email : str = Field(default=None)
    phone : str = Field(default=None)
    address : str = Field(default=None)
    username : str = Field(default=None)
    password : str = Field(default=None)
    status : bool = Field(default=False)
    created_time : datetime = Field(default=None)
    updated_time : datetime = Field(default=None)
    updated_by:str = Field(default=None)
    
    class config:
        schema_extra = {
            "user-demo":{
                "name" : "nama",
                "email" : "email@sample.com",
                "phone" : "08123456789",
                "address" : "string",
                "username" : "string unique",
                "password" : "string",
                "status" : "bool",
                "created_time" : "date",
                "updated_time" : "date",
                "updated_by" : "string"
            }
        }
        
# class UserRegisterSchema(BaseModel):
#     username : str = Field(default=None)
#     email : str = Field(default=None)
#     password : str = Field(default=None)
#     class Config:
#         schema_extra={
#             "user register":{
#                 "username":"jhon_doe",
#                 "email" : "email@example.mail",
#                 "password" : "12345678"
#             }
#         }
    
class UserLoginSchema(BaseModel):
    username : str = Field(default=None)
    password : str = Field(default=None)
    class Config:
        schema_extra={
            "user register":{
                "username":"jhon_doe",
                "password" : "12345678"
            }
        }