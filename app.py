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

# # from flask import Flask, render_template, request, redirect, url_for, flash, jsonify
# # import mysql.connector
# # import os

# # app = Flask(__name__)
# # app.secret_key = os.urandom(24)

# # # Database connection details
# # db_config = {
# #     'user': 'root',
# #     'password': 'root',
# #     'host': 'localhost',
# #     'database': 'pharmacy_db'
# # }

# # def get_db_connection():
# #     connection = mysql.connector.connect(**db_config)
# #     return connection

# # @app.route('/')
# # def about():
# #     return render_template('about.html')

# # @app.route('/login_customer', methods=['GET', 'POST'])
# # def login_customer():
# #     if request.method == 'POST':
# #         username = request.form['username']
# #         password = request.form['password']
# #         connection = get_db_connection()
# #         cursor = connection.cursor()
# #         cursor.execute("SELECT * FROM user_credentials WHERE username=%s AND password=%s", (username, password))
# #         user = cursor.fetchone()
# #         if user:
# #             cursor.execute("SELECT id, name FROM pharmacies")  # Fetching pharmacy id along with name
# #             pharmacies = cursor.fetchall()  # Fetch all pharmacy data (id, name)
# #             cursor.close()
# #             connection.close()
# #             return render_template('pharmacy_list.html', pharmacies=pharmacies)
# #         else:
# #             flash('Invalid username or password')
# #             cursor.close()
# #             connection.close()
# #     return render_template('login_customer.html')

# # @app.route('/login_pharmacist', methods=['GET', 'POST'])
# # def login_pharmacist():
# #     if request.method == 'POST':
# #         username = request.form['username']
# #         password = request.form['password']
# #         connection = get_db_connection()
# #         cursor = connection.cursor()
# #         cursor.execute("SELECT * FROM pharmacy_credentials WHERE username=%s AND password=%s", (username, password))
# #         user = cursor.fetchone()
# #         if user:
# #             # Fetch suppliers for this pharmacist (you can modify this query based on your database structure)
# #             cursor.execute("SELECT id, name FROM suppliers WHERE pharmacy_id = %s", (user[0],))  # Assuming `user[0]` is the pharmacist's ID
# #             suppliers = cursor.fetchall()
# #             cursor.close()
# #             connection.close()
# #             return render_template('supplier_list.html', suppliers=suppliers)
# #         else:
# #             flash('Invalid username or password')
# #             cursor.close()
# #             connection.close()
# #     return render_template('login_pharmacist.html')

# # @app.route('/register_customer', methods=['GET', 'POST'])
# # def register_customer():
# #     if request.method == 'POST':
# #         username = request.form['username']
# #         password = request.form['password']
# #         connection = get_db_connection()
# #         cursor = connection.cursor()
# #         cursor.execute("INSERT INTO user_credentials (username, password) VALUES (%s, %s)", (username, password))
# #         connection.commit()
# #         cursor.close()
# #         connection.close()
# #         flash('Customer registration successful! You can now log in.')
# #         return redirect(url_for('login_customer'))
# #     return render_template('register_customer.html')

# # @app.route('/register_pharmacist', methods=['GET', 'POST'])
# # def register_pharmacist():
# #     if request.method == 'POST':
# #         username = request.form['username']
# #         password = request.form['password']
# #         connection = get_db_connection()
# #         cursor = connection.cursor()
# #         cursor.execute("INSERT INTO pharmacy_credentials (username, password) VALUES (%s, %s)", (username, password))
# #         connection.commit()
# #         cursor.close()
# #         connection.close()
# #         flash('Pharmacist registration successful! You can now log in.')
# #         return redirect(url_for('login_pharmacist'))
# #     return render_template('register_pharmacist.html')

# # @app.route('/pharmacy/<int:pharmacy_id>')
# # def pharmacy_medicines(pharmacy_id):
# #     connection = get_db_connection()
# #     cursor = connection.cursor()
# #     cursor.execute("SELECT id, name, quantity, price, description FROM medicines WHERE pharmacy_id = %s", (pharmacy_id,))
# #     medicines = cursor.fetchall()  # Fetch all medicines for the pharmacy
# #     cursor.close()
# #     connection.close()

# #     # Fetch the pharmacy name
# #     connection = get_db_connection()
# #     cursor = connection.cursor()
# #     cursor.execute("SELECT name FROM pharmacies WHERE id = %s", (pharmacy_id,))
# #     pharmacy_name = cursor.fetchone()[0]
# #     cursor.close()
# #     connection.close()

# #     return render_template('medicine_list.html', medicines=medicines, pharmacy_name=pharmacy_name)

