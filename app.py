# from flask import Flask, render_template, request, redirect, url_for, flash, jsonify
# import mysql.connector
# import os

# app = Flask(__name__)
# app.secret_key = os.urandom(24)

# # Database connection details
# db_config = {
#     'user': 'root',
#     'password': 'root',
#     'host': 'localhost',
#     'database': 'pharmacy_db'
# }

# def get_db_connection():
#     connection = mysql.connector.connect(**db_config)
#     return connection

# @app.route('/')
# def about():
#     return render_template('about.html')

# @app.route('/login_customer', methods=['GET', 'POST'])
# def login_customer():
#     if request.method == 'POST':
#         username = request.form['username']
#         password = request.form['password']
#         connection = get_db_connection()
#         cursor = connection.cursor()
#         cursor.execute("SELECT * FROM user_credentials WHERE username=%s AND password=%s", (username, password))
#         user = cursor.fetchone()
#         if user:
#             cursor.execute("SELECT id, name FROM pharmacies")  # Fetching pharmacy id along with name
#             pharmacies = cursor.fetchall()  # Fetch all pharmacy data (id, name)
#             cursor.close()
#             connection.close()
#             return render_template('pharmacy_list.html', pharmacies=pharmacies)
#         else:
#             flash('Invalid username or password')
#             cursor.close()
#             connection.close()
#     return render_template('login_customer.html')

# @app.route('/login_pharmacist', methods=['GET', 'POST'])
# def login_pharmacist():
#     if request.method == 'POST':
#         username = request.form['username']
#         password = request.form['password']
#         connection = get_db_connection()
#         cursor = connection.cursor()
#         cursor.execute("SELECT * FROM pharmacy_credentials WHERE username=%s AND password=%s", (username, password))
#         user = cursor.fetchone()
#         cursor.close()
#         connection.close()
#         if user:
#             return "Pharmacist logged in successfully!"
#         else:
#             flash('Invalid username or password')
#     return render_template('login_pharmacist.html')

# @app.route('/register_customer', methods=['GET', 'POST'])
# def register_customer():
#     if request.method == 'POST':
#         username = request.form['username']
#         password = request.form['password']
#         connection = get_db_connection()
#         cursor = connection.cursor()
#         cursor.execute("INSERT INTO user_credentials (username, password) VALUES (%s, %s)", (username, password))
#         connection.commit()
#         cursor.close()
#         connection.close()
#         flash('Customer registration successful! You can now log in.')
#         return redirect(url_for('login_customer'))
#     return render_template('register_customer.html')

# @app.route('/register_pharmacist', methods=['GET', 'POST'])
# def register_pharmacist():
#     if request.method == 'POST':
#         username = request.form['username']
#         password = request.form['password']
#         connection = get_db_connection()
#         cursor = connection.cursor()
#         cursor.execute("INSERT INTO pharmacy_credentials (username, password) VALUES (%s, %s)", (username, password))
#         connection.commit()
#         cursor.close()
#         connection.close()
#         flash('Pharmacist registration successful! You can now log in.')
#         return redirect(url_for('login_pharmacist'))
#     return render_template('register_pharmacist.html')

# @app.route('/pharmacy/<int:pharmacy_id>')
# def pharmacy_medicines(pharmacy_id):
#     connection = get_db_connection()
#     cursor = connection.cursor()
#     cursor.execute("SELECT id, name, quantity, price, description FROM medicines WHERE pharmacy_id = %s", (pharmacy_id,))
#     medicines = cursor.fetchall()  # Fetch all medicines for the pharmacy
#     cursor.close()
#     connection.close()

#     # Fetch the pharmacy name
#     connection = get_db_connection()
#     cursor = connection.cursor()
#     cursor.execute("SELECT name FROM pharmacies WHERE id = %s", (pharmacy_id,))
#     pharmacy_name = cursor.fetchone()[0]
#     cursor.close()
#     connection.close()

#     return render_template('medicine_list.html', medicines=medicines, pharmacy_name=pharmacy_name)

# @app.route('/update_quantity/<int:medicine_id>/<string:action>', methods=['POST'])
# def update_quantity(medicine_id, action):
#     connection = get_db_connection()
#     cursor = connection.cursor()
    
#     if action == 'increment':
#         cursor.execute("UPDATE medicines SET quantity = quantity + 1 WHERE id = %s", (medicine_id,))
#     elif action == 'decrement':
#         cursor.execute("UPDATE medicines SET quantity = quantity - 1 WHERE id = %s", (medicine_id,))
    
#     connection.commit()
#     cursor.execute("SELECT quantity FROM medicines WHERE id = %s", (medicine_id,))
#     new_quantity = cursor.fetchone()[0]
#     cursor.close()
#     connection.close()
    
