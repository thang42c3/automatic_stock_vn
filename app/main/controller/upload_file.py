import os
from flask import Flask, flash, request, redirect, url_for, render_template, current_app
from werkzeug.utils import secure_filename
import pandas as pd
import csv
import logging
from app.main.model.code_of_stock import code_stocks
from app.main.model.make_database_of_code import csv_file_to_sql
import threading
from app.main.service.fill_form_stock import fill_form_stock1
from apscheduler.schedulers.background import BackgroundScheduler
from config.config import configs
from app import app
config = configs()
from flask_apscheduler import APScheduler
'''
Đầu vào: Dữ liệu các mã cổ phiếu.
Đầu ra: Các file excell được download trực tiếp từ website ứng với từng mã"
'''

schedule = BackgroundScheduler()
scheduler = APScheduler()
scheduler.init_app(app)
scheduler.start()

ALLOWED_EXTENSIONS = {'csv'}


def read_csv_file(url_file_csv):
    data = []
    with open(url_file_csv, mode='r') as csv_file:
        csv_reader = csv.reader(csv_file)
        line_count = 0
        print(csv_reader)
        for row in csv_reader:
            data.append(row)
            line_count += 1
        data = pd.DataFrame(data)
    return data

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS



@app.route('/', methods=['GET', 'POST'])
def upload_file():
    if request.method == 'POST':
        # check if the post request has the file part
        if 'file' not in request.files:
            flash('No file part')
            return redirect(request.url)
        file = request.files['file']
        # if user does not select file, browser also
        # submit an empty part without filename
        if file.filename == '':
            flash('No selected file')
            return redirect(request.url)
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            logging.warning(filename)
            file.save(os.path.join(current_app.config['UPLOAD_FOLDER'], filename))
            url_file_csv = os.path.join(current_app.config['UPLOAD_FOLDER'], filename)
            return redirect(url_for('data',
                                    filename=filename))
    return render_template('index.html', cache_timeout=0)


@app.route('/data/<filename>', methods=['GET', 'POST'])
def data(filename):
    url_file_csv1 = os.path.join(current_app.config['UPLOAD_FOLDER'], filename)
    csv_file_to_sql(url_file_csv1)
    data = read_csv_file(url_file_csv1)
    code_stocks_news = code_stocks.query.all()
    i = 0
    for code_stock_new in code_stocks_news:
        symbol1 = code_stock_new.symbol
        print(symbol1)
        volume1 = code_stock_new.volume
        trading1 = code_stock_new.trading
        date = code_stock_new.date.split("/")
        time1 = code_stock_new.time.split(":")
        print((int(date[2]), int(date[1]), int(date[0]), int(time1[0]), int(time1[1]),
                                           int(time1[2])))
        datetime1 = date[2] + "-" + date[1] + "-" + date[0] + " " + time1[0] + ":" + time1[1] + ":" + time1[2]


        scheduler.add_job(func=fill_form_stock1,
                         trigger='date',
                         run_date= datetime1,
                         args=[symbol1, volume1, trading1],
                          id = "t{0}".format(i))
        i = i + 1
    def return_render():
        return render_template('data.html', cache_timeout=0, filename=filename,
                          code_stocks1 = code_stocks_news)
#    t2 = threading.Thread(target=return_render())
#    t2.start()
    return1 = return_render()
    return return1



