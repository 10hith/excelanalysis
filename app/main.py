from fastapi import FastAPI
import dash_labs as dl
import pandas as pd
import dash
import dash_core_components as dcc
import dash_bootstrap_components as dbc
import plotly.express as px
from dash_apps.upload_component import app as app_upload
from fastapi.middleware.wsgi import WSGIMiddleware

from utils.spark_utils import get_local_spark_session, get_spark_conf_as_json

app = FastAPI()

spark = get_local_spark_session(app_name="default session")


@app.on_event("startup")
async def startup_event():
    spark = get_local_spark_session(app_name="fastApi Startup")
    return spark


@app.on_event("shutdown")
def shutdown_event():
    spark.stop()


@app.get("/")
def read_main():
    spark_conf_json=get_spark_conf_as_json(spark)
    return {"lohith says": f"DF is => ${spark_conf_json}"}


app.mount("/upload", WSGIMiddleware(app_upload.server))