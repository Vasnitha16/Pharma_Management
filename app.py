from flask import Flask, render_template, request, redirect, url_for, flash
import mysql.connector
from mysql.connector import Error

app = Flask(__name__)
app.secret_key = 'your_secret_key'

# Database connection configuration
db_config = {
    'host': 'localhost',
    'user': 'root',
    'password': 'root',
    'database': 'pharmacy_db'
}

def get_db_connection():
    try:
        connection = mysql.connector.connect(**db_config)
        if connection.is_connected():
            return connection
    except Error as e:
        print(f"Error: {e}")
        return None

@app.route('/')
def home():
    return """
    <h1>Welcome to the Pharmacy Database Management System</h1>
    <nav>
        <a href='/about'>About Us</a>
        <a href='/login'>Login</a>
        <a href='/signup'>Signup</a>
    </nav>
    """

@app.route('/about')
def about():
    return render_template('about.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        
        connection = get_db_connection()
        cursor = connection.cursor()
        cursor.execute("SELECT * FROM pharmacy_users WHERE username = %s AND password = %s", (username, password))
        user = cursor.fetchone()
        connection.close()
        
        if user:
            flash('Login successful!', 'success')
            return redirect(url_for('home'))
        else:
            flash('Invalid credentials, please try again.', 'danger')
    
    return render_template('login.html')

@app.route('/signup', methods=['GET', 'POST'])
def signup():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        
        connection = get_db_connection()
        cursor = connection.cursor()
        try:
            cursor.execute("INSERT INTO pharmacy_users (username, password) VALUES (%s, %s)", (username, password))
            connection.commit()
            flash('Signup successful! Please login.', 'success')
            return redirect(url_for('login'))
        except mysql.connector.IntegrityError:
            flash('Username already exists. Please choose a different username.', 'danger')
        finally:
            connection.close()
    
    return render_template('signup.html')

if __name__ == '__main__':
    app.run(debug=True)
