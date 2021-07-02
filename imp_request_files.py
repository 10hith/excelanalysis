from fastapi import FastAPI, File, UploadFile
# impor python-multipart
import uvicorn
from pyspark.sql import SparkSession
import os
from pyspark.sql import SparkSession

home = os.environ.get("PROJECT_HOME", ".")
keytab = os.environ["KEYTAB"]


app = FastAPI()


@app.post("/files/")
async def create_file(file: bytes = File(...)):
    return {"file_size": len(file)}


# @app.post("/spark/{racf}")


@app.post("/uploadfile/")
async def create_upload_file(file: UploadFile = File(...)):
    return {"filename": file.filename}


@app.post("/uploadkeytab/")
async def create_upload_file(file: UploadFile = File(...)):
    """
    :param principal: The Racf of the user
    :param app_name: Any App  name provided by the user
    :return: A Spark session created for the user
    """
    contents = await file.read()
    spark = (
        SparkSession.builder.appName(f"DeDash")
            .enableHiveSupport()
            .master("yarn")
            .config("spark.yarn.keytab", contents)
            .config("spark.yarn.principal", f"basal@EUROPA.RBSGRP.NET")
            .config(
            "spark.driver.extraJavaOptions",
            "-Djava.security.krb5.conf=" +
            os.getenv("KRB5_CONFIG", "/opt/edh/config/krb5-europa.ini")
        ).getOrCreate()
    )
    return {"Spark session created": f"{spark}"}


if __name__ == "__main__":
    uvicorn.run("imp_request_files:app", host="11.15.93.81", port=8000, reload=True)