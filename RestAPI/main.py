import redis.asyncio as redis
from fastapi import FastAPI, Depends, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi_limiter import FastAPILimiter
from sqlalchemy import text
from sqlalchemy.ext.asyncio import AsyncSession

from src.database.db import get_db
from src.routes import contacts, auth, users
from src.conf.config import config

app = FastAPI()

origins = ["*"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
# app.mount('/static', StaticFiles(directory='../src/static'), name='static')
app.mount('/static', StaticFiles(directory='src/static'), name='static')

app.include_router(auth.router, prefix='/api')
app.include_router(users.router, prefix='/api')
app.include_router(contacts.router, prefix='/api')


@app.on_event("startup")
async def startup():
    """
    The startup function is called when the application starts up.
    
    :return: A fastapilimiter object
    """
    r = await redis.Redis(host=config.REDIS_DOMAIN, port=config.REDIS_PORT, db=0, password=config.REDIS_PASSWORD)
    await FastAPILimiter.init(r)


@app.get("/")
def index():
    """
    The index function is a simple function that returns the string &quot;Contact book&quot;
        as a JSON object. This is to show that the API works and can return data.
    
    :return: A dictionary with a key &quot;message&quot; and value &quot;contact book&quot;
    """
    return {"message": "Contact book"}


@app.get("/api/healthchecker")
async def healthchecker(db: AsyncSession = Depends(get_db)):
    """
    The healthchecker function is a simple function that checks if the database connection is working.
    It does this by executing a simple SQL query and checking if it returns any results.
    If there are no results, then the database connection has failed.
    
    :param db: AsyncSession: Inject the database session into the function
    :return: A dictionary with a message
    """
    try:
        result = await db.execute(text("SELECT 1"))
        result = result.fetchone()
        if result is None:
            raise HTTPException(status_code=500, detail="Database is not configured correctly")
        return {"message": "Welcome to FastAPI!"}
    except Exception as e:
        print(e)
        raise HTTPException(status_code=500, detail="Error connecting to the database")
