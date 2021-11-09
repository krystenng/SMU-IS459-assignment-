from pyspark.sql import SparkSession
from pyspark.sql.types import *
from pyspark.sql.functions import explode
from pyspark.sql.functions import from_json, col, window, current_timestamp, desc


if __name__ == "__main__":

    spark = SparkSession.builder \
               .appName("KafkaWordCount") \
               .getOrCreate()

    #Read from Kafka's topic scrapy-output
    df = spark.readStream \
            .format("kafka") \
            .option("kafka.bootstrap.servers", "localhost:9092") \
            .option("subscribe", "scrapy-output") \
            .option("startingOffsets", "earliest") \
            .load()

    #Parse the fields in the value column of the message
    lines = df.selectExpr("CAST(value AS STRING)", "timestamp")

    #Specify the schema of the fields
    hardwarezoneSchema = StructType([ \
        StructField("topic", StringType()), \
        StructField("author", StringType()), \
        StructField("content", StringType()) \
        ])

    #Use the function to parse the fields
    # lines = parse_data_from_kafka_message(lines, hardwarezoneSchema) \
    #     .select("topic","author","content","timestamp")
    lines = lines.withColumn('data', from_json(col("value"), schema=hardwarezoneSchema)).select('timestamp', 'data.*')


    # Top-10 users with most posts in 2 minutes

    users_df = lines.select("timestamp", "author") \
        .groupBy(window("timestamp", "2 minutes", "1 minute"), "author").count() \
        .withColumn("start", col("window")["start"]) \
        .withColumn("end", col("window")["end"]) \
        .withColumn("current_timestamp", current_timestamp()) 

    top10_authorsDF = users_df \
        .filter(users_df.end < users_df.current_timestamp) \
        .orderBy(desc('window'), desc("count")).limit(10)

    # #Select the content field and output
    contents1 = top10_authorsDF.select("author", "count") \
        .writeStream \
        .queryName("WriteContent1") \
        .trigger(processingTime="1 minute") \
        .outputMode("complete") \
        .format("console") \
        .option("checkpointLocation", "/user/krystenng/spark-checkpoint") \
        .start()

    #Start the job and wait for the incoming messages
    contents1.awaitTermination()
