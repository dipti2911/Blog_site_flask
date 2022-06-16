import  sqlite3
con= sqlite3.connect("mydb3.db")
cur=con.cursor()
cur.execute("create table users(id INTEGER PRIMARY KEY AUTOINCREMENT,fname TEXT, lname TEXT,uname TEXT,email TEXT,pass1 TEXT)")
cur.execute("create table blog(blog_id INTEGER PRIMARY KEY AUTOINCREMENT,title TEXT,pname TEXT,desc TEXT)")

con.commit()
con.close()