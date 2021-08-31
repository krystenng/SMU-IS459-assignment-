# SMU-IS459-assignment-

Repo address: https://github.com/krystenng/SMU-IS459.git

Navigation to codes:
hardwarezone/
    scrapy.cfg   <-- Configuration file (DO NOT TOUCH!)
    result.json    <-- The results from the data crawled
    hardwarezone/
        items.py                 <-- Model of the item to scrap
        middlewares.py    <-- Scrapy processing hooks (DO NOT TOUCH)
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
>>> scrapy crawl spider                <-- ensure that the pipelines.py and settings.py have the codes to connect to the localhost
                                         port 27017
>>> used robo 3T to check whether the records have been dumped into mongoDB
