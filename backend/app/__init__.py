from fastapi import FastAPI
from .database.models import User, Item
from fastapi.middleware.cors import CORSMiddleware
from .database import create_db_and_tables
from fastapi.security import OAuth2PasswordBearer
from .core.security import oauth2_scheme
from .routes import auth, items, users, files
from dotenv import load_dotenv
load_dotenv()
app = FastAPI()

origins = [
    "http://localhost",
    "http://localhost:8080",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.on_event("startup")
def on_startup():
    create_db_and_tables()


app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173", "http://localhost:8080"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.on_event("startup")
def on_startup():
    create_db_and_tables()


@app.get("/")
async def root():
    return {"message": "Hello World"}



app.include_router(auth.router)
app.include_router(files.router)
app.include_router(items.router)
app.include_router(users.router)



