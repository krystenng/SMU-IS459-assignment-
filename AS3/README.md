# Assignment 3 instructions

Navigation to codes:

Assignment 3 is inside the AS3 folder

AS3/

		README.md
		kafka_wordcount.py   
		kafka_postcount.py
		Scrapy/
			spiders/
				__init__.py
				spider.py
			items.py
			middlewares.py
			pipelines.py
			settings.py
			__init__.py
			
>>> kafka_wordcount.py --> This is the file to show the top-10 words in the posts in 2 minutes

>>> kafka_postcount.py --> This is the file to show the top-10 users with most posts in 2 minutes

>>> Instructions on how to run the code:

>>> Navigate to hadoop folder:

>>> sbin/start-dfs.sh

>>> sbin/start-yarn.sh

>>> Navigate to your kafka folder:

>>> bin/zookeeper-server-start.sh config/zookeeper.properties

>>> bin/kafka-server-start.sh config/server.properties

>>> bin/kafka-console-consumer.sh --topic scrapy-output --bootstrap-server localhost:9092 --> To run the kafka messages 

>>> Navigate to hardwarezone folder

>>> scrapy runspider spiders/spider.py --> To run the scrapy

>>> Navigate to AS3 folder:

>>> spark-submit --packages org.apache.spark:spark-sql-kafka-0-10_2.12:3.0.0 kafka_postcount.py --> To run to show the top-10 users with most posts in 2 minutes

>>> Clear spark-checkpoint in the hadoop to run the next file

>>> spark-submit --packages org.apache.spark:spark-sql-kafka-0-10_2.12:3.0.0 kafka_wordcount.py --> To run to show the top-10 words in the posts in 2 minutes



