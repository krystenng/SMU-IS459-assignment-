import pyspark
from pyspark.sql import SparkSession
from pyspark.sql.functions import monotonically_increasing_id
from graphframes import *
from nltk import tokenize
from operator import itemgetter
import math
import nltk
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
import string
from nltk.stem import WordNetLemmatizer

spark = SparkSession.builder.appName('sg.edu.smu.is459.assignment2').getOrCreate()

# Load data
posts_df = spark.read.load('/user/krystenng/parquet-input/hardwarezone.parquet')

# Clean the dataframe by removing rows with any null value
posts_df = posts_df.na.drop()

#posts_df.createOrReplaceTempView("posts")

# Find distinct users
#distinct_author = spark.sql("SELECT DISTINCT author FROM posts")
author_df = posts_df.select('author').distinct()

print('Author number :' + str(author_df.count()))

# Assign ID to the users
author_id = author_df.withColumn('id', monotonically_increasing_id())
author_id.show()

# Construct connection between post and author 
# have two tables so that later on can map the author of the same topic together side by side
left_df = posts_df.select('topic', 'author') \
    .withColumnRenamed("topic","ltopic") \
    .withColumnRenamed("author","src_author")

right_df =  left_df.withColumnRenamed('ltopic', 'rtopic') \
    .withColumnRenamed('src_author', 'dst_author')

#  Self join on topic to build connection between authors
# if they are on the same topic, to build a connection side by side
author_to_author = left_df. \
    join(right_df, left_df.ltopic == right_df.rtopic) \
    .select(left_df.src_author, right_df.dst_author) \
    .distinct()
edge_num = author_to_author.count()
print('Number of edges with duplicate : ' + str(edge_num)) #1498263

# Convert it into ids
#for all the dst authors, link to the author of the same topic but with their ids only
id_to_author = author_to_author \
    .join(author_id, author_to_author.src_author == author_id.author) \
    .select(author_to_author.dst_author, author_id.id) \
    .withColumnRenamed('id','src')

id_to_id = id_to_author \
    .join(author_id, id_to_author.dst_author == author_id.author) \
    .select(id_to_author.src, author_id.id) \
    .withColumnRenamed('id', 'dst')

id_to_id = id_to_id.filter(id_to_id.src >= id_to_id.dst).distinct()

id_to_id.cache()

print("Number of edges without duplciate :" + str(id_to_id.count()))

# Build graph with RDDs
graph = GraphFrame(author_id, id_to_id)

# For complex graph queries, e.g., connected components, you need to set
# the checkopoint directory on HDFS, so Spark can handle failures.
# Remember to change to a valid directory in your HDFS
spark.sparkContext.setCheckpointDir('/user/krystenng/spark-checkpoint')

# To get the connected components:
result = graph.connectedComponents()

# Getting the number of unconnected components:
result.filter("component != '0'").count()

# Getting the number of connected components:
num_connected_components = result.filter("component == '0'").count()

print("The number of connected components are :" + str(num_connected_components))

# To get the top 20 most frequent words in the topics of hardwarezone forum
postCollect = posts_df.collect()

content_str = ''

# Remove stop words from the topics and put them into a string
stop_words = set(stopwords.words('english'))
for post in postCollect:
	if post['content'] not in stop_words:
		content_str += post['content'].lower() + ''

# Remove unnecessary punctuations from the string
data = str.maketrans(dict.fromkeys(string.punctuation))
topics_without_punctuation = content_str.translate(data)

# Lemmatize the words so that the words will be in the base form and it will be easier to identify key words
lemmatizer = WordNetLemmatizer()
content_clean = ''
for w in topics_without_punctuation:
	content_clean += lemmatizer.lemmatize(w)

# Split the words into array 
words_array = content_clean.split()

# To put the words and their count into a dictionary: key is the word and the value is the number of times the word appear
df = {}
for word in words_array:
	if word not in df:
		df[word] = 1
	else:
		df[word] += 1

tf_score = df
# Calculate the score of the words by using the df_idf method, as there are no more than one file, only df score is calculated
total_word_length = len(words_array) 
tf_score.update((x, y/int(total_word_length)) for x, y in tf_score.items())

# Function to get the top n words from the dict
def get_top_n(dict_elem, n):
    result = dict(sorted(dict_elem.items(), key = itemgetter(1), reverse = True)[:n]) 
    return result

#Get the top 20 words
top200_words = get_top_n(tf_score, 200)

top200 = ''
for word in top200_words:
    top200 += word + ', '

top200 = top200[:-2]

print("The most frequent words are the following :" + '\n' + top200)

# To get the triangle count for each author
results = graph.triangleCount()

# Rename the count to num_of_triangles to identify it
results = results.withColumnRenamed('count', 'num_of_triangles')

# To get the dataframe of total number of triangles for the community
num_of_triangles = results.agg({'num_of_triangles':'sum'})

# Get the total number of triangles as a value, string
total_num_triangles = num_of_triangles.collect()[0][0]

# Count the number of authors present in the hardwarezone
count = results.count()

avg_num_triangles = int(total_num_triangles/count)

print("Average # of triangles over every user in a community is :" + str(avg_num_triangles))
