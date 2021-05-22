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
