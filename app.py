import mysql.connector
from flask import Flask, render_template, request, redirect, url_for, session
import hashlib
from scanner import nmap_version_scan

app = Flask(__name__)

mydb = mysql.connector.connect(
    host="localhost",
    user="root",
    password="kali",
    database="Testip"
)

# Set a secret key for the session
app.secret_key = 'your_secret_key'


@app.route('/login', methods=['GET', 'POST'])
def login():
    # Output message if something goes wrong...
    msg = ''
    if request.method == 'POST' and 'username' in request.form and 'password' in request.form:
        # Create variables for easy access
        username = request.form['username']
        password = request.form['password']
        params = (username, password)
        print(params)
        # Retrieve the hashed password
        hash = password + app.secret_key
        hash = hashlib.sha1(hash.encode())
        password = hash.hexdigest()
        cursor = mydb.cursor()
        query = 'SELECT * FROM accounts WHERE username = %s AND password = %s'
        cursor.execute(query, params)
        account = cursor.fetchone()
        print(account)
        if account:
            # Create session data, we can access this data in other routes
            session['loggedin'] = True
            session['id'] = account[0]
            # session['username'] = account[0]
            print('logged')
            return redirect(url_for('index'))
        else:
            msg = 'Incorrect username/password!'
            print(msg)
    return render_template('loginForm.html', msg='')


@app.route('/login/index', methods=["GET", "POST"])
def index():
    if 'loggedin' in session:
        cur = mydb.cursor()
        cur.execute("SELECT * FROM scan_results")
        scans = cur.fetchall()
        print(scans)
        cur.close()
        return render_template('index.html', scans=scans)


def gfg():
    if request.method == "POST":
        ip = request.form['ip']
        print(ip)
        nmap_version_scan(ip)
        return ip
    return redirect(url_for('login'))


if __name__ == '__main__':
    app.run(debug=True)
