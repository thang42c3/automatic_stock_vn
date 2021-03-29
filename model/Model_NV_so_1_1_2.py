import json
import scrapy
from scrapy import cmdline
import csv
import os

# NHIỆM VỤ SỐ 1
if os.path.exists(r'..\file_csv\lich_su_gia_co_phieu.csv'):
    os.remove(r'..\file_csv\lich_su_gia_co_phieu.csv')
fields = ['STT',
          'Ma_cty',
          'Ngay',
          'Gia_tham_chieu',
          'Len_xuong',
          'Phan_tram',
          'Dong_cua',
          'Khoi_luong',
          'Mo_cua',
          'Cao_nhat',
          'Thap_nhat',
          'Giao_dich_thoa_thuan',
          'Nuoc_ngoai_mua',
          'Nuoc_ngoai_ban']

with open(r'..\file_csv\lich_su_gia_co_phieu.csv', 'a') as f:
    write = csv.writer(f)
    write.writerow(fields)


class CpSpider(scrapy.Spider):
    name = 'cp_item'
    start_urls = ['https://www.cophieu68.vn/historyprice.php?currentPage=1&id=pan']
    #for i in range(1, 72):
        #   start_urls.append('https://www.cophieu68.vn/historyprice.php?currentPage={0}&id={1}'.format(i, Ten_cty))
    def parse(self, response):
        rows = []
        for table in response.css('table.stock'):
            for j in range (2, 51):
                record = [ table.xpath('tr[{0}]/td[1]/text()'.format(j)).get(),
                    'PAN',
                    table.xpath('tr[{0}]/td[2]/text()'.format(j)).get(),
                    table.xpath('tr[{0}]/td[3]/text()'.format(j)).get(),
                    table.xpath('tr[{0}]/td[4]/span[1]/text()'.format(j)).get(),
                    table.xpath('tr[{0}]/td[5]/span[1]/text()'.format(j)).get(),
                    table.xpath('tr[{0}]/td[6]/span[1]/strong[1]/text()'.format(j)).get(),
                    table.xpath('tr[{0}]/td[7]/text()'.format(j)).get(),
                    table.xpath('tr[{0}]/td[8]/span[1]/text()'.format(j)).get(),
                    table.xpath('tr[{0}]/td[9]/span[1]/text()'.format(j)).get(),
                    table.xpath('tr[{0}]/td[10]/span[1]/text()'.format(j)).get(),
                    table.xpath('tr[{0}]/td[11]/text()'.format(j)).get(),
                    table.xpath('tr[{0}]/td[12]/text()'.format(j)).get(),
                    table.xpath('tr[{0}]/td[13]/text()'.format(j)).get()
            ]
                if record[3] is not None:
                    rows.append(record)
        Page = response.xpath("//ul[@id='navigator']/li[9]/a[1]/@href").get()
        if Page is not None:
            next_page = response.xpath("//ul[@id='navigator']/li[9]/a[1]/@href").get()
        elif response.xpath("//ul[@id='navigator']/li[6]/span[1]/text()").get() == "70":
            next_page = response.xpath("//ul[@id='navigator']/li[7]/a[1]/@href").get()
        elif response.xpath("//ul[@id='navigator']/li[7]/span[1]/text()").get() == "71":
            next_page = None
        else:
            next_page = response.xpath("//ul[@id='navigator']/li[6]/a[1]/@href").get()
        if next_page is not None:
            yield response.follow(next_page, self.parse)


        with open(r'..\file_csv\lich_su_gia_co_phieu.csv', 'a') as f:
            write = csv.writer(f)
            write.writerows(rows)


cmdline.execute("scrapy runspider Model_NV_so_1.py".split())







