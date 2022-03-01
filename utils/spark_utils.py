import pandas as pd
from pyspark.sql import SparkSession
from databricks import koalas as ks
from pyspark.sql import functions as f
from utils.deutils import run_profile

from sedona.register import SedonaRegistrator
from sedona.utils import SedonaKryoRegistrator, KryoSerializer

import json
from pathlib import Path
from pyspark.sql import DataFrame
import re
import os


def get_project_root() -> Path:
    return Path(__file__).parent.parent


PROJECT_ROOT = get_project_root()
SPARK_NUM_PARTITIONS = 8

DATA_PATH = str(PROJECT_ROOT) + '/resources/data'
DEUTILS_PATH = str(PROJECT_ROOT) + '/resources/DqProfiler-1.0-SNAPSHOT-jar-with-dependencies.jar'
POSTGRES_JDBC = str(PROJECT_ROOT) + '/resources/postgresql-42.3.3.jar'
GEOTOOLS_JAR = str(PROJECT_ROOT) + '/resources/geotools-wrapper-1.1.0-25.2.jar'
SEDONA_JAR = str(PROJECT_ROOT) + '/resources/sedona-python-adapter-3.0_2.12-1.1.1-incubating.jar'
AWS_JAVA = str(PROJECT_ROOT) + '/resources/aws-java-sdk-bundle-1.12.167.jar'
HADOOP_AWS = str(PROJECT_ROOT) + '/resources/hadoop-aws-3.2.0.jar'

os.environ["PYARROW_IGNORE_TIMEZONE"] = "1"


def get_local_spark_session(app_name: str = "SparkTest"):
    """
    Creates a local spark session.
            # .config("spark.sql.shuffle.partitions", f"{SPARK_NUM_PARTITIONS}") \
            spark.debug.maxToStringFields=100
            spark.conf.set("spark.sql.debug.maxToStringFields", 100)
        .config('spark.sql.execution.arrow.pyspark.enabled', True) \
        .config('spark.sql.session.timeZone', 'UTC') \
        .config('spark.driver.memory','32G') \
    Need to add more configuration
    :param app_name:
    :return:
    """
    spark = SparkSession \
        .builder \
        .appName(f"{app_name}") \
        .config("spark.sql.shuffle.partitions", f"{SPARK_NUM_PARTITIONS}") \
        .config('spark.jars', f"{DEUTILS_PATH},{POSTGRES_JDBC}") \
        .config("driver-class-path", f"{POSTGRES_JDBC}")\
        .config('spark.sql.session.timeZone', 'UTC') \
        .config('spark.sql.execution.arrow.pyspark.enabled', True) \
        .config('spark.debug.maxToStringFields', 0) \
        .getOrCreate()
    return spark


# def get_cluster_spark_session(app_name: str = "SparkCluster"):
#     """
#     Creates a local spark session.
#             # .config("spark.sql.shuffle.partitions", f"{SPARK_NUM_PARTITIONS}") \
#             spark.debug.maxToStringFields=100
#             spark.conf.set("spark.sql.debug.maxToStringFields", 100)
#         .config('spark.sql.execution.arrow.pyspark.enabled', True) \
#         .config('spark.sql.session.timeZone', 'UTC') \
#         .config('spark.driver.memory','32G') \
#     Need to add more configuration
#     :param app_name:
#     :return:
#     """
#     spark = SparkSession \
#         .builder \
#         .master("spark://spark-master:7077") \
#         .config("spark.executor.memory", "512m") \
#         .config("spark.sql.shuffle.partitions", f"{SPARK_NUM_PARTITIONS}") \
#         .config('spark.jars', f"{DEUTILS_PATH},{POSTGRES_JDBC}") \
#         .config("driver-class-path", f"{POSTGRES_JDBC}")\
#         .config('spark.sql.session.timeZone', 'UTC') \
#         .config('spark.sql.execution.arrow.pyspark.enabled', True) \
#         .config('spark.debug.maxToStringFields', 0) \
#         .getOrCreate()
#     return spark


