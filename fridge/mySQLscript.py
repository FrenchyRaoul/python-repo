#!/usr/bin/python
import MySQLdb
import datetime

db = MySQLdb.connect(host="192.168.1.138",
			 user="pi",
			passwd="raspberry",
			db="beer")
db.autocommit(True)

cur = db.cursor()
time = datetime.datetime.now()

year = time.year
month = time.month
day = time.day
hour = time.hour
minute = time.minute
second = time.second

temp = 60



sql = "INSERT INTO temperature (year,month,day,hour,minute,second,temperature) VALUES ('%s','%s','%s','%s','%s','%s','%s')" % (year,month,day,hour,minute,second,temp)
cur.execute(sql)

#sql = ("SELECT * FROM temperature")
#cur.execute(sql)

for row in cur.fetchall():
	print row[4]
