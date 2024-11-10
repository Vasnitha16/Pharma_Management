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
from decimal import Decimal

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
        pharmacy_id = request.form['pharmacy_id']  # Ensure this is passed from the form

        # Connect to the database
        connection = get_db_connection()
        cursor = connection.cursor()

        # Query to check if the credentials are correct
        cursor.execute("SELECT * FROM pharmacy_credentials WHERE username=%s AND password=%s AND pharmacy_id=%s", (username, password, pharmacy_id))
        user = cursor.fetchone()

        if user:
            # Fetch distinct suppliers associated with the given pharmacy_id
            cursor.execute("""
                SELECT DISTINCT  suppliers.name 
                FROM suppliers 
                WHERE pharmacy_id = %s
            """, (pharmacy_id,))
            suppliers = cursor.fetchall()

            # Debugging: Print the suppliers data to check if names are retrieved
            print("Suppliers data:", suppliers)  # This will print a list of tuples (id, name)

            # Close the database connections
            cursor.close()
            connection.close()

            # Render the supplier list page with fetched suppliers
            return render_template('supplier_list.html', suppliers=suppliers)
        else:
            flash('Invalid username, password, or pharmacy ID')
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
        pharmacy_id = request.form['pharmacy_id']

        # Establish a database connection
        connection = get_db_connection()
        cursor = connection.cursor()

        # Check if the pharmacy ID exists in the pharmacies table
        cursor.execute("SELECT * FROM pharmacies WHERE id = %s", (pharmacy_id,))
        pharmacy = cursor.fetchone()

        if not pharmacy:
            flash('Invalid Pharmacy ID. Please check and try again.')
        else:
            # Check if the username already exists
            cursor.execute("SELECT * FROM pharmacy_credentials WHERE username=%s", (username,))
            existing_user = cursor.fetchone()

            if existing_user:
                flash('Username already exists')
            else:
                # Insert new pharmacist into pharmacy_credentials table with plain text password
                cursor.execute("""
                    INSERT INTO pharmacy_credentials (username, password, pharmacy_id)
                    VALUES (%s, %s, %s)
                """, (username, password, pharmacy_id))
                connection.commit()

                flash('Registration successful! Please log in.')

        cursor.close()
        connection.close()

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

@app.route('/suppliers')
def supplier_list():
    connection = get_db_connection()
    cursor = connection.cursor()
    cursor.execute("SELECT id, name FROM suppliers")
    suppliers = cursor.fetchall()
    connection.close()
    return render_template('supplier_list.html', suppliers=suppliers)

@app.route('/supplier/<int:supplier_id>/medicines')
def supplier_medicines(supplier_id):
    connection = get_db_connection()
    cursor = connection.cursor()
    query = """
        SELECT m.id, m.name, m.quantity, m.price, m.description 
        FROM medicines m
        JOIN suppliers s ON m.id = s.medicine_id
        JOIN pharmacies p ON s.pharmacy_id = p.id
        WHERE s.id = %s
    """
    cursor.execute(query, (supplier_id,))
    medicines = [row[0] for row in cursor.fetchall()]
    connection.close()
    return render_template('supplier_medicines.html', medicines=medicines)

@app.route('/update_quantity/<int:medicine_id>/<string:action>', methods=['POST'])
def update_quantity(medicine_id, action):
    # Get cart from session
    cart = session.get('cart', {})

    # Fetch medicine details from the database
    connection = get_db_connection()
    cursor = connection.cursor()
    cursor.execute("SELECT name, price FROM medicines WHERE id = %s", (medicine_id,))
    medicine = cursor.fetchone()
    connection.close()

    if not medicine:
        return jsonify({'success': False, 'error': 'Medicine not found'}), 404

    name, price = medicine
    if action == 'increment':
        if medicine_id in cart:
            cart[medicine_id]['quantity'] += 1
        else:
            cart[medicine_id] = {'name': name, 'quantity': 1, 'price': price}

    elif action == 'decrement':
        if medicine_id in cart and cart[medicine_id]['quantity'] > 0:
            cart[medicine_id]['quantity'] -= 1
        else:
            return jsonify({'success': False, 'error': 'Cannot decrement below zero'}), 400

    session['cart'] = cart  # Update cart in session

    return jsonify({'success': True, 'new_quantity': cart[medicine_id]['quantity']})

@app.route('/cart', methods=['GET'])
def view_cart():
    # Retrieve the cart from the session
    cart = session.get('cart', {})

    # If cart is empty, show an appropriate message
    if not cart:
        flash('Your cart is empty.')
        return render_template('cart.html', cart={}, total_bill=0.00)

    total_bill = 0
    purchased_items = []

    # Iterate over the items in the cart to calculate the total bill
    for item in cart.values():
        try:
            # Ensure that quantity and price are numbers
            quantity = int(item['quantity'])  # Force integer conversion
            price = float(item['price'])      # Force float conversion

            total_bill += quantity * price
            purchased_items.append({
                'name': item['name'],
                'quantity': quantity,
                'price': price,
                'total': quantity * price
            })
        except ValueError:
            flash('There was an error processing your cart items.')
            return redirect(url_for('about'))  # Redirect to a safe page

    return render_template('cart.html', cart=purchased_items, total_bill=total_bill)

@app.route('/checkout', methods=['POST'])
def checkout():
    # Here, you could process the payment or order.
    # After checkout, clear the cart.
    session.pop('cart', None)
    flash('Checkout successful! Thank you for your purchase.')
    return redirect(url_for('about'))  # Redirect to the "about" page or another relevant page

@app.route('/calculate_bill', methods=['GET'])
def calculate_bill():
    total_bill = 0
    purchased_items = []

    # Make sure there's a cart in the session
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




@app.route('/logout')
def logout():
    return redirect(url_for('about'))

if __name__ == '__main__':
    app.run(debug=True)