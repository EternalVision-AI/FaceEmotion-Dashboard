from flask import Flask,render_template, request
import sqlite3
import os
from datetime import datetime, timedelta


app = Flask(__name__)
app.secret_key = os.urandom(24)


# Connect to the SQLite database (it will create the database if it doesn't exist)
conn = sqlite3.connect('emodb.db', check_same_thread=False)
curs = conn.cursor()

# Create the table if it doesn't exist
curs.execute('''
    CREATE TABLE IF NOT EXISTS emotable (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        gender TEXT NOT NULL,
        emotion TEXT NOT NULL,
        createddate TEXT NOT NULL
    )
''')

# Commit the table creation (and any other changes) and close the connection
conn.commit()


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

            return render_template('dashboard.html', data=[total, happy_rows, angry_rows, surprised_rows, disgusted_rows, neutral_rows, fear_rows, sad_rows])
    return render_template('login.html', error=error)

# Dashboard Data Page
@app.route("/emotion", methods=['GET', 'POST'])
def emotion():
    # print('request')
    # print(request.form)
    start_date = request.form.get('start_date','')
    end_date = request.form.get('end_date','')
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

    print(sql_query, params)
    curs.execute(sql_query, params)
    # Fetch all rows that match the query
    rows = curs.fetchall()
    print(start_date)
    # Displaying the fetched rows (for demonstration purposes)

    for row in rows:
        if start_date:
            if datetime.strptime(row[1], '%Y-%m-%d')>=datetime.strptime(start_date, '%Y-%m-%d') and datetime.strptime(row[1], '%Y-%m-%d')<=datetime.strptime(end_date, '%Y-%m-%d'):
                # print(row)
                # print(date)
                if row[0] == 'happy':
                    emotion_counts['happy'] += 1
                elif row[0] == 'angry':
                    emotion_counts['angry'] += 1
                elif row[0] == 'surprised':
                    emotion_counts['surprised'] += 1
                elif row[0] == 'disgusted':
                    emotion_counts['disgusted'] += 1
                elif row[0] == 'neutral':
                    emotion_counts['neutral'] += 1
                elif row[0] == 'fear':
                    emotion_counts['fear'] += 1
        elif date_period:
            date_x_days_ago = datetime.now() - timedelta(days=int(date_period))
            date_x_days_ago_str = date_x_days_ago.strftime('%Y-%m-%d')
            if datetime.strptime(row[1], '%Y-%m-%d')>=date_x_days_ago:
                # print(row)
                # print(date)
                if row[0] == 'happy':
                    emotion_counts['happy'] += 1
                elif row[0] == 'angry':
                    emotion_counts['angry'] += 1
                elif row[0] == 'surprised':
                    emotion_counts['surprised'] += 1
                elif row[0] == 'disgusted':
                    emotion_counts['disgusted'] += 1
                elif row[0] == 'neutral':
                    emotion_counts['neutral'] += 1
                elif row[0] == 'fear':
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
    return render_template('home.html')



if __name__ == "__main__":
    app.run(debug=True)
