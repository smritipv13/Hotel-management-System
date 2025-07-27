from flask import Flask,render_template
import mysql.connector

app=Flask(__name__)

db=mysql.connector.connect(
    host="127.0.0.1",
    user="root",
    password="root",
    port=3306,
    database="hotel_management"
)

print("trying to connect to the db...")
if db.is_connected():
    print("successfully connected to your mysql database")
else:
    print("connection failed")


@app.route('/')
def home():
    return "WELCOME TO HOTEL MANAGEMENT SYSTEM!"
@app.route('/hi')
def home1():
    return render_template('index.html')

if __name__=="__main__":
    app.run(debug=True)