#     return jsonify({'success': True, 'new_quantity': new_quantity})

# if __name__ == '__main__':
#     app.run(debug=True)

# from flask import Flask, render_template, request, redirect, url_for, flash, jsonify
# import mysql.connector
# import os

# app = Flask(__name__)
# app.secret_key = os.urandom(24)

# # Database connection details
# db_config = {
#     'user': 'root',
#     'password': 'root',
#     'host': 'localhost',
#     'database': 'pharmacy_db'
# }

# def get_db_connection():
#     connection = mysql.connector.connect(**db_config)
#     return connection

# @app.route('/')
# def about():
#     return render_template('about.html')

# @app.route('/login_customer', methods=['GET', 'POST'])
# def login_customer():
#     if request.method == 'POST':
#         username = request.form['username']
#         password = request.form['password']
#         connection = get_db_connection()
#         cursor = connection.cursor()
#         cursor.execute("SELECT * FROM user_credentials WHERE username=%s AND password=%s", (username, password))
#         user = cursor.fetchone()
#         if user:
#             cursor.execute("SELECT id, name FROM pharmacies")  # Fetching pharmacy id along with name
#             pharmacies = cursor.fetchall()  # Fetch all pharmacy data (id, name)
#             cursor.close()
#             connection.close()
#             return render_template('pharmacy_list.html', pharmacies=pharmacies)
#         else:
#             flash('Invalid username or password')
#             cursor.close()
#             connection.close()
#     return render_template('login_customer.html')

# @app.route('/login_pharmacist', methods=['GET', 'POST'])
# def login_pharmacist():
#     if request.method == 'POST':
#         username = request.form['username']
#         password = request.form['password']
#         connection = get_db_connection()
#         cursor = connection.cursor()
#         cursor.execute("SELECT * FROM pharmacy_credentials WHERE username=%s AND password=%s", (username, password))
#         user = cursor.fetchone()
#         if user:
#             # Fetch suppliers for this pharmacist (you can modify this query based on your database structure)
#             cursor.execute("SELECT id, name FROM suppliers WHERE pharmacy_id = %s", (user[0],))  # Assuming `user[0]` is the pharmacist's ID
#             suppliers = cursor.fetchall()
#             cursor.close()
#             connection.close()
#             return render_template('supplier_list.html', suppliers=suppliers)
#         else:
#             flash('Invalid username or password')
#             cursor.close()
#             connection.close()
#     return render_template('login_pharmacist.html')

# @app.route('/register_customer', methods=['GET', 'POST'])
# def register_customer():
#     if request.method == 'POST':
#         username = request.form['username']
#         password = request.form['password']
#         connection = get_db_connection()
#         cursor = connection.cursor()
#         cursor.execute("INSERT INTO user_credentials (username, password) VALUES (%s, %s)", (username, password))
#         connection.commit()
#         cursor.close()
#         connection.close()
#         flash('Customer registration successful! You can now log in.')
#         return redirect(url_for('login_customer'))
#     return render_template('register_customer.html')

# @app.route('/register_pharmacist', methods=['GET', 'POST'])
# def register_pharmacist():
#     if request.method == 'POST':
#         username = request.form['username']
#         password = request.form['password']
#         connection = get_db_connection()
#         cursor = connection.cursor()
#         cursor.execute("INSERT INTO pharmacy_credentials (username, password) VALUES (%s, %s)", (username, password))
#         connection.commit()
#         cursor.close()
#         connection.close()
#         flash('Pharmacist registration successful! You can now log in.')
#         return redirect(url_for('login_pharmacist'))
#     return render_template('register_pharmacist.html')

# @app.route('/pharmacy/<int:pharmacy_id>')
# def pharmacy_medicines(pharmacy_id):
#     connection = get_db_connection()
#     cursor = connection.cursor()
#     cursor.execute("SELECT id, name, quantity, price, description FROM medicines WHERE pharmacy_id = %s", (pharmacy_id,))
#     medicines = cursor.fetchall()  # Fetch all medicines for the pharmacy
#     cursor.close()
#     connection.close()

#     # Fetch the pharmacy name
#     connection = get_db_connection()
#     cursor = connection.cursor()
#     cursor.execute("SELECT name FROM pharmacies WHERE id = %s", (pharmacy_id,))
#     pharmacy_name = cursor.fetchone()[0]
#     cursor.close()
#     connection.close()

#     return render_template('medicine_list.html', medicines=medicines, pharmacy_name=pharmacy_name)

# @app.route('/update_quantity/<int:medicine_id>/<string:action>', methods=['POST'])
# def update_quantity(medicine_id, action):
#     connection = get_db_connection()
#     cursor = connection.cursor()
    