# # @app.route('/update_quantity/<int:medicine_id>/<string:action>', methods=['POST'])
# # def update_quantity(medicine_id, action):
# #     connection = get_db_connection()
# #     cursor = connection.cursor()
    
# #     if action == 'increment':
# #         cursor.execute("UPDATE medicines SET quantity = quantity + 1 WHERE id = %s", (medicine_id,))
# #     elif action == 'decrement':
# #         cursor.execute("UPDATE medicines SET quantity = quantity - 1 WHERE id = %s", (medicine_id,))
    
# #     connection.commit()
# #     cursor.execute("SELECT quantity FROM medicines WHERE id = %s", (medicine_id,))
# #     new_quantity = cursor.fetchone()[0]
# #     cursor.close()
# #     connection.close()
    
# #     return jsonify({'success': True, 'new_quantity': new_quantity})

# # @app.route('/logout')
# # def logout():
# #     # Clear session or redirect to the login page
# #     return redirect(url_for('login_pharmacist'))

# # if __name__ == '__main__':
# #     app.run(debug=True)

from flask import Flask, render_template, request, redirect, url_for, jsonify, session
import mysql.connector

import os


app = Flask(__name__)
app.secret_key = os.urandom(24)
# Database configuration
db_config = {
    'user': 'root',
    'password': 'root',
    'host': 'localhost',
    'database': 'pharmacy_db'
}
def get_db_connection():
     connection = mysql.connector.connect(**db_config)
     return connection

# Function to execute a query
def execute_query(query, params=None):
    conn = mysql.connector.connect(**db_config)
    cursor = conn.cursor(dictionary=True)
    cursor.execute(query, params)
    conn.commit()
    cursor.close()
    conn.close()

# Function to fetch all results
def fetch_all(query, params=None):
    conn = mysql.connector.connect(**db_config)
    cursor = conn.cursor(dictionary=True)
    cursor.execute(query, params)
    result = cursor.fetchall()
    cursor.close()
    conn.close()
    return result

# Function to fetch one result
def fetch_one(query, params=None):
    conn = mysql.connector.connect(**db_config)
    cursor = conn.cursor(dictionary=True)
    cursor.execute(query, params)
    result = cursor.fetchone()
    cursor.close()
    conn.close()
    return result

@app.route('/')
def about():
    return render_template('about.html')

@app.route('/login_customer', methods=['GET', 'POST'])
def login_customer():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        query = "SELECT * FROM user_credentials WHERE username = %s AND password = %s"
        user = fetch_one(query, (username, password))
        if user:
            session['user_id'] = user['id']  # Store user ID in session
            return redirect(url_for('pharmacy_list'))
        else:
            return "Invalid username or password!"
    return render_template('login_customer.html')


@app.route('/register_customer', methods=['GET', 'POST'])
def register_customer():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        query = "SELECT * FROM user_credentials WHERE username = %s"
        user = fetch_one(query, (username,))
        if user:
            return "Username already exists!"
        query = "INSERT INTO user_credentials (username, password) VALUES (%s, %s)"
        execute_query(query, (username, password))
        return redirect(url_for('login_customer'))
    return render_template('register_customer.html')

# Pharmacist routes
@app.route('/login_pharmacist', methods=['GET', 'POST'])
def login_pharmacist():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        query = "SELECT * FROM pharmacists WHERE username = %s AND password = %s"
        user = fetch_one(query, (username, password))
        if user:
            return redirect(url_for('pharmacy_list'))
        else:
            return "Invalid username or password!"
    return render_template('login_pharmasist.html')

@app.route('/register_pharmacist', methods=['GET', 'POST'])
def register_pharmacist():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        query = "SELECT * FROM pharmacists WHERE username = %s"
        user = fetch_one(query, (username,))
        if user:
            return "Username already exists!"
        query = "INSERT INTO pharmacists (username, password) VALUES (%s, %s)"
        execute_query(query, (username, password))
        return redirect(url_for('login_pharmacist'))
    return render_template('register_pharmacist.html')

# Route to display the list of pharmacies
@app.route('/pharmacy_list')
def pharmacy_list():
    query = "SELECT * FROM pharmacies"
    pharmacies = fetch_all(query)
    return render_template('pharmacy_list.html', pharmacies=pharmacies)

