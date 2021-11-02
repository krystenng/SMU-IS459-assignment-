import pyspark
from pyspark.sql import SparkSession
from pyspark.ml.feature import Tokenizer
from pyspark.ml.feature import StopWordsRemover
import pyspark.sql.functions as f
from pyspark.sql import functions as F

# QUESTION 3 TO FIND ANY STRANGE COMMUNITY
# To find out any anomlay in the community
spark = SparkSession.builder.appName('sg.edu.smu.is459.assignment2').getOrCreate()

users_df = spark.read.load('/user/krystenng/parquet-input/assignment2.parquet')
users_df.show()

# Find out the number of posts each author post on the forum
author_rdd = users_df.rdd
author_rdd.first()
author_date_rdd =author_rdd.map(lambda x: (x[1],(x[2], 1)))
count_rdd = author_date_rdd.reduceByKey(lambda x, y: (x[0], x[1] + y[1]))
df_rdd = count_rdd.map(lambda x: (x[0],x[1][0],x[1][1]))
df = df_rdd.toDF()
df1 = df.withColumnRenamed('_1', 'author') \
        .withColumnRenamed('_2', 'joinedDate') \
        .withColumnRenamed('_3', 'num_of_posts') \

#sort by descending order to find out who has the most number of posts
df1.sort(F.desc('num_of_posts')).show()

# To find out the common topics discussed by the authors with the most number of posts
topic_rdd = users_df.rdd
topic_rdd.first()
topic_author_date_rdd =topic_rdd.map(lambda x: (x[1],(x[2], x[0], 1)))
countpost_rdd = topic_author_date_rdd.reduceByKey(lambda x, y: (x[0], x[1] + y[1], x[2] + y[2]))
df_topic_rdd = countpost_rdd.map(lambda x: (x[0],x[1][0],x[1][1], x[1][2]))
df_topic = df_topic_rdd.toDF()
df1_topic = df_topic.withColumnRenamed('_1', 'author') \
        .withColumnRenamed('_2', 'joinedDate') \
        .withColumnRenamed('_3', 'topic') \
        .withColumnRenamed('_4','num_of_posts')
        
df1_topic.sort(F.desc('num_of_posts')).show()

# To find out key words from topics discussed by authors who joined in the year 2008 as it has the most 
# number of authors who joined in that year
tokenizer = Tokenizer(inputCol="topic", outputCol="topic_token")
tokenized = tokenizer.transform(df1_topic).select("author", "joinedDate", "topic_token", "num_of_posts")
remover = StopWordsRemover(inputCol='topic_token', outputCol='topic_clean')
data_clean = remover.transform(tokenized).select("author", "joinedDate","topic_clean", "num_of_posts")
data_clean.show()
filtered_df = data_clean.filter(data_clean.joinedDate.like('%2008'))
results = filtered_df.withColumn('word', f.explode(f.col('topic_clean'))) \
	.groupBy('word') \
	.count().sort('count', ascending=False) 
word_count = results.collect()[:40]
for word in word_count:
    print(word[0] + ',' + str(word[1]) + '\t')
