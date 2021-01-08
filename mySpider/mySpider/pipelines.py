# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
import os

from itemadapter import ItemAdapter


class MyspiderPipeline:
    def process_item(self, item, spider):
        img_path = './download'
        if not os.path.exists(img_path):
            os.mkdir(img_path)
            if item.get('type') == 'img':
                with open(img_path + item.get('img_name'), 'wb') as f:
                    f.write(item.get('img_byte'))
                return
        # return item
