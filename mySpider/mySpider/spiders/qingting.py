import scrapy


class QingtingSpider(scrapy.Spider):
    name = 'qingting'
    allowed_domains = ['qingting.fm']
    start_urls = ['https://m.qingting.fm/rank/']

    def parse(self, response):
        # 存储提取到的30个a标签组成的列表对象
        a_list = response.xpath("//div[@class='rank-list']/a")
        # 使用for循环，依次处理每一个a标签对象
        for a_temp in a_list:
            # 排名
            rank_number = a_temp.xpath("./div[@class='badge']/text()").extract_first()
            # 图片的地址
            img_src = a_temp.xpath("./img/@src").extract_first()
            # 标题
            title = a_temp.xpath(".//div[@class='title']/text()").extract_first()
            # 描述
            desc = a_temp.xpath(".//div[@class='desc']/text()").extract_first()
            # 播放量
            play_number = a_temp.xpath(".//div[@class='info-item'][1]/span/text()").extract_first()
            # print("---->", rank_number, img_src, title, desc, play_number)
            # print("---->", rank_number.extract(), img_src.extract(), title.extract(), desc.extract(), play_number.extract())
            # print("---->", rank_number.extract_first(), img_src.extract_first(), title.extract_first(), desc.extract_first(), play_number.extract_first())

            # 生成的是信息（要在管道中进行处理）
            yield {
                "type": "info",
                "rank_number": rank_number,
                "img_src": img_src,
                "title": title,
                "desc": desc,
                "play_number": play_number
            }

            # 生成了一个请求对象
            # url表示要下载的地址，callback表示下载之后要回调的函数
            yield scrapy.Request(url=img_src, callback=self.parse_img, cb_kwargs={"img_name": title})

    def parse_img(self, response, img_name):
        # print("---2-->", response.url)
        # response.body  # 图片的二进制数据
        yield {
            "type": "img",
            "img_name": img_name + ".png",
            "img_bytes": response.body
        }
