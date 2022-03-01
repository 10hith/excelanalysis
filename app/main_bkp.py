from fastapi import FastAPI
import uvicorn as uvicorn
from utils.params import HOST

from fastapi.middleware.wsgi import WSGIMiddleware
from utils.spark_utils import get_local_spark_session, get_spark_conf_as_json, spark, get_cluster_spark_session

from dash_apps.example1 import app as app_eg1
from dash_apps.multipage_app import app as multi_app
from routers.mapp import mappRouter

app = FastAPI()



@app.on_event("startup")
async def startup_event():
    # spark = get_local_spark_session(app_name="fastApi Startup")
    spark = get_cluster_spark_session()
    return spark


@app.on_event("shutdown")
async def shutdown_event():
    spark.stop()


@app.get("/spark")
def read_main():
    spark_conf_json=get_spark_conf_as_json(spark)
    return {"lohith says": f"DF is => ${spark_conf_json}"}

# app.mount("/eg1", WSGIMiddleware(app_eg1.server))
# app.mount("/", WSGIMiddleware(multi_app.server))


app.include_router(mappRouter, prefix="/mapp")


app.mount("/eg1", WSGIMiddleware(app_eg1.server))
app.mount("/mapp", WSGIMiddleware(multi_app.server))


# @app.get("/")
# def read_main():
#     return {"lohith says": "hello from Main App"}


if __name__ == '__main__':
    uvicorn.run("main:app", host=HOST, port=8000, reload=True)