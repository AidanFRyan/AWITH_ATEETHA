import mysql.connector as sql
db = sql.connect(host='localhost', user='pi', passwd='pi')
cur = db.cursor()
cur.execute("CREATE DATABASE testbase")
cur.execute("CREATE TABLE Item(name VARCHAR(20), price INTEGER, date DATE, mID INTEGER, username VARCHAR(20), PRIMARY KEY (name, username, date))")
cur.execute("CREATE TABLE User(username VARCHAR(20), numTrades INTEGER, PRIMARY KEY (name))")
cur.execute("CREATE TABLE Manufacturer(mID INTEGER, mName VARCHAR(20), PRIMARY KEY (mID))")