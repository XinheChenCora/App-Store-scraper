# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
import pymysql


class IosPipeline:

    def __init__(self):
        self.conn = pymysql.Connect(host='localhost', port=3306, user='****', password='******', database='*****',
                                    charset='utf8mb4')
        self.cursor = self.conn.cursor()
        # self.data=[]

    def close_spider(self, spider):
        self.conn.commit()
        self.conn.close()

    def process_item(self, item, spider):
        name = item.get('name', '')
        provider = item.get('provider', '')
        link = item.get('link', '')
        newlink = ','.join(link)
        linktype = item.get('linktype', '')
        newlinktype = ','.join(linktype)
        notlinkedtype = item.get('notlinkedtype', '')
        newnotlinkedtype = ','.join(notlinkedtype)
        tracktype = item.get('tracktype', '')
        newtracktype = ','.join(tracktype)
        rate = item.get('rate', '')
        size = item.get('size', '')
        price = item.get('price', '')
        # category = item.get('category', '')
        age = item.get('age', '')
        inpurchases = item.get('inpurchases', '')


        self.cursor.execute(
            'insert into utilities(name,provider,rate,size,price,age,inpurchases) values(%s,%s,%s,%s,%s,%s,%s)',
            (name,provider,rate,size,price,age,inpurchases)
        )

        self.cursor.execute(
            'update utilities set link =%s where name=%s',
            (newlink, name)
        )

        self.cursor.execute(
            'update utilities set linktype =%s where name=%s',
            (newlinktype, name)
        )

        self.cursor.execute(
            'update utilities set tracktype =%s where name=%s',
            (newtracktype, name)
        )

        self.cursor.execute(
            'update utilities set notlinkedtype =%s where name=%s',
            (newnotlinkedtype, name)
        )

        self.conn.commit()

        return item

    # def write_to_db(self):
    #     self.cursor.execute(
    #         'insert into book(name) values (%s)',
    #          name
    #     )
    #     self.conn.commit()
