import sqlite3

conn = sqlite3.connect('/DB/music.db')
print "Opened database successfully";

conn.close()