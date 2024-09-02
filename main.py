from fastapi import Depends, FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.security import OAuth2PasswordRequestForm
from fastapi_keycloak import FastAPIKeycloak, OIDCUser
from starlette.responses import RedirectResponse

from auth import create_access_token, get_current_user
from config import APP_NAME, VERSION
from files import router as files
from model import User, users_db



app = FastAPI(
    title=APP_NAME,
    version=VERSION
)


app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
    allow_credentials=True
)

# ---- Do this for all of your routes ----
app.include_router(files)
# ----------------------------------------

# Redirect / -> Swagger-UI documentation
@app.get("/")
def main_function():
    """
    # Redirect
    to documentation (`/docs/`).
    """
    return RedirectResponse(url="/docs/")


@app.post("/token")
async def login_for_access_token(form_data: OAuth2PasswordRequestForm = Depends()):
    user = users_db.get(form_data.username)
    print(user)
    if user is None or user.password != form_data.password:
        raise HTTPException(status_code=400, detail="Incorrect username or password")
    access_token = create_access_token(data={"sub": user.username})
    return {"access_token": access_token, "token_type": "bearer"}

@app.get("/protected")
async def protected_route(username: str = Depends(get_current_user)):
    return {"message": f"Hello, {username}! This is a protected resource."}

@app.get("/create_user")
async def protected_route(username: str, password: str):
    users_db[username] = User(username=username, password=password)
    return {"message": f"Hello, {username}! This is a create resource."}