import MySQLdb

conn = MySQLdb.connect(host="127.0.0.1", user="root", password="1234", db="onlinelearning")
cursor = conn.cursor()
username = "'' or 1=1 #"
password = ""
sql = "select * from users_userprofile where username={} and password={}".format(username, password)

cursor.execute(sql)
for row in cursor.fetchall():
    print(row)