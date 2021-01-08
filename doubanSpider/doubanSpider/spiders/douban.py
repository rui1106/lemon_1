import scrapy


class DoubanSpider(scrapy.Spider):
    name = 'douban'
    allowed_domains = ['douban.com', 'doubanio.com']
    start_urls = ['https://movie.douban.com/top250?start=0&filter=']
    pages = 0
    num = 1

    def parse(self, response):
        li_list = response.xpath('//ol[@class="grid_view"]/li')

        for li in li_list:
            titles = li.xpath('.//a/span/text()').extract()
            titles = titles[0].strip()
            title = ''.join(titles)
            actors = li.xpath('.//div[@class="bd"]/p[1]/text()').extract()
            grade = li.xpath(".//div[@class='star']/span[@class='rating_num']/text()")[0].extract()
            evaluate_num = li.xpath(".//div[@class='star']/span[4]/text()")[0].extract()
            quote = li.xpath(".//p[@class='quote']/span/text()")[0].extract()
            img_url = li.xpath(".//div[@class='pic']//img/@src")[0].extract()
            print('======>', title)
            actor = actors[0].strip()
            time = actors[1].strip()
            print(img_url)
            # print('======>', actor)
            # print('======>', time)
            # print('======>', grade)
            # print('======>', evaluate_num)
            # print('======>', quote)

            temp_dict = {
                "type": 'info',
                'title': title,
                "actor": actor,
                "time": time,
                "grade": grade,
                "evaluate_num": evaluate_num,
                "quote": quote
            }
            yield temp_dict

            yield scrapy.Request(url=img_url, callback=self.parse_img, cb_kwargs={'title': titles})
        self.pages += 25
        self.num += 1
        if self.num <= 10:
            url = 'https://movie.douban.com/top250?start=%s&filter=' % self.pages
            yield scrapy.Request(url=url, callback=self.parse)

    def parse_img(self, response, title):
        print("----图片url----", response.url)
        yield {
            'type': "img",
            'img_name': title + ".png",
            'img_bytes': response.body
        }
