from pyspark.sql import SparkSession
import json
from pathlib import Path


def get_project_root() -> Path:
    return Path(__file__).parent.parent


PROJECT_ROOT = get_project_root()

DEUTILS_PATH = str(PROJECT_ROOT) + "/resources/deutils.jar"


def get_local_spark_session(app_name: str = "SparkTest"):
    """
    Creates a local spark session.
    Need to add more configuration
    :param app_name:
    :return:
    """
    spark = SparkSession \
        .builder \
        .appName(f"{app_name}") \
        .config("spark.some.config.option", "some-value") \
        .config('spark.jars', f'{DEUTILS_PATH}') \
        .getOrCreate()
    return spark


def get_spark_conf_as_json(spark: SparkSession) -> json:
    """
    Returns the spark configuration as a json
    :param spark:
    :return:
    """
    configurations = spark.sparkContext.getConf().getAll()
    return json.dumps(dict(configurations))
