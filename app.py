from flask import Flask, render_template, request, redirect, url_for, flash
import mysql.connector
import os

app = Flask(__name__)
app.secret_key = os.urandom(24)

# Database connection details
db_config = {
    'user': 'root',
    'password': 'root',
    'host': 'localhost',
    'database': 'pharmacy_db'
}

def get_db_connection():
    connection = mysql.connector.connect(**db_config)
    return connection

@app.route('/')
def about():
    return render_template('about.html')

@app.route('/login_customer', methods=['GET', 'POST'])
def login_customer():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        connection = get_db_connection()
        cursor = connection.cursor()
        cursor.execute("SELECT * FROM user_credentials WHERE username=%s AND password=%s", (username, password))
        user = cursor.fetchone()
        cursor.close()
        connection.close()
        if user:
            return redirect(url_for('pharmacy_list'))
        else:
            flash('Invalid username or password')
    return render_template('login_customer.html')

@app.route('/login_pharmacist', methods=['GET', 'POST'])
def login_pharmacist():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        connection = get_db_connection()
        cursor = connection.cursor()
        cursor.execute("SELECT * FROM pharmacy_credentials WHERE username=%s AND password=%s", (username, password))
        user = cursor.fetchone()
        cursor.close()
        connection.close()
        if user:
            return "Pharmacist logged in successfully!"
        else:
            flash('Invalid username or password')
    return render_template('login_pharmacist.html')

@app.route('/register_customer', methods=['GET', 'POST'])
def register_customer():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        connection = get_db_connection()
        cursor = connection.cursor()
        cursor.execute("INSERT INTO user_credentials (username, password) VALUES (%s, %s)", (username, password))
        connection.commit()
        cursor.close()
        connection.close()
        flash('Customer registration successful! You can now log in.')
        return redirect(url_for('login_customer'))
    return render_template('register_customer.html')

@app.route('/register_pharmacist', methods=['GET', 'POST'])
def register_pharmacist():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        connection = get_db_connection()
        cursor = connection.cursor()
        cursor.execute("INSERT INTO pharmacy_credentials (username, password) VALUES (%s, %s)", (username, password))
        connection.commit()
        cursor.close()
        connection.close()
        flash('Pharmacist registration successful! You can now log in.')
        return redirect(url_for('login_pharmacist'))
    return render_template('register_pharmacist.html')

@app.route('/pharmacy_list')
def pharmacy_list():
    connection = get_db_connection()
    cursor = connection.cursor()
    cursor.execute("SELECT id, name FROM pharmacies")
    pharmacies = cursor.fetchall()
    cursor.close()
    connection.close()
    return render_template('pharmacy_list.html', pharmacies=pharmacies)

@app.route('/pharmacy/<int:pharmacy_id>')
def pharmacy_medicines(pharmacy_id):
    connection = get_db_connection()
    cursor = connection.cursor()
    cursor.execute("SELECT name FROM medicines WHERE pharmacy_id = %s", (pharmacy_id,))
    medicines = cursor.fetchall()
    cursor.close()
    connection.close()

    connection = get_db_connection()
    cursor = connection.cursor()
    cursor.execute("SELECT name FROM pharmacies WHERE id = %s", (pharmacy_id,))
    pharmacy_name = cursor.fetchone()[0]
    cursor.close()
    connection.close()

    return render_template('medicine_list.html', medicines=medicines, pharmacy_name=pharmacy_name)

if __name__ == '__main__':
    app.run(debug=True)
