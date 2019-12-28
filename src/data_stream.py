import logging

from pyspark.sql import SparkSession
from pyspark.sql.types import StringType, StructType, StructField, TimestampType
import pyspark.sql.functions as psf

import settings


# TODO Create a schema for incoming resources (DONE)
schema = StructType([
    StructField("crime_id", StringType(), False),
    StructField("original_crime_type_name", StringType(), False),
    StructField("report_date", TimestampType(), False),
    StructField("call_date", TimestampType(), False),
    StructField("offense_date", TimestampType(), False),
    StructField("call_time", StringType(), False),
    StructField("call_date_time", TimestampType(), False),
    StructField("disposition", StringType(), False),
    StructField("address", StringType(), False),
    StructField("city", StringType(), False),
    StructField("state", StringType(), False),
    StructField("agency_id", StringType(), False),
    StructField("address_type", StringType(), False),
    StructField("common_location", StringType(), False),
])


def run_spark_job(spark):

    # TODO Create Spark Configuration (DONE)
    # Create Spark configurations with max offset of 200 per trigger
    # set up correct bootstrap server and port
    df = spark \
        .readStream \
        .format("kafka") \
        .option("kafka.bootstrap.servers", settings.KAFKA_BOOTSTRAP_SERVERS) \
        .option("subscribe", settings.KAFKA_TOPIC) \
        .option("startingOffsets", "earliest") \
        .option("maxOffsetsPerTrigger", "200") \
        .option("stopGracefullyOnShutdown", "true") \
        .load()

    # Show schema for the incoming resources for checks
    df.printSchema()

    # TODO extract the correct column from the kafka input resources
    # Take only value and convert it to String
    kafka_df = df.selectExpr("CAST(value as string)")

    service_table = kafka_df \
        .select(psf.from_json(psf.col('value'), schema).alias("DF")) \
        .select("DF.*")

    # TODO select original_crime_type_name and disposition (DONE)
    distinct_table = service_table.select("original_crime_type_name", "disposition")

    # count the number of original crime type
    # NOTE: I added the disposition column to the group by in order for the join to work
    #       It was unclear from the instructions if that was what I was supposed to do
    agg_df = distinct_table.groupBy("original_crime_type_name", "disposition").count()

    # TODO get the right radio code json path (DONE)
    radio_code_json_filepath = settings.RADIO_CODES
    radio_code_df = spark.read.option("multiline", "true").json(radio_code_json_filepath)

    # clean up your data so that the column names match on radio_code_df and agg_df
    # we will want to join on the disposition code

    # TODO rename disposition_code column to disposition (DONE)
    radio_code_df = radio_code_df.withColumnRenamed("disposition_code", "disposition")

    # TODO join on disposition column (DONE)
    join_query = agg_df.join(radio_code_df, "disposition")

    # NOTE: I moved the writeStream to the end so that the join would be appied
    query = join_query \
        .writeStream \
        .format("console") \
        .trigger(processingTime="120 seconds") \
        .outputMode("Complete") \
        .option("truncate", "false") \
        .start()

    # TODO attach a ProgressReporter (DONE)
    query.awaitTermination()


if __name__ == "__main__":
    logger = logging.getLogger(__name__)

    # TODO Create Spark in Standalone mode
    spark = SparkSession \
        .builder \
        .master("local[*]") \
        .appName("KafkaSparkStructuredStreaming") \
        .config("spark.executor.memory", "1g") \
        .config("spark.python.worker.memory", "512m") \
        .config("spark.memory.fraction", "1.0") \
        .config("spark.memory.storageFraction", "0.5") \
        .config("spark.serializer", "org.apache.spark.serializer.KryoSerializer") \
        .getOrCreate()

    logger.info("Spark started")

    run_spark_job(spark)

    spark.stop()
