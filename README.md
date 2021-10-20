# SMU-IS459-assignment-
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

>>> Instructions on how to run it, please look at the README.md in AS3 folder

# Assignment 2 instructions

Navigation to codes:


Python code for questions 1 and 2:

>>> assignment_2_q1q2.py


Python code for question 3:

>>> assignment_2_q3.py


Data scraped for question3:

assignment2/

		result.json   
		scrapy.cfg
		assignment2.parquet
		mongodb_to_parquet.py
        	assignment2/
			spiders/
				__init__.py
				spider.py
			items.py
			middlewares.py
			pipelines.py
			settings.py
			__init__.py



# Assignment 1 instructions

Navigation to codes:
hardwarezone/

    scrapy.cfg   <-- Configuration file
    result.json    <-- The results from the data crawled
    hardwarezone/
        items.py                 <-- Model of the item to scrap
        middlewares.py    <-- Scrapy processing hooks
        pipelines.py           <-- What to do with the scraped item
        settings.py             <-- Settings file
        spiders/                  <-- Directory of the spider
            __init__.py
            spider.py         <--- Containing xpath codes to extract the data

Creating spider in the terminal using visual studio code:

>>> scrapy startproject hardwarezone

>>> cd  hardwarezone

>>> scrapy genspider spider forums.hardwarezone.com.sg/forums/pc-gaming.382/        <--- connecting to the webpage

>>> scrapy crawl spider           <-- to run the spider

>>> scrapy runspider spider.py -o result.json       <-- in order to get the output (data) crawled from the website        

Using ubuntu (20.04) to dump the records to mongoDB:

>>> clone your git repo to ubuntu

>>> cd SMU-IS459(assignment)

>>> cd Scrapy

>>> cd hardwarezone

>>> mongd       <-- in another terminal to start your mongoDB running

>>> mongo

>>> scrapy crawl spider                <-- ensure that the pipelines.py and settings.py have the codes to connect to the localhost
                                         port 27017

>>> used robo 3T to check whether the records have been dumped into mongoDB
