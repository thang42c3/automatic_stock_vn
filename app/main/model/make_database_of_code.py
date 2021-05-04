import logging
logging.basicConfig(level=logging.DEBUG)
from app import db
from app.main.model.code_of_stock import code_stocks
import csv

#db.create_all()
#db.session.query(ma_co_phieus).delete()
#db.session.commit()


def csv_file_to_sql(url_file_csv):
    db.session.query(code_stocks).delete()
    db.session.commit()
    with open(url_file_csv, mode='r') as csv_file:
        csv_reader = csv.reader(csv_file)
        line_count = 0
        i = 0
        for row in csv_reader:
            if i != 0:
                symbol = row[0]
                volume = row[1]
                trading = row[2]
                date = row[3]
                time = row[4]
                print(symbol)
                code_stock = code_stocks(symbol = symbol, volume=volume, trading=trading, date=date, time=time)
#                logging.debug(symbol)
#                logging.debug(volume)
                db.session.add(code_stock)
                db.session.commit()
            i += 1



  
'''

class CpSpider(scrapy.Spider):
    name = 'companylist'
    start_urls = ['https://www.cophieu68.vn/companylist.php']

    #for i in range(1, 72):
        #   start_urls.append('https://www.cophieu68.vn/historyprice.php?currentPage={0}&id={1}'.format(i, Ten_cty))
    def parse(self, response):
        for table in response.css('tbody#fred'):
            for j in range (2, 28):
                name = table.xpath('tr[{0}]/td[3]/text()'.format(j)).get()
                name = str(name).strip()
                code = table.xpath('tr[{0}]/td[2]/a[1]/strong[1]/text()'.format(j)).get()
                if code is not None:
                    ma_co_phieu = ma_co_phieus(name=name, code=code)
                    logging.debug(name)
                    logging.debug(code)
                    db.session.add(ma_co_phieu)
                    db.session.commit()

        Page = response.xpath("//ul[@id='navigator']/li[9]/a[1]/@href").get()
        logging.debug(Page)
        if Page is not None:
            next_page = response.xpath("//ul[@id='navigator']/li[9]/a[1]/@href").get()
            logging.debug(next_page)
        elif response.xpath("//ul[@id='navigator']/li[6]/a[1]/text()").get() == ">":
            next_page = response.xpath("//ul[@id='navigator']/li[6]/a[1]/@href").get()
            logging.debug(next_page)
        elif response.xpath("//ul[@id='navigator']/li[7]/a[1]/@href").get() is not None:
            next_page = response.xpath("//ul[@id='navigator']/li[7]/a[1]/@href").get()
            logging.debug(next_page)
        else:
            next_page = None
        if next_page is not None:
            yield response.follow(next_page, self.parse)



#        with open(r'.\file_csv\lich_su_gia_co_phieu.csv', 'a') as f:
#            write = csv.writer(f)
#            write.writerows(rows)


cmdline.execute("scrapy runspider make_database_of_code.py".split())
'''