def get_spatial_spark_session(app_name: str = "SparkTest"):
    """
    Creates a local spark session.
            # .config("spark.sql.shuffle.partitions", f"{SPARK_NUM_PARTITIONS}") \
            spark.debug.maxToStringFields=100
            spark.conf.set("spark.sql.debug.maxToStringFields", 100)
        .config('spark.sql.execution.arrow.pyspark.enabled', True) \
        .config('spark.sql.session.timeZone', 'UTC') \
        .config('spark.driver.memory','32G') \
    Need to add more configuration
    :param app_name:
    :return:
    """
    spark = SparkSession \
        .builder \
        .appName(f"{app_name}") \
        .config("spark.sql.shuffle.partitions", f"{SPARK_NUM_PARTITIONS}") \
        .config('spark.jars',
                f"{DEUTILS_PATH},"
                f"{POSTGRES_JDBC},"
                f"{SEDONA_JAR},"
                f"{GEOTOOLS_JAR},"
                f"{HADOOP_AWS},"
                f"{AWS_JAVA}"
                ) \
        .config("spark.serializer", KryoSerializer.getName) \
        .config("spark.kryo.registrator", SedonaKryoRegistrator.getName) \
        .config("driver-class-path", f"{POSTGRES_JDBC}")\
        .config('spark.sql.session.timeZone', 'UTC') \
        .config('spark.sql.execution.arrow.pyspark.enabled', True) \
        .config('spark.debug.maxToStringFields', 0) \
        .getOrCreate()

    SedonaRegistrator.registerAll(spark)

    return spark


spark = get_spatial_spark_session(app_name="GeoSpatial Application")


def get_spark_conf_as_json(spark: SparkSession) -> json:
    """
    Returns the spark configuration as a json
    :param spark:
    :return:
    """
    configurations = spark.sparkContext.getConf().getAll()
    return json.dumps(dict(configurations))


def get_summary_and_histogram_dfs(pdf: pd.DataFrame, spark) -> (pd.DataFrame, pd.DataFrame):
    kdf = ks.from_pandas(pdf)
    sdf = kdf.to_spark()
    profiled_sdf = run_profile(spark, sdf)

    histogram_sdf = profiled_sdf.\
        select(
        "column_name",
        f.explode("histogram").alias("histogram")
    ).selectExpr(
        "column_name",
        f"CASE "
        f"WHEN LENGTH(histogram.value)>{10} "
        f"THEN CONCAT(SUBSTRING(histogram.value,1,{10}), '..')"
        f"ELSE histogram.value END as value",
        f"histogram.value as value_complete",
        "histogram.num_occurrences as num_occurrences",
        "histogram.ratio*100 as percentage")

    summary_stats_sdf: spark.sql.DataFrame = profiled_sdf.drop("histogram")

    summary_stats_pdf: pd.DataFrame = summary_stats_sdf.toPandas()
    histogram_pdf: pd.DataFrame = histogram_sdf.toPandas()
    # Get the size of the dataframe
    size = summary_stats_pdf['size'].iloc[0]
    summary_stats_pdf.drop('size', axis=1, inplace=True)

    num_cat_cols = summary_stats_pdf['distribution_available'].sum().astype(int)

    return summary_stats_pdf, histogram_pdf, size, num_cat_cols


def transform(self, f):
    """
    Method monkey patched into the DataFrame class.
    It enables to chain the transformations/functions passed as f
    Usage:  testDF.\
        transform(with_date_cols_casted).\
        transform(with_decimal_cols_casted).\
        transform(trim_columns(["col2", "col2"]))
    """
    return f(self)


DataFrame.transform = transform


def cleanup_col_name(col_name: str):
    str_no_special_chars = re.sub(r"[^a-zA-Z0-9]+", ' ', col_name)
    str_w_single_space = ' '.join(str_no_special_chars.split())
    str_w_underscore = str_w_single_space.replace(' ', '_' )
    return col_name, str_w_underscore.lower()


def build_select_expr(cols_map):
    select_expr = [" `{}` as {}".format(x[0],x[1]) for x in cols_map]
    return select_expr


def with_std_column_names():
    """
    Conform all the columns to be stripped of all whitespaces lowercase
    Args:
        cols: list of columns
    Returns:
        Dataframe with specified columns converted
    """

    def inner(df):
        cols_map = [cleanup_col_name(x) for x in df.columns]
        select_expr=build_select_expr(cols_map)
        return df.selectExpr(select_expr)

    return inner


def get_crime(lkp_lat, lkp_log, spark):
    df = spark.sql(f"""
    SELECT 
    crime_type,
    CAST(CONCAT(mnth,'-01') AS DATE) AS mnth,
    lat,
    log as lon,
    CONCAT(lat,',',log) AS point,
    ST_Distance(
        crime_geo,
        ST_Transform(ST_Point({lkp_lat},{lkp_log}),'epsg:4326', 'epsg:3857')
        )/1609 AS distance_in_km
    FROM 
    crime
    WHERE ST_Distance(
        crime_geo,
        ST_Transform(ST_Point({lkp_lat},{lkp_log}),'epsg:4326', 'epsg:3857')
        )/1609 < .321
    """)

    df = df.withColumn("tooltip",f.expr(
        """CONCAT(crime_type, '-', ROUND(distance_in_km,2), ' km away') """)
                       )
    return df


