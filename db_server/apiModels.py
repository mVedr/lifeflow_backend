from datetime import date

from pydantic import BaseModel


class UserProfile(BaseModel):
    name: str
    dob: date
    email: str
    phone_number: str
    blood_group: str
    sex: str
    profile_url: str
    location: str

class UserRegisterWithEmail(BaseModel):
    email: str

class UserRegisterWithEmailCords(BaseModel):
    email: str
    lat: str
    lon: str

class EntityRegister(BaseModel):
    primary_email: str
    primary_ph_no: str
    reg_number: str
    name: str

class EntityProfile(BaseModel):
    name :str
    location :str
    photo_url :str
    website_url :str
    primary_ph_no :str
    secondary_ph_no :str
    primary_email :str
    secondary_email :str

class VolumeSetRequest(BaseModel):
    email :str
    vol :int
    