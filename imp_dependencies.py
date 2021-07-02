
from fastapi import FastAPI, Depends
import uvicorn
from pyspark.sql import SparkSession

app = FastAPI(title="trying dependencies")


async def str_len(input: str, offset: int) -> int:
    return len(input)+offset


@app.get("/{racf}")
async def say_hello(racf: str, this_can_be_anything: SparkSession = Depends(str_len)):
    return {"msg", this_can_be_anything}


if __name__ == "__main__":
    uvicorn.run("imp_dependencies:app", host="11.15.93.81", port=8000, reload=True)