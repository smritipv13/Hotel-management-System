import mysql.connector
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

def check(name,password,db):

    cur=db.cursor()
    cur.execute("select * from customers where name=%s and passkey=%s",(name,password))

    s=cur.fetchall()
    print(s)
    print(len(s))
check('aditya','ad23',db)
check('smriti','sm04',db)
check('smriti','sm04',db)

def insertcustomer(name,email_id,phone_no,passkey,address,db):
    cur=db.cursor()
    cur.execute("""
    INSERT INTO customers (name, email_id, phone_no, passkey, address)
    VALUES (%s, %s, %s, %s, %s)
""", (name, email_id, phone_no, passkey, address))
    db.commit()
    

insertcustomer("smriti", "smritipv13@gmail.com", 7795884780,"sm04","bsk stage 1,bangalore",db)
insertcustomer("rohit","rohit1vasishta@gmail.com",9591625019,"rohit1","montreal,canada",db)
insertcustomer("anvi","anvikumar@gmail.com",8073465065,"anvi05","bannarghetha,bangalore",db)

def updateemail(pemail,nemail,db):
    cur=db.cursor()
    cur.execute("update customers set email_id=%s where email_id=%s",(pemail,nemail))
    db.commit()
updateemail("smritip13@gmail.com","smritipv13@gmail.com",db)

def updatephoneno(pphone,nphone,db):
    cur=db.cursor()
    cur.execute("update customers set phone_no=%s where phone_no=%s",(pphone,nphone))
    db.commit()
updatephoneno(7795884789,7795884780,db)

