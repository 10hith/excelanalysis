from pyspark.sql import SparkSession
import json
from pathlib import Path
from pyspark.sql import DataFrame
import re


def get_project_root() -> Path:
    return Path(__file__).parent.parent


PROJECT_ROOT = get_project_root()
SPARK_NUM_PARTITIONS = 8

DEUTILS_PATH = str(PROJECT_ROOT) + "/resources/DqProfiler-1.0-SNAPSHOT-jar-with-dependencies.jar"


def get_local_spark_session(app_name: str = "SparkTest"):
    """
    Creates a local spark session.
            # .config("spark.sql.shuffle.partitions", f"{SPARK_NUM_PARTITIONS}") \
    Need to add more configuration
    :param app_name:
    :return:
    """
    spark = SparkSession \
        .builder \
        .appName(f"{app_name}") \
        .config('spark.jars', f'{DEUTILS_PATH}') \
        .getOrCreate()
    return spark


SPARK = get_local_spark_session(app_name="Upload Application")


def get_spark_conf_as_json(spark: SparkSession) -> json:
    """
    Returns the spark configuration as a json
    :param spark:
    :return:
    """
    configurations = spark.sparkContext.getConf().getAll()
    return json.dumps(dict(configurations))


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




