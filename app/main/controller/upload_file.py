from app.main.controller import bp
import os
from flask import Flask, flash, request, redirect, url_for, render_template, current_app
from werkzeug.utils import secure_filename
import pandas as pd
import csv
import logging
from app.main.model.code_of_stock import code_stocks
from app.main.model.make_database_of_code import csv_file_to_sql
from app.main.service.time import run_on_time
from threading import Thread
import threading
from flask_apscheduler import APScheduler


ALLOWED_EXTENSIONS = {'csv'}
scheduler = APScheduler()
scheduler.init_app(bp)
scheduler.start()


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

@bp.route('/', methods=['GET', 'POST'])
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
            return redirect(url_for('main.data',
                                    filename=filename))
    return render_template('index.html', cache_timeout=0)


@bp.route('/data/<filename>', methods=['GET', 'POST'])
def data(filename):
    url_file_csv1 = os.path.join(current_app.config['UPLOAD_FOLDER'], filename)
    csv_file_to_sql(url_file_csv1)
    data = read_csv_file(url_file_csv1)
    code_stocks_news = code_stocks.query.all()
    def run_code_stock():
        run_on_time(code_stocks_news)
    def return_render():
        return render_template('data.html', cache_timeout=0, filename=filename,
                          code_stocks1 = code_stocks_news)
    t1 = threading.Thread(target=run_code_stock())
    t2 = threading.Thread(target=return_render())
    t1.start()
    t2.start()
    return1 = return_render()
    return return1
#    return render_template('data.html', cache_timeout=0, filename=filename, data = data.to_html(header=False, index=False))


