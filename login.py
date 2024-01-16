from flask import Flask, request, session, redirect, url_for
from flask_mysqldb import MySQL

app = Flask(__name__)

# MySQL configuration
app.config['MYSQL_USER'] = 'your_mysql_username'
app.config['MYSQL_PASSWORD'] = 'your_mysql_password'
app.config['MYSQL_DB'] = 'flask_auth'
app.config['MYSQL_CURSORCLASS'] = 'DictCursor'

# Initialize MySQL
mysql = MySQL(app)

# Set a secret key for the session
app.secret_key = 'your_secret_key'


@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        # Retrieve the user's credentials from the request
        username = request.form['username']
        password = request.form['password']

        # Validate the credentials against the database
        cur = mysql.connection.cursor()
        cur.execute("SELECT * FROM users WHERE username=%s AND password=%s", (username, password))
        user = cur.fetchone()

        # If the credentials are valid, create a new session for the user
        if user:
            session['username'] = user['username']
            return redirect(url_for('index'))
        else:
            # If the credentials are invalid, return an error message to the user
            return 'Invalid credentials'

    else:
        # If the request method is GET, return the login form
        return '''
      <form method="post">
        <label for="username">Username:</label><br>
        <input type="text" id="username" name="username"><br>
        <label for="password">Password:</label><br>
        <input type="password" id="password" name="password"><br>
        <input type="submit" value="Submit">
      </form>
    '''


@app.route('/index')
def index():
    # If the user is not logged in, redirect them to the login page
    if 'username' not in session:
        return redirect(url_for('login'))

    # If the user is logged in, display a welcome message
    return 'Welcome, {}!'.format(session['username'])


if __name__ == '__main__':
    app.run()