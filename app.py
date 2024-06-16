from flask import Flask,render_template, request, make_response, Response, redirect
import json
from werkzeug.utils import secure_filename
from time import time
import sqlite3
from twilio.rest import Client
import csv
import xlwt
from flask_mail import Mail, Message
import io
import os
import threading
from plyer import notification
from datetime import date, datetime
from Adafruit_IO import RequestError, Client, Feed
from playsound import playsound 
from datetime import datetime, timedelta

UPLOAD_FOLDER = 'C:/Users/Dell/Desktop/XYMA/static/uploads/'

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.secret_key = os.urandom(24)


# SQLite3 Connection
conn = sqlite3.connect('emodb.db', check_same_thread=False)
curs = conn.cursor()


# Error Handling
@app.errorhandler(404)
def error(error):
    return render_template('error.html'), 404

#Home Page
@app.route('/')
def main():
    return render_template('home.html')

#Login Page
@app.route('/login', methods=['GET', 'POST'])
def login():
    error = ""
    if request.method == 'POST':
        if request.form['username'] != 'Admin' or request.form['password'] != 'admin' or request.form['api'] != '111':
            error = 'Invalid Credentials. Please try again.'
        else:
            sql_query = "SELECT * FROM emotable WHERE emotion='happy'"
            params = []
            curs.execute(sql_query, params)
            happy_rows = len(curs.fetchall())
            sql_query = "SELECT * FROM emotable WHERE emotion='angry'"
            params = []
            curs.execute(sql_query, params)
            angry_rows = len(curs.fetchall())
            sql_query = "SELECT * FROM emotable WHERE emotion='surprised'"
            params = []
            curs.execute(sql_query, params)
            surprised_rows = len(curs.fetchall())
            sql_query = "SELECT * FROM emotable WHERE emotion='disgusted'"
            params = []
            curs.execute(sql_query, params)
            disgusted_rows = len(curs.fetchall())
            sql_query = "SELECT * FROM emotable WHERE emotion='neutral'"
            params = []
            curs.execute(sql_query, params)
            neutral_rows = len(curs.fetchall())
            sql_query = "SELECT * FROM emotable WHERE emotion='fear'"
            params = []
            curs.execute(sql_query, params)
            fear_rows = len(curs.fetchall())
            sql_query = "SELECT * FROM emotable WHERE emotion='sad'"
            params = []
            curs.execute(sql_query, params)
            sad_rows = len(curs.fetchall())

            total=happy_rows+angry_rows+surprised_rows+disgusted_rows+neutral_rows+fear_rows+sad_rows

            return render_template('index.html', data=[total, happy_rows, angry_rows, surprised_rows, disgusted_rows, neutral_rows, fear_rows, sad_rows])
    return render_template('login.html', error=error)

