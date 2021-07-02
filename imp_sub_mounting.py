
from typing import List, Optional
import databases
import sqlalchemy
from fastapi import FastAPI, status, Cookie, Response
from fastapi.middleware.cors import CORSMiddleware
from fastapi.middleware.wsgi import WSGIMiddleware
from pydantic import BaseModel
from imp_create_spark import app as app_login
import uvicorn
import uuid


# Defining the Session Id
session_id = str(uuid.uuid4())


# https://www.tutlinks.com/fastapi-with-postgresql-crud-async/


# Create database instance
DATABASE_URL = "sqlite:///./test.db"
database = databases.Database(DATABASE_URL)
metadata = sqlalchemy.MetaData()


# Create SQL Alchemy model/Table
metadata = sqlalchemy.MetaData()

notes = sqlalchemy.Table(
    "notes",
    metadata,
    sqlalchemy.Column("id", sqlalchemy.Integer, primary_key=True),
    sqlalchemy.Column("text", sqlalchemy.String),
    sqlalchemy.Column("completed", sqlalchemy.Boolean),
)

# Create Engine
engine = sqlalchemy.create_engine(
    DATABASE_URL, connect_args={"check_same_thread": False}
)
metadata.create_all(engine)


# Create Models using Pydantic
class NoteIn(BaseModel):
    text: str
    completed: bool

class Note(BaseModel):
    id: int
    text: str
    completed: bool


app = FastAPI(title="REST API using FastAPI PostgreSQL Async EndPoints")
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"]
)
#
# allow_origins=['client-facing-example-app.com', 'localhost:5000']

# Application Startup & Shutdown Events
@app.on_event("startup")
async def startup():
    await database.connect()


@app.on_event("shutdown")
async def shutdown():
    await database.disconnect()

@app.get("/")
async def root():
    return {"message": "Hello World"}


@app.get("/notes/", response_model=List[Note], status_code = status.HTTP_200_OK)
async def read_notes(skip: int = 0, take: int = 20):
    query = notes.select().offset(skip).limit(take)
    return await database.fetch_all(query)


@app.get("/notes/{note_id}/", response_model=Note, status_code = status.HTTP_200_OK)
async def read_notes(note_id: int):
    query = notes.select().where(notes.c.id == note_id)
    return await database.fetch_one(query)


@app.post("/notes/", response_model=Note, status_code = status.HTTP_201_CREATED)
async def create_note(note: NoteIn):
    query = notes.insert().values(text=note.text, completed=note.completed)
    last_record_id = await database.execute(query)
    return {**note.dict(), "id": last_record_id}


@app.post("/multiple-notes/", status_code = status.HTTP_201_CREATED)
async def create_note(note: List[NoteIn]):
    for x in note:
        query = notes.insert().values(text=x.text, completed=x.completed)
        await database.execute(query)
    return {"id": "insert successful"}


@app.put("/notes/{note_id}/", response_model=Note, status_code = status.HTTP_200_OK)
async def update_note(note_id: int, payload: NoteIn):
    query = notes.update().where(notes.c.id == note_id).values(text=payload.text, completed=payload.completed)
    await database.execute(query)
    return {**payload.dict(), "id": note_id}


@app.delete("/notes/{note_id}/", status_code = status.HTTP_200_OK)
async def delete_note(note_id: int):
    query = notes.delete().where(notes.c.id == note_id)
    await database.execute(query)
    return {"message": "Note with id: {} deleted successfully!".format(note_id)}

''' Working with cookies
'''
@app.get("/get-cookie/")
async def read_items(racf: Optional[str] = Cookie(None)):
    return {"racf": racf}


# @app.post("/set-cookie/{racf}")
# def create_cookie(racf: str, response: Response):
#     response.set_cookie(key="racf", value=racf, httponly=True)
#     return {"message": f"racf set to {racf}"}


@app.get("/set-cookie-get/{racf}")
def create_cookie_get(racf: str, response: Response):
    response.set_cookie(key="racf", value=racf, httponly=True)
    return {"message": f"racf set to {racf}, from a get request"}

''' Mounting App
'''
app.mount("/login/", WSGIMiddleware(app_login.server))

if __name__ == "__main__":
    uvicorn.run("imp_sub_mounting:app", host="11.15.93.81", port=8000, reload=True)