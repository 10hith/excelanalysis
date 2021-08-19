"""
Module containing python wrappers around the utils framework
utils is built on Deequ and contains all dependencies within the jar (./resources/utils.jar)
"""
from typing import List

from py4j import java_gateway
from py4j.java_gateway import JavaObject
from pyspark.sql import DataFrame, SparkSession, SQLContext


# pylint: disable=protected-access
def get_sql_ctx(spark_session: SparkSession) -> SQLContext:
    """
    Returns the SQLContext that is used to wrap JVM variables
    :param spark_session: Spark Session
    :return:SQLContext
    """
    return SQLContext(
        sparkContext=spark_session._sc,
        sparkSession=spark_session,
        jsqlContext=spark_session._jsparkSession.sqlContext(),
    )


def create_df_from_jdf(jdf: JavaObject, spark_session: SparkSession) -> DataFrame:
    """
    Creates a Spark dataframe from Java dataframe (_jdf)
    Args:
        jdf: Java dataframe
        spark_session: Spark session
    Return:
        Spark DataFrame
    """
    return DataFrame(jdf, get_sql_ctx(spark_session))


def to_scala_seq(jvm: java_gateway, iterable: List) -> JavaObject:
    """
    Helper method to take an iterable and turn it into a Scala sequence
    Args:
        jvm: Spark session's JVM
        iterable: your iterable
    Returns:
        Scala sequence
    """
    return jvm.scala.collection.JavaConversions.iterableAsScalaIterable(
        iterable
    ).toSeq()


def run_profile(spark: SparkSession, df: DataFrame) -> DataFrame:
    """
    Runs the runProfile method in DEUtils provided as a jar, accessed via the JVM variable
    Usage: run_profile(spark, df)
    Args:
        spark: Spark Session
        df: Input DataFrame that needs to be profiled
    Returns:
        Profiled DataFrame for all columns
    """
    _run_profile = spark._jvm.ProfileHelpers.runProfileWideDf
    jdf = _run_profile(df._jdf)
    return create_df_from_jdf(jdf, spark)


def get_distribution(spark_session: SparkSession, df: DataFrame, *cols) -> DataFrame:
    """
    Runs the runProfile method in DEUtils provided as a jar, accessed via the JVM variable
    Usage: get_distribution(spark, df, "column_1", "column_2")
    Args:
        df: Input DataFrame that needs to be profiled
        spark_session: Spark Session
        cols: List of categorical columns
    Returns:
        Value distribution(with counts and %) of the categorical columns
    """
    _get_distribution = spark_session._jvm.DEUtils.DQ.HistogramHelpers.getDistribution
    scala_cols_sql = to_scala_seq(spark_session._jvm, cols)
    jdf = _get_distribution(df._jdf, scala_cols_sql)
    return create_df_from_jdf(jdf, spark_session)


def compare_dfs(spark: SparkSession, df1: DataFrame, df2: DataFrame) -> DataFrame:
    """
    Gather metrics for df1 and apply them on df2.
    Returns the comparision results
    Usage: compare_dfs(spark, df1, df2)
    Args:
        spark: Spark Session
        df1: Input DataFrame on which constraints are generated
        df2: Input DataFrame against which the constraints are applied to
    Returns:
        Result of the comparision
    """
    _compare_df = spark._jvm.DEUtils.DQ.CompareHelpers.compareWith
    jdf = _compare_df(df2._jdf, df1._jdf)
    return create_df_from_jdf(jdf, spark)