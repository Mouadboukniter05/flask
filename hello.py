from flask import Flask
from flask import render_template
from flask import request
from flask import session
from flask import abort, redirect, url_for
from werkzeug.utils import secure_filename
from flask_mysqldb import MySQL
import MySQLdb.cursors

app = Flask(__name__)
app.secret_key = b'_5#y2L"F4Q8z\n\xec]/'
app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = ''
app.config['MYSQL_DB'] = 'flask'

mysql = MySQL(app)


@app.get("/")
def hello_world():
    return render_template('hello.html', test='user' in session)


@app.get("/login")
def login_get():
    if 'user' in session:
        return redirect(url_for('listFile'))
    error = request.args.get('error', default=None)
    return render_template('login.html', error=error)


@app.post('/login')
def login_post():
    if 'user' in session:
        return redirect(url_for('listFile'))
    cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
    cursor.execute(
        ''' select * from users where email like %s and password like %s''', (request.form['email'], request.form['password']))
    data = cursor.fetchall()
    if not data:
        return redirect(url_for('login_get', error="email or password is incorect"))
    session['user'] = data[0]
    return redirect(url_for('listFile'))


# apres auth ----------------------

@app.route('/logout')
def logout():
    if 'user' not in session:
        return redirect(url_for('login_get'))
    session.pop('user', None)
    return redirect(url_for('login_get'))


@app.get("/get/files")
def listFile():
    if 'user' not in session:
        return redirect(url_for('login_get'))
    getlist = [{"file_name": "156dfd5145f4"}, {
        "file_name": "157dfd5145f5"}, {"file_name": "156dfd5145f4"}]
    return render_template('les_fichiers.html', getlist=getlist, user=session["user"])


@app.get("/uploadFile")
def uploadFileView():
    if 'user' not in session:
        return redirect(url_for('login_get'))
    return render_template('upload.html', user=session["user"])


@app.post("/uploadFile")
def uploadFile():
    if 'user' not in session:
        return redirect(url_for('login_get'))
    f = request.files['the_file']
    f.save(f'./testUploads/{secure_filename(f.filename)}')
    getlist = [{"file_name": "156dfd5145f4"}, {
        "file_name": "157dfd5145f5"}, {"file_name": "156dfd5145f4"}]
    return render_template('les_fichiers.html', getlist=getlist)
# apres auth ---------------------
