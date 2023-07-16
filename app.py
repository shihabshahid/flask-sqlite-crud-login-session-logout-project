from flask import Flask,render_template,request,redirect,url_for,flash,session
import sqlite3 as sql
app = Flask(__name__)

@app.route('/',methods=['POST','GET'])
@app.route('/login',methods=['POST','GET'])
def login():
    if request.method=='POST':
        name = request.form['name']
        password = request.form['password']
        con=sql.connect("user_db.db")
        cur=con.cursor()
        cur.execute("select name,password from admin where name=? and password=?",[name,password])
        data=cur.fetchone()
        if data is not None:
            session['name']=name
            return redirect(url_for("retrieve"))
        else:
            flash('name or password not mached','warning')
            return render_template('login.html')
    return render_template('login.html')

@app.route('/logout')
def logout():
    session.pop('name',None)
    return redirect(url_for('login'))

@app.route('/retrieve')
def retrieve():
    if 'name' in session:
        con=sql.connect("user_db.db")
        con.row_factory=sql.Row
        cur=con.cursor()
        cur.execute("select * from user_table")
        data=cur.fetchall()
        return render_template('retrieve.html',datas=data)
    else:
        flash('access this need to login first','warning')
        return render_template('login.html')
    

@app.route('/create',methods=['POST','GET'])
def create():
    if 'name' in session:
        if request.method=='POST':
            name=request.form['name']
            contact=request.form['contact']
            con=sql.connect("user_db.db")
            cur=con.cursor()
            cur.execute("insert into user_table(name,contact) values(?,?)",[name,contact])
            con.commit()
            flash('Data Saved','success')
            return redirect(url_for("retrieve"))
        return render_template('create.html')
    else:
        flash('access this need to login first','warning')
        return render_template('login.html')

@app.route('/update/<string:id>',methods=['POST','GET'])
def update(id):
    if 'name' in session:
        con=sql.connect("user_db.db")
        con.row_factory=sql.Row
        cur=con.cursor()
        cur.execute("select * from user_table where id=?",[id])
        data=cur.fetchone()
        if request.method=='POST':
            name=request.form['name']
            contact=request.form['contact']
            con=sql.connect("user_db.db")
            cur=con.cursor()
            cur.execute("update user_table set name=?,contact=? where id=?",[name,contact,id])
            con.commit()
            flash('Data updated','success')
            return redirect(url_for("retrieve"))
        return render_template('update.html',datas=data)
    else:
        flash('access this need to login first','warning')
        return render_template('login.html')

@app.route('/delete/<string:id>',methods=['GET'])
def delete(id):
    if 'name' in session:
        con=sql.connect("user_db.db")
        con.row_factory=sql.Row
        cur=con.cursor()
        cur.execute("delete from user_table where id=?",[id])
        con.commit()
        flash('Data Deleted','warning')
        return redirect(url_for("retrieve"))
    else:
        flash('access this need to login first','warning')
        return render_template('login.html')

if __name__ =='__main__':
    app.secret_key='admin123'
    app.run(debug=True)
