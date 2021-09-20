from fastapi import FastAPI
from fastapi.middleware.wsgi import WSGIMiddleware
import uvicorn as uvicorn

from utils.spark_utils import get_local_spark_session, get_spark_conf_as_json, spark
from utils.params import HOST

from dash_apps.upload_component import app as app_upload
from dash_apps.upload_component_withGraph import app as app_new_upload
from dash_apps.example1 import app as app_eg1
from dash_apps.example2 import app as app_eg2


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
app.mount("/new_upload/", WSGIMiddleware(app_new_upload.server))
app.mount("/eg1", WSGIMiddleware(app_eg1.server))
app.mount("/eg2", WSGIMiddleware(app_eg2.server))

if __name__ == '__main__':
    uvicorn.run("main:app", host=HOST, port=8000, reload=True)