#     if action == 'increment':
#         cursor.execute("UPDATE medicines SET quantity = quantity + 1 WHERE id = %s", (medicine_id,))
#     elif action == 'decrement':
#         cursor.execute("UPDATE medicines SET quantity = quantity - 1 WHERE id = %s", (medicine_id,))
    
#     connection.commit()
#     cursor.execute("SELECT quantity FROM medicines WHERE id = %s", (medicine_id,))
#     new_quantity = cursor.fetchone()[0]
#     cursor.close()
#     connection.close()
    
#     return jsonify({'success': True, 'new_quantity': new_quantity})

# @app.route('/logout')
# def logout():
#     # Clear session or redirect to the login page
#     return redirect(url_for('login_pharmacist'))

# if __name__ == '__main__':
#     app.run(debug=True)

from flask import Flask, render_template, request, redirect, url_for, flash, jsonify, session
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
        if user:
            cursor.execute("SELECT id, name FROM pharmacies")  # Fetching pharmacy id along with name
            pharmacies = cursor.fetchall()  # Fetch all pharmacy data (id, name)
            cursor.close()
            connection.close()
            return render_template('pharmacy_list.html', pharmacies=pharmacies)
        else:
            flash('Invalid username or password')
            cursor.close()
            connection.close()
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
        if user:
            cursor.execute("SELECT id, name FROM suppliers WHERE pharmacy_id = %s", (user[0],))  # Assuming `user[0]` is the pharmacist's ID
            suppliers = cursor.fetchall()
            cursor.close()
            connection.close()
            return render_template('supplier_list.html', suppliers=suppliers)
        else:
            flash('Invalid username or password')
            cursor.close()
            connection.close()
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

@app.route('/pharmacy/<int:pharmacy_id>')
def pharmacy_medicines(pharmacy_id):
    connection = get_db_connection()
    cursor = connection.cursor()
    cursor.execute("SELECT id, name, quantity, price, description FROM medicines WHERE pharmacy_id = %s", (pharmacy_id,))
    medicines = cursor.fetchall()  # Fetch all medicines for the pharmacy
    cursor.close()
    connection.close()

    # Fetch the pharmacy name
    connection = get_db_connection()
    cursor = connection.cursor()
    cursor.execute("SELECT name FROM pharmacies WHERE id = %s", (pharmacy_id,))
    pharmacy_name = cursor.fetchone()[0]
    cursor.close()
    connection.close()

    return render_template('medicine_list.html', medicines=medicines, pharmacy_name=pharmacy_name, pharmacy_id=pharmacy_id)

@app.route('/update_quantity/<int:medicine_id>/<string:action>', methods=['POST'])
def update_quantity(medicine_id, action):
    # Track medicines added to the cart in the session
    if 'cart' not in session:
        session['cart'] = {}

    if action == 'increment':
        if medicine_id in session['cart']:
            session['cart'][medicine_id]['quantity'] += 1
        else:
            session['cart'][medicine_id] = {'quantity': 1}

    elif action == 'decrement':
        if medicine_id in session['cart'] and session['cart'][medicine_id]['quantity'] > 0:
            session['cart'][medicine_id]['quantity'] -= 1
            if session['cart'][medicine_id]['quantity'] == 0:
                del session['cart'][medicine_id]

    session.modified = True
    return jsonify({'success': True, 'cart': session['cart']})

@app.route('/calculate_bill', methods=['GET'])
def calculate_bill():
    total_bill = 0
    purchased_items = []
    
    if 'cart' in session:
        connection = get_db_connection()
        cursor = connection.cursor()

        for medicine_id, details in session['cart'].items():
            cursor.execute("SELECT name, price FROM medicines WHERE id = %s", (medicine_id,))
            medicine = cursor.fetchone()
            if medicine:
                name, price = medicine
                total_bill += price * details['quantity']
                purchased_items.append([name, details['quantity'], price])

        cursor.close()
        connection.close()

    return jsonify({'total_bill': total_bill, 'purchased_items': purchased_items})

@app.route('/checkout/<int:pharmacy_id>', methods=['GET'])
def checkout(pharmacy_id):
    # Here we could proceed with actual checkout logic, such as saving the order in a database.
    session.pop('cart', None)  # Clear the cart after checkout
    flash('Checkout successful! Thank you for your purchase.')
    return redirect(url_for('pharmacy_medicines', pharmacy_id=pharmacy_id))

@app.route('/logout')
def logout():
    session.pop('cart', None)  # Clear the cart on logout
    return redirect(url_for('login_pharmacist'))

if __name__ == '__main__':
    app.run(debug=True)
