from fastapi import FastAPI
from dash_apps.upload_component import app as app_upload

from fastapi.middleware.wsgi import WSGIMiddleware
import uvicorn as uvicorn

from utils.spark_utils import get_local_spark_session, get_spark_conf_as_json, spark
from utils.params import HOST

app = FastAPI()


@app.on_event("startup")
async def startup_event():
    spark = get_local_spark_session(app_name="fastApi Startup")
    return spark


@app.on_event("shutdown")
async def shutdown_event():
    spark.stop()


@app.get("/")
def read_main():
    spark_conf_json=get_spark_conf_as_json(spark)
    return {"lohith says": f"DF is => ${spark_conf_json}"}


app.mount("/upload", WSGIMiddleware(app_upload.server))

if __name__ == '__main__':
    uvicorn.run("main:app", host=HOST, port=8000, reload=True)