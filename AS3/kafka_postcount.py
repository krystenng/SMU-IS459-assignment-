from pyspark.sql import SparkSession
from pyspark.sql.types import *
from pyspark.sql.functions import explode
from pyspark.sql.functions import split
from pyspark.sql import functions as F
from pyspark.sql.functions import *

def parse_data_from_kafka_message(sdf, schema):
    from pyspark.sql.functions import split
    assert sdf.isStreaming == True, "DataFrame doesn't receive streaming data"
    col = split(sdf['value'], '",')
    #split attributes to nested array in one Column
    #now expand col to multiple top-level columns
    for idx, field in enumerate(schema):
        sdf = sdf.withColumn(field.name, col.getItem(idx).cast(field.dataType))
    return sdf.select([field.name for field in schema])

if __name__ == "__main__":

    spark = SparkSession.builder \
               .appName("KafkaWordCount") \
               .getOrCreate()

    #Read from Kafka's topic scrapy-output
    df = spark.readStream \
            .format("kafka") \
            .option("kafka.bootstrap.servers", "localhost:9092") \
            .option("subscribe", "scrapy-output") \
            .option("startingOffsets", "latest") \
            .load()

    #Parse the fields in the value column of the message
    lines = df.selectExpr("CAST(value AS STRING)")

    #Specify the schema of the fields
    hardwarezoneSchema = StructType([ \
        StructField("topic", StringType()), \
        StructField("author", StringType()), \
        StructField("content", StringType()), \
        ])

    #Use the function to parse the fields
    lines = parse_data_from_kafka_message(lines, hardwarezoneSchema)
    lines = lines.withColumn("timestamp", current_timestamp())

    query = lines \
       .select("timestamp", "author") \
       .groupBy(window("timestamp", "2 minutes", "1 minute"), lines.author) \
       .count()

    querySort = query.orderBy(desc("count")).limit(10)
    #Select the content field and output
    contents = querySort.select("author", "count") \
        .writeStream \
        .queryName("WriteContent") \
        .outputMode("complete") \
        .format("console") \
        .option("checkpointLocation", "/user/krystenng/spark-checkpoint") \
        .option("truncate", False) \
        .start()

    #Start the job and wait for the incoming messages
    contents.awaitTermination()
