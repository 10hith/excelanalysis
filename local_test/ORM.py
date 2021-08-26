from typing import List
import databases
import sqlalchemy
from fastapi import FastAPI, status
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import uvicorn

DATABASE_URL = "postgresql://postgres:example123@localhost:5432/postgres"

database = databases.Database(DATABASE_URL)

# Create SQL Alchemy model/Table
metadata = sqlalchemy.MetaData()

distribution = sqlalchemy.Table(
    "distribution",
    metadata,
    sqlalchemy.Column("column_name", sqlalchemy.String),
    sqlalchemy.Column("cat_value", sqlalchemy.String),
    sqlalchemy.Column("count", sqlalchemy.Float),
    sqlalchemy.Column("ratio", sqlalchemy.Float),
)

# Create Engine
engine = sqlalchemy.create_engine(
    DATABASE_URL
)
metadata.create_all(engine)


# Create Models using Pydantic
class Distribution(BaseModel):
    column_name: str
    cat_value: str
    count: float
    ratio: float


# Add CORS to FastAPI
# Remove this while integrating with main
app = FastAPI(title="REST API using FastAPI PostgreSQL Async EndPoints")
# Application Startup & Shutdown Events
@app.on_event("startup")
async def startup():
    await database.connect()


@app.on_event("shutdown")
async def shutdown():
    await database.disconnect()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"]
)
# allow_origins=['client-facing-example-app.com', 'localhost:5000']


@app.post("/htgrm/")
async def insert_histogram(v_distribution: List[Distribution]):
    for x in v_distribution:
        query = distribution.insert().values(
            column_name=x.column_name,
            cat_value=x.cat_value,
            count=x.count,
            ratio=x.ratio
        )
        await database.execute(query)
    return {"id": "insert successful"}


@app.get("/htgrm/", response_model=List[Distribution])
async def get_histogram():
    query = distribution.select()
    return await database.fetch_all(query)

if __name__ == "__main__":
    uvicorn.run("ORM:app", port=8000, reload=True)

'''
@app.get("/notes/", response_model=List[Note], status_code=status.HTTP_200_OK)
async def read_notes(skip: int = 0, take: int = 20):
    query = notes.select().offset(skip).limit(take)
    return await database.fetch_all(query)


@app.get("/notes/{note_id}/", response_model=Note, status_code=status.HTTP_200_OK)
async def read_notes(note_id: int):
    query = notes.select().where(notes.c.id == note_id)
    return await database.fetch_one(query)


@app.post("/notes/", response_model=Note, status_code=status.HTTP_201_CREATED)
async def create_note(note: NoteIn):
    query = notes.insert().values(text=note.text, completed=note.completed)
    last_record_id = await database.execute(query)
    return {**note.dict(), "id": last_record_id}


@app.post("/multiple-notes/", status_code=status.HTTP_201_CREATED)
async def create_note(note: List[NoteIn]):
    for x in note:
        query = notes.insert().values(text=x.text, completed=x.completed)
        await database.execute(query)
    return {"id": "insert successful"}


@app.put("/notes/{note_id}/", response_model=Note, status_code=status.HTTP_200_OK)
async def update_note(note_id: int, payload: NoteIn):
    query = notes.update().where(notes.c.id == note_id).values(text=payload.text, completed=payload.completed)
    await database.execute(query)
    return {**payload.dict(), "id": note_id}


@app.delete("/notes/{note_id}/", status_code=status.HTTP_200_OK)
async def delete_note(note_id: int):
    query = notes.delete().where(notes.c.id == note_id)
    await database.execute(query)
    return {"message": "Note with id: {} deleted successfully!".format(note_id)}
'''