# Dashboard Data Page
@app.route("/emotion", methods=['GET', 'POST'])
def emotion():
    # print('request')
    # print(request.form)
    date = request.form.get('date', '')
    gender = request.form.get('gender', 'all')
    date_period = request.form.get('date_period', 'all')
    
    # Build SQL query with WHERE clause based on form inputs
    sql_query = "SELECT emotion, createddate FROM emotable WHERE 1=1"
    params = []
    emotions = ['happy', 'angry', 'surprised', 'disgusted', 'neutral', 'fear', 'sad']
    emotion_counts = {'happy': 0, 'angry': 0, 'surprised': 0, 'disgusted': 0, 'neutral': 0, 'fear': 0, 'sad': 0}
    # if date != '':
    #     sql_query += " AND strftime('%Y-%m-%d',createddate) = ?"
    #     params.append(date)

    if gender != 'all':
        sql_query += " AND gender = ?" 
        params.append(gender)

    # if date_period != 0:
    #     date_x_days_ago = datetime.now() - timedelta(days=int(date_period))
    #     date_x_days_ago_str = date_x_days_ago.strftime('%Y-%m-%d')
    #     sql_query += " AND datetime.strftime('%Y-%m-%d',createddate) >= ?"
    #     params.append(date_x_days_ago_str)

    print(sql_query, params)
    curs.execute(sql_query, params)

   
    # Fetch all rows that match the query
    rows = curs.fetchall()
    print(len(rows))
    # Displaying the fetched rows (for demonstration purposes)

    for row in rows:
        if date:
            if datetime.strptime(row[1], '%Y-%m-%d')==datetime.strptime(date, '%Y-%m-%d'):
                print(row)
                # print(date)
                if row[0] == 'happy':
                    # Handle case 1
                    emotion_counts['happy'] += 1
                elif row[0] == 'angry':
                    # Handle case 1
                    emotion_counts['angry'] += 1
                elif row[0] == 'surprised':
                    # Handle case 1
                    emotion_counts['surprised'] += 1
                elif row[0] == 'disgusted':
                    # Handle case 1
                    emotion_counts['disgusted'] += 1
                elif row[0] == 'neutral':
                    # Handle case 1
                    emotion_counts['neutral'] += 1
                elif row[0] == 'fear':
                    # Handle case 1
                    emotion_counts['fear'] += 1
        elif date_period:
            date_x_days_ago = datetime.now() - timedelta(days=int(date_period))
            date_x_days_ago_str = date_x_days_ago.strftime('%Y-%m-%d')
            if datetime.strptime(row[1], '%Y-%m-%d')>=date_x_days_ago:
                print(row)
                # print(date)
                if row[0] == 'happy':
                    # Handle case 1
                    emotion_counts['happy'] += 1
                elif row[0] == 'angry':
                    # Handle case 1
                    emotion_counts['angry'] += 1
                elif row[0] == 'surprised':
                    # Handle case 1
                    emotion_counts['surprised'] += 1
                elif row[0] == 'disgusted':
                    # Handle case 1
                    emotion_counts['disgusted'] += 1
                elif row[0] == 'neutral':
                    # Handle case 1
                    emotion_counts['neutral'] += 1
                elif row[0] == 'fear':
                    # Handle case 1
                    emotion_counts['fear'] += 1
        else :
            if row[0] == 'happy':
                    # Handle case 1
                    emotion_counts['happy'] += 1
            elif row[0] == 'angry':
                # Handle case 1
                emotion_counts['angry'] += 1
            elif row[0] == 'surprised':
                # Handle case 1
                emotion_counts['surprised'] += 1
            elif row[0] == 'disgusted':
                # Handle case 1
                emotion_counts['disgusted'] += 1
            elif row[0] == 'neutral':
                # Handle case 1
                emotion_counts['neutral'] += 1
            elif row[0] == 'fear':
                # Handle case 1
                emotion_counts['fear'] += 1
    
    all_emotions=0
    for emotion in emotion_counts:
        all_emotions+=emotion_counts[emotion]
    # return [all_emotions]
    return [all_emotions, emotion_counts['happy'], emotion_counts['angry'], emotion_counts['surprised'], emotion_counts['disgusted'], emotion_counts['neutral'], emotion_counts['fear']]

    

#Dashbaord Page
@app.route('/home', methods=["GET", "POST"])
def home():
    return render_template('index.html')

# Send Email
@app.route("/send_email")
def send_email():
    mail_settings = {
        "MAIL_SERVER": 'smtp.gmail.com',
        "MAIL_PORT": 465,
        "MAIL_USE_TLS": False,
        "MAIL_USE_SSL": True,
        "MAIL_USERNAME": 'EMAIL_ID',
        "MAIL_PASSWORD": 'PASSWORD'
    }

    app.config.update(mail_settings)
    mail = Mail(app)
    with app.app_context():
        msg = Message(subject="Mail from ARMS-Raspi",
                      sender=app.config.get("MAIL_USERNAME"),
                      recipients=["RECEIVER_MAIL_ID"],
                      body="Temp value is High")
        mail.send(msg)
    email_success = "Succesfull"
    return render_template('report.html', email_success=email_success)

# Download Report Excel Format
@app.route("/download/excel")
def download_report():
    conn = sqlite3.connect('emodb.db', check_same_thread=False)
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM emotable")
    result = cursor.fetchall()

    #output in bytes
    output = io.BytesIO()
    # create WorkBook object
    workbook = xlwt.Workbook()
    # add a sheet
    sh = workbook.add_sheet('Data')

    # add headers
    sh.write(0, 0, 'Time Stamp')
    sh.write(0, 1, 'Temperature')
    sh.write(0, 2, 'Humidity')

    idx = 0
    for row in result:
        time = str(row[0])
        temp = row[1]
        hum = row[2]
        sh.write(idx+1, 0, time)
        sh.write(idx+1, 1, temp)
        sh.write(idx+1, 2, hum)
        idx += 1

    workbook.save(output)
    output.seek(0)

    return Response(output, mimetype="application/ms-excel", headers={"Content-Disposition": "attachment;filename=data.xls"})


# Download Report CSV Format
@app.route("/download/csv")
def download_csv():
    conn = sqlite3.connect('eomdb.db', check_same_thread=False)
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM emotable")
    result = cursor.fetchall()
    output = io.StringIO()
    writer = csv.writer(output)

    line = ['Timestamp, Temperature, Humidity']
    # writer.writerow(line)
    for row in result:
        time = str(row[0])
        temp = str(row[1])
        hum = str(row[2])
        line = [time + ',' + temp + ',' + hum]
        writer.writerow(line)
    output.seek(0)
    return Response(output, mimetype="text/csv", headers={"Content-Disposition": "attachment;filename=data.csv"})

if __name__ == "__main__":
    app.run(debug=True)
