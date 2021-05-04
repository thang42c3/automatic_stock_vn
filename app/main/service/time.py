import schedule
import time
from datetime import datetime
from app.main.service.fill_form_stock import fill_form_stock
from app.main.model.code_of_stock import code_stocks
import datetime, schedule, requests
import threading


def run_on_time(code_stock_news):

    def job(symbol1, volume1, trading1, time1):
        date = datetime.datetime.now().strftime("%d.%m.%Y %H:%M:%S")
        runTime = time1
        print(date)
        print(runTime)
        date_to_real = datetime.datetime.strptime(date, "%d.%m.%Y %H:%M:%S")
        runTime_to_real = datetime.datetime.strptime(runTime, "%d.%m.%Y %H:%M:%S")
        if date_to_real <= runTime_to_real:
            print(date_to_real-runTime_to_real)
            if date == str(runTime):
                print("OKKKKKKKKKKKKKKKKKKKKKKKKKKKK")
                fill_form_stock(symbol1, volume1, trading1)
        return schedule.CancelJob

    def run_threaded(job_func):
        job_thread = threading.Thread(target=job_func)
        job_thread.start()


    for code_stock_new in code_stock_news:
        symbol1 = code_stock_new.symbol
        print(symbol1)
        print('me nha no')
        volume1 = code_stock_new.volume
        trading1 = code_stock_new.trading
        time1 = code_stock_new.date.replace("/", ".") + " " + code_stock_new.time
        date = datetime.datetime.now().strftime("%d.%m.%Y %H:%M:%S")

        schedule.every(0.01).minutes.until(datetime.datetime.strptime(time1, "%d.%m.%Y %H:%M:%S")+datetime.timedelta(0,10)).do(run_threaded, lambda : job(symbol1, volume1, trading1, time1))


        while True:
            schedule.run_all()
            time.sleep(1)
        continue