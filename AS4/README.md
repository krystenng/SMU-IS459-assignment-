# Assignment 4 instructions

# Results of the post-count:
<img width="871" alt="image" src="https://user-images.githubusercontent.com/79707828/142149752-12859fe0-c54b-4178-a644-bb3e0d8e2e76.png">


## Files that are edited:

> 1. postcount_kafka.py
> >> Edited the codes to output to kafka broker:
> >> 
> >> Drop the columns with null author
> >> > Navigation to codes is as shown:
```
>>> cd SMU-IS459-assignment-/AS4/django/hwz_monitor/
>>> nano postcount_kafka.py
```
Link: [postcount_kafka.py](https://github.com/krystenng/SMU-IS459-assignment-/blob/main/AS4/django/hwz_monitor/postcount_kafka.py)

> 2. views.py
> >> Edited the codes to get the output from kafka broker
> >> 
> >> Will get the latest top10 post as by default the auto.offset.reset = latest already
> >> 
> >> Set the timeout, so that it will not run forever and will get the latest top 10 post from broker
> >> > Navigation to codes is as shown:
```
>>> nano SMU-IS459-assignment-/AS4/django/hwz_monitor/dashboard/views.py
```
Link: [views.py](https://github.com/krystenng/SMU-IS459-assignment-/blob/main/AS4/django/hwz_monitor/dashboard/views.py)

> 3. urls.py
>  >> Edited the codes to replace post-count-chart with kafka count so that output from kafka can be shown on barchart:
>  >> > Navigation to codes is as shown:
```
>>> nano SMU-IS459-assignment-/AS4/django/hwz_monitor/dashboard/urls.py 
```
Link: [urls.py](https://github.com/krystenng/SMU-IS459-assignment-/blob/main/AS4/django/hwz_monitor/dashboard/urls.py)

> 4. barchart.html
> >> Edited this such that the labels and data matches with the JSONResponse from kafka
> >> > Navigation to codes is as shown:
```
>>> nano SMU-IS459-assignment-/AS4/django/hwz_monitor/dashboard/templates/barchart.html
```
Link: [barchart.html](https://github.com/krystenng/SMU-IS459-assignment-/blob/main/AS4/django/hwz_monitor/dashboard/templates/barchart.html)

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
>>> cd kafka_2.12-3.0.0
>>> bin/kafka-server-start.sh config/server.properties
```

**Open a new terminal:**
```
>>> mongod
```

**Open a new terminal to consume the kafka messages for scrapy:**
```
>>> cd kafka_2.12-3.0.0
>>> bin/kafka-console-consumer.sh --topic scrapy-output --bootstrap-server localhost:9092
```

**Open a new terminal to run scrapy:**
```
>>> cd SMU-IS459-assignment-/AS4/django/hwz_monitor/tasks/hardwarezone/hardwarezone
>>> scrapy runspider spiders/spider.py
```

**Open a new terminal to run the spark streaming:**
```
>>> cd SMU-IS459-assignment-/AS4/django/hwz_monitor
>>> spark-submit --packages org.apache.spark:spark-sql-kafka-0-10_2.12:3.0.0 postcount_kafka.py
```
>>> However, if there is an **error** running the spark, which would probably be a bug in kafka-0.10_2.12:3.0.0, do run it using this code:
```
>>> spark-submit --packages org.apache.spark:spark-sql-kafka-0-10_2.12:3.1.2 postcount_kafka.py
```

*If necessary to clear checkpoint, open a new terminal:*
```
>>> hadoop fs -rm -r -f /user/krystenng/spark-checkpoint
>>> hadoop fs -mkdir /user/krystenng/spark-checkpoint
```

**Open a new terminal to start the kafka broker running:**
```
>>> cd kafka_2.12-3.0.0
>>> bin/kafka-console-consumer.sh --topic stream_data --bootstrap-server localhost:9092
```

**Open a new terminal to start the server running on port 8000:**
```
>>> cd SMU-IS459-assignment-/AS4/django/hwz_monitor
>>> python manage.py runserver
```
*If port 8000 is used, can run on port 8080:*
```
>>> cd SMU-IS459-assignment-/AS4/django/hwz_monitor
>>> python manage.py runserver 8080
```

### Start up the browser:
```
>> To see the top 10 authors and count in json format
>>> http://localhost:8000/dashboard/kafka
>> To see the top 10 post-count, represented by a barchart
>>> http://localhost:8000/dashboard/barchart
```
***To note: Refresh both pages to see a new set of output***









