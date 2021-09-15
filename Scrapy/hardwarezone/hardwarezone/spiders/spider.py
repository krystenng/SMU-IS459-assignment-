import scrapy

class SpiderSpider(scrapy.Spider):
    name = 'spider'
    start_urls = ['http://forums.hardwarezone.com.sg/forums/pc-gaming.382//']
    base_url = 'https://forums.hardwarezone.com.sg'

    def parse(self, response):

        for thread in response.xpath('//div[starts-with(@class, "structItem structItem")]'):

            content_url = self.base_url + thread.xpath('.//div[@class="structItem-title"]/a/@href').extract_first()

            yield scrapy.Request(content_url, callback=self.parse_thread, dont_filter=True)

        next_page = response.xpath('//a[starts-with(@class, "pageNav-jump pageNav-jump--next")]/@href').extract_first()
        next_page_url = self.base_url + next_page
        yield scrapy.Request(next_page_url, callback=self.parse, dont_filter=True)



    def parse_thread(self, response):

        next_page = response.xpath('//a[starts-with(@class, "pageNav-jump pageNav-jump--next")]/@href').extract_first()
        if next_page != None:
            posts = response.xpath('//article[starts-with(@class, "message message--post")]')
            for post in posts:

                topic = response.xpath('//h1[@class="p-title-value"]/text()').extract_first()
                author = post.xpath('.//h4/a/text()').extract_first()
                content = post.xpath('.//article/div[@class="bbWrapper"]/text()').extract_first()

                if author == None:
                    author = post.xpath('.//h4/a/span/text()').extract_first()

                yield {
                    'topic': topic,
                    'author': author,
                    'content': content
                }

            next_page_url = self.base_url + next_page
            yield scrapy.Request(next_page_url, callback=self.parse_thread, dont_filter=True)

        else:
            posts = response.xpath('//article[starts-with(@class, "message message--post")]')
            for post in posts:

                topic = response.xpath('//h1[@class="p-title-value"]/text()').extract_first()
                author = post.xpath('.//h4[@class="message-name"]/a/text()').extract_first()
                content = post.xpath('.//article/div[@class="bbWrapper"]/text()').extract_first()

                if author == None:
                    author = post.xpath('.//h4/a/span/text()').extract_first()

                yield {
                    'topic': topic,
                    'author': author,
                    'content': content
                }
            
