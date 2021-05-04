from app import db
from app import create_app
import logging
logging.basicConfig(level=logging.DEBUG)

app = create_app()
app.app_context().push()

db.metadata.clear()
#logging.debug(db)

class code_stocks(db.Model):
    with app.app_context():
        id = db.Column('id', db.Integer, primary_key = True)
        symbol = db.Column(db.String(30))
        volume = db.Column(db.String(30))
        trading = db.Column(db.String(10))
        date = db.Column(db.String(10))
        time = db.Column(db.String(30))

def __init__(self, symbol, volume, trading, date, time):
     self.symbol = symbol
     self.volume = volume
     self.trading = trading
     self.date = date
     self.time = time



#db.metadata.clear()
db.create_all()
