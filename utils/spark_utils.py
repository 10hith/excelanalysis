"""
All spark related utility functions goes here
"""
import os
from pyspark.sql import SparkSession

home = os.environ.get("PROJECT_HOME", ".")
keytab = os.environ["KEYTAB"]


def get_spark_session(
        racf: str,
        app_name: str="DeDash app") -> SparkSession:
    """
    :param principal: The Racf of the user
    :param app_name: Any App  name provided by the user
    :return: A Spark session created for the user
    """

    spark = (
        SparkSession.builder.appName(f"{app_name}")
            .enableHiveSupport()
            .master("yarn")
            .config("spark.yarn.keytab", keytab)
            .config("spark.yarn.principal", f"{racf}@EUROPA.RBSGRP.NET")
            .config(
            "spark.driver.extraJavaOptions",
            "-Djava.security.krb5.conf=" +
            os.getenv("KRB5_CONFIG", "/opt/edh/config/krb5-europa.ini")
        ).getOrCreate()
    )
    return spark
