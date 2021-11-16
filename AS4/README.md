# Assignment 4 instructions

# Results of the post-count:

## Files that are edited:
> 1. postcount_kafka.py
```
>>> cd /AS4/django/hwz_monitor/
>>> nano postcount_kafka.py
```
>> Edited the codes to output to kafka broker

> 2. views.py
```
>>> cd /AS4/django/hwz_monitor/dashboard/views.py
```

## Things that need to be installed beforehand:
```
>>> pip install django
>>> pip install celery
>>> pip install graphene_django
>>> pip install django-cors-headers
```

## Things that need to be run to get the output:

**Open terminal:**
```
>>> sudo apt remove openssh-server
>>> sudo apt install openssh-server
>>> sudo service ssh start
```

**Open a new terminal:**
```
>>> cd hadoop/hadoop-3.3.0
>>> sbin/start-dfs.sh
>>> sbin/start-yarn.sh
```

**Open a new terminal:**
```
>>> cd kafka_2.12-3.0.0
>>> bin/zookeeper-server-start.sh config/zookeeper.properties
```

**Open a new terminal:**
```
>>> bin/kafka-server-start.sh config/server.properties
```

**Open a new terminal:**
```
>>> mongod
```

**Open a new terminal to start the kafka messages for scrapy:**
```
>>> cd kafka_2.12-3.0.0
>>> bin/kafka-console-consumer.sh --topic scrapy-output --bootstrap-server localhost:9092
```

**Open a new terminal to run scrapy:**
```
>>> cd /SMU-IS459-assignment-/AS4/django/hwz_monitor/tasks/hardwarezone/hardwarezone
>>> scrapy runspider spiders/spider.py
```

**Open a new terminal to run the spark streaming:**
```
>>> cd /SMU-IS459-assignment-/AS4/django/hwz_monitor
>>> spark-submit --packages org.apache.spark:spark-sql-kafka-0-10_2.12:3.0.0 postcount_kafka.py
```
>>> However, if there is an **error** running the spark, which would probably be a bug in kafka-0.10_2.12:3.0.0, do run it using this code:
```
>>> spark-submit --packages org.apache.spark:spark-sql-kafka-0-10_2.12:3.1.2 postcount_kafka.py
```

**Open a new terminal to start the kafka broker running:**
```
>>> cd kafka_2.12-3.0.0
>>> bin/kafka-console-consumer.sh --topic stream_data --bootstrap-server localhost:9092
```

**If necessary to clear checkpoint, open a new terminal:**
```
>>> *hadoop fs -rm -r -f /user/krystenng/spark-checkpoint*
>>> *hadoop fs -mkdir /user/krystenng/spark-checkpoint*
```