# Route to display the list of medicines for a selected pharmacy
@app.route('/pharmacy_medicines/<int:pharmacy_id>')
def pharmacy_medicines(pharmacy_id):
    query = "SELECT * FROM medicines WHERE pharmacy_id = %s"
    medicines = fetch_all(query, (pharmacy_id,))
    pharmacy_query = "SELECT * FROM pharmacies WHERE id = %s"
    pharmacy = fetch_one(pharmacy_query, (pharmacy_id,))
    return render_template('medicine_list.html', medicines=medicines, pharmacy_name=pharmacy['name'], pharmacy_id=pharmacy_id)

@app.route('/add_to_cart/<int:medicine_id>', methods=['POST'])
def add_to_cart(medicine_id):
    user_id = session.get('user_id')  # Placeholder, replace with actual user ID from session

    # Check if the medicine is already in the cart for this user
    query = "SELECT * FROM cart WHERE user_id = %s AND medicine_id = %s"
    existing_item = fetch_one(query, (user_id, medicine_id))

    if existing_item:
        # If the medicine is already in the cart, just increment the quantity
        new_quantity = existing_item['quantity'] + 1
        update_query = "UPDATE cart SET quantity = %s WHERE user_id = %s AND medicine_id = %s"
        execute_query(update_query, (new_quantity, user_id, medicine_id))
    else:
        # If the medicine is not in the cart, add a new item
        insert_query = "INSERT INTO cart (user_id, medicine_id, quantity) VALUES (%s, %s, 1)"
        execute_query(insert_query, (user_id, medicine_id))

    return jsonify({'success': True})


@app.route('/view_cart')
def view_cart():
    user_id = session.get('user_id')  # Placeholder for actual logged-in user ID
    query = """SELECT m.name, c.quantity, m.price, c.medicine_id 
               FROM cart c
               JOIN medicines m ON c.medicine_id = m.id
               WHERE c.user_id = %s"""
    cart_items = fetch_all(query, (user_id,))
    return render_template('view_cart.html', cart_items=cart_items)


@app.route('/update_quantity/<int:medicine_id>', methods=['POST'])
def update_quantity(medicine_id):
    user_id = session.get('user_id')  # Placeholder for actual logged-in user ID

    # Get the new quantity from the POST request and convert it to an integer
    data = request.get_json()
    new_quantity = int(data.get('quantity'))

    if new_quantity is None or new_quantity <= 0:
        return jsonify({'success': False, 'message': 'Invalid quantity'})

    # Update the quantity in the cart
    query = """UPDATE cart 
               SET quantity = %s
               WHERE user_id = %s AND medicine_id = %s"""
    execute_query(query, (new_quantity, user_id, medicine_id))

    return jsonify({'success': True})


@app.route('/checkout', methods=['POST'])
def checkout():
    user_id = session.get('user_id')
    if not user_id:
        return redirect(url_for('login_customer'))  # Redirect to login if not logged in

    cart_items = request.json.get('items', [])
    total_price = 0

    for item in cart_items:
        medicine_id = item['medicine_id']
        quantity = int(item['quantity'])

        # Fetch medicine price from the database
        query = "SELECT price FROM medicines WHERE id = %s"
        medicine = fetch_one(query, (medicine_id,))

        if medicine:
            price = medicine['price']
            total_price += price * quantity

        # Update medicine quantity in the database
        update_query = """UPDATE medicines 
                          SET quantity = quantity - %s 
                          WHERE id = %s"""
        execute_query(update_query, (quantity, medicine_id))

    # Store the total price in the session
    session['total_price'] = total_price

    # Redirect to billing page
    return redirect(url_for('billing'))


@app.route('/logout', methods=['POST'])
def logout():
    
    user_id = session.get('user_id')
    cart_items = session.get('cart_items', [])
    for item in cart_items:
        medicine_id = item['medicine_id']
        quantity = item['quantity']

        # Decrease medicine quantity in the database
        update_query = """UPDATE medicines 
                          SET quantity = quantity - %s 
                          WHERE id = %s"""
        execute_query(update_query, (quantity, medicine_id))

    # Clear the session after processing the logout
    session.pop('user_id', None)
    session.pop('cart_items', None)
    session.pop('total_price', None)

    if user_id:
        # Clear cart entries for the user from the database
        delete_query = "DELETE FROM cart WHERE user_id = %s"
        execute_query(delete_query, (user_id,))
    
    # Clear other session data
    session.pop('total_price', None)
    session.clear()  # Clears the entire session

    # Perform other logout operations (e.g., redirect to login page)
    return redirect(url_for('login_customer'))


@app.route('/billing')
def billing():
    # Retrieve the total price from the session
    total_price = session.get('total_price', 0.0)
    print(f"Received Total Price from session: {total_price}")  # Debug log

    return render_template('billing.html', total_price=total_price)


if __name__ == '__main__':
    app.run(debug=True)