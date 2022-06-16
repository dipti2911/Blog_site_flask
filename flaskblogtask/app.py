from flask import Flask, render_template, flash, request, redirect, session,url_for
from flask_bootstrap import Bootstrap
import sqlite3,os
from werkzeug.utils import secure_filename
#from werkzeug.security import generate_password_hash,check_password_hash
app = Flask(__name__)
Bootstrap(app)
@app.route("/")
def index():
    con = sqlite3.connect("mydb3.db")

    cur = con.cursor()
    cur.execute("SELECT * from blog")

    data = cur.fetchall()

    return  render_template('index.html',data=data)


@app.route("/about")
def about():
    return render_template("about.html")

"""@app.route("/blogs/<int:blog_id>/")
def blogs(blog_id):
    con = sqlite3.connect("mydb2.db")
    cur = con.cursor()
    resultvalue=cur.execute("Select * from blogs where blog_id=?",[blog_id])
    if len(resultvalue)>0:
        blogs=cur.fetchall()
        return render_template("blogs.html", blogs=blogs)
    return "Blog not found"""

app.secret_key="abcd"


@app.route("/register",methods=["GET","POST"])
def register():
    if request.method=="POST":
        fname = request.form["fname"]
        lname = request.form["lname"]
        uname = request.form['uname']
        email = request.form["email"]
        pass1 = request.form["pass1"]

        #userDetails=request.form
        if request.form["pass1"] !=request.form["cpass1"]:
            flash('Password do not match! Try again.','danger')
            return render_template('register.html')

        con = sqlite3.connect("mydb3.db")
        cur = con.cursor()



        cur.execute("insert into users(fname,lname,uname,email,pass1)values(?,?,?,?,?)", (fname, lname,uname, email,pass1))
        con.commit()
        flash("Registration success! Please Login",'success')
        return redirect(url_for('login'))
    return render_template('register.html')



@app.route("/login",methods=["GET","POST"])
def login():
    if request.method == "POST":
            un = request.form['uname']
            pw = request.form['pass1']
            con = sqlite3.connect("mydb3.db")

            cur = con.cursor()
            cur.execute("SELECT * from users where uname=? and pass1=?", (un, pw))

            data = cur.fetchall()
            if len(data) == 1:
                session["username"] = un
                session["password"] = pw # session start
                return render_template("base.html")
            else:
                flash("Please enter valid password and username")
                return redirect(url_for("login"))
    return render_template("login.html")


@app.route("/write_blog",methods=["GET","POST"])
def write_blog():
    if request.method=="POST":
        title = request.form['title']
        pname = request.form['pname']
        desc = request.form['desc']
        con = sqlite3.connect("mydb3.db")
        cur = con.cursor()
        cur.execute("insert into blog(title,pname,desc)values(?,?,?)", (title, pname, desc))
        con.commit()
        flash("successfully posted! new blog", 'success')
        return redirect(url_for("View_blog"))
    return render_template('write_blog.html')


UPLOAD_FOLDER = 'static/upload/'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024

ALLOWED_EXTENSIONS = set(['png', 'jpg', 'jpeg', 'gif'])


def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS







@app.route("/write_blog")
def file():
    return  render_template("write_blog.html")
@app.route("/file_upload",methods=["POST","GET"])
def file_upload():
    if request.method=="POST":
        f=request.files['photo']
        f.save(f.filename)
        f.filename
        f.save(os.path.join(app.config["UPLOAD_FOLDER"],f.filename))

        return "File uploaded syccessfully"
    else:
        return "fail"





@app.route("/View_blog")
def View_blog():

        con=sqlite3.connect("mydb3.db")

        cur=con.cursor()
        cur.execute("SELECT * from blog")

        data=cur.fetchall()

        return  render_template("view_blog.html",data=data)





@app.route("/edit_blog/<int:blog_id>")
def edit_blog(blog_id):
        con = sqlite3.connect("mydb3.db")
        cur = con.cursor()

        cur.execute("select * from blog where blog_id=?",[blog_id])
        data = cur.fetchall()
        return render_template("edit_blog.html", data=data)


@app.route("/update", methods=["POST", "GET"])
def update():
    if request.method == "POST":
        blog_id = request.form["blog_id"]
        title = request.form["title"]
        pname = request.form["pname"]
        desc = request.form["desc"]

        con = sqlite3.connect("mydb3.db")
        cur = con.cursor()
        cur.execute("update blog set title=?, pname=?, desc=? where blog_id=?", (title, pname,desc,blog_id))

        con.commit()
        return redirect(url_for("View_blog"))


# update part end


@app.route("/delete/<int:blog_id>")
def delete(blog_id):
    con=sqlite3.connect("mydb3.db")
    cur=con.cursor()
    cur.execute("delete from blog where blog_id=?",[blog_id])
    con.commit()
    return redirect(url_for("View_blog"))

app.config["UPLOAD_FOLDER"]="C:/Users/Owner/PycharmProjects/PythonFortunecloud/flaskblogtask/image"





@app.route("/logout",methods=["POST"])
def logout():
    session.pop("username",None)#session end
    flash("Successfully Log Out")
    return redirect(url_for("login"))


if __name__=="__main__":
    app.run(debug=True)