# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
import csv
import os

from itemadapter import ItemAdapter


class DoubanspiderPipeline:
    def process_item(self, item, spider):
        img_name = item.get("img_name")
        img_byte = item.get("img_bytes")
        img_path = './download'
        if not os.path.exists(img_path):
            os.mkdir(img_path)
        msg_type = item.get("type")
        if msg_type == 'img':
            with open(img_path + '/' + img_name, "wb") as f:
                f.write(img_byte)
                print("保存图片%s完成....ok" % img_name)
        elif msg_type == 'info':
            with open('豆瓣.csv', 'a', encoding='utf-8') as f:
                # 创建一个csv的DictWriter对象，这样才能够将写入csv格式数据到这个文件
                f_csv = csv.DictWriter(f, ['title', 'actor', 'time', 'grade', 'evaluate_num', 'quote'])
                # f_csv.writeheader()
                # 写入多行行（当做数据）
                item.pop("type")
                f_csv.writerows([item])
                print("保存信息到CSV....ok")
        # return item
