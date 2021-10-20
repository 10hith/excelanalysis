from fastapi import FastAPI
from fastapi.middleware.wsgi import WSGIMiddleware
import uvicorn as uvicorn

from utils.spark_utils import get_local_spark_session, get_spark_conf_as_json, spark
from utils.params import HOST

from dash_apps.upload_component_withGraph import app as app_new_upload
from dash_apps.profile_app import app as profile_app
# from dash_apps.profile_wix_app import app as profile_wix_app
from dash_apps.example1 import app as app_eg1


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


app.mount("/profile", WSGIMiddleware(profile_app.server))
# app.mount("/wix", WSGIMiddleware(profile_wix_app.server))
app.mount("/new_upload/", WSGIMiddleware(app_new_upload.server))
app.mount("/eg1", WSGIMiddleware(app_eg1.server))

if __name__ == '__main__':
    uvicorn.run("main:app", host=HOST, port=8000, reload=True)