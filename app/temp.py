from fastapi import FastAPI, Depends, HTTPException, status
from fastapi.responses import JSONResponse
from pydantic import BaseModel
import pandas as pd
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
import jwt
import datetime

# instantiating the application
app = FastAPI()


# defining endpoint to authenticate token
oauth2_scheme = OAuth2PasswordBearer(tokenUrl='token')


# defining a secret key to generate JWT
JWT_SECRET = 'mysecretJWTkey2'


# defining a demo user_details dict, in real-time scenarios this will be replaced by user-table from database
user_details = {
    "id":1,
    "username":"harshpreets",
    "password":"mysecretkey"
}

df = pd.read_csv('data/collegeData.csv')

class getDetails(BaseModel):
    city: str

class getUserdetails(BaseModel):
    username: str
    password: str


# to authenticate if the user is present in the db
async def authenticate_user(username: str, password: str):
    if not user_details.get("username")  == username:
        return False
    if not user_details.get("password") == password:
        return False
    return user_details

# endpoint to generate token using username and password after authentication
@app.post('/token')
async def generate_token(form_data: OAuth2PasswordRequestForm = Depends()):
    user = await authenticate_user(form_data.username, form_data.password)

    if not user:
        return HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, 
            detail='Invalid username or password'
        )

    token = jwt.encode(user_details,JWT_SECRET)

    return {"access_token":token, "token_type":"bearer"}


# endpoint to get the token using username
@app.get('/getToken/')
async def getToken(token: str = Depends(oauth2_scheme)):
    return JSONResponse(
        status_code=200,
        content={
            "username":user_details.get("username"),
            "usertoken":token
        }
    )


# to authenticate the bearer token
async def get_current_user(token: str = Depends(oauth2_scheme)):
    try:
        payload = jwt.decode(token, JWT_SECRET, algorithms=['HS256'])
        
        # user = await user_details.get(id=payload.get('id'))
        if payload.get('id')==1:  # registered user
            user = user_details
        else:
            raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, 
            detail='Invalid Bearer Token'
        )
    except:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, 
            detail='Invalid Bearer Token'
        )
        
    return user
   

# endpoint to test the authenticated api
@app.post('/collegeSearch/')
def getResults(infodict: getDetails, token: str = Depends(get_current_user)):
    results = df[df['city'] == infodict.city]
    listOfCollegeNames = results['fullName'].to_list()

    return JSONResponse(
        status_code=200,
        content= {
            "city":infodict.city,
            "data": listOfCollegeNames
        }
    )