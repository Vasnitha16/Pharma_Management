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

from flask import Flask, render_template, request, redirect, url_for, flash, jsonify
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
            # Fetch suppliers for this pharmacist (you can modify this query based on your database structure)
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
@app.route('/medicine_list', methods=['GET'])
def medicine_list():
    # Get initial quantities from the database
    connection = get_db_connection()
    cursor = connection.cursor()
    
    pharmacy_id = request.args.get('pharmacy_id')
    cursor.execute("SELECT id, name, quantity, price FROM medicines WHERE pharmacy_id = %s", (pharmacy_id,))
    medicines = cursor.fetchall()
    
    # Store initial quantities in session only if not already stored
    if 'initial_quantities' not in session:
        initial_quantities = {str(medicine[0]): medicine[2] for medicine in medicines}  # Store initial quantities by medicine_id
        session['initial_quantities'] = initial_quantities
        session.modified = True  # Mark session as modified to persist changes
    
    connection.close()
    
    return render_template('medicine_list.html', medicines=medicines, pharmacy_name="My Pharmacy", pharmacy_id=pharmacy_id)


@app.route('/pharmacy/<int:pharmacy_id>')
def pharmacy_medicines(pharmacy_id):
    connection = get_db_connection()
    cursor = connection.cursor()
    cursor.execute("SELECT id, name, quantity, price, description FROM medicines WHERE pharmacy_id = %s", (pharmacy_id,))
    medicines = cursor.fetchall()
    cursor.close()
    connection.close()

    connection = get_db_connection()
    cursor = connection.cursor()
    cursor.execute("SELECT name FROM pharmacies WHERE id = %s", (pharmacy_id,))
    pharmacy_name = cursor.fetchone()[0]
    cursor.close()
    connection.close()

    # Store initial quantities in session only if not already stored
    if 'initial_quantities' not in session:
        session['initial_quantities'] = {medicine[0]: medicine[2] for medicine in medicines}
        session.modified = True  # Mark session as modified
    return render_template('medicine_list.html', medicines=medicines, pharmacy_name=pharmacy_name, pharmacy_id=pharmacy_id)


@app.route('/update_quantity/<int:medicine_id>/<action>', methods=['POST'])
def update_quantity(medicine_id, action):
    # Get current quantities stored in the session
    initial_quantities = session.get('initial_quantities', {})
    current_quantities = session.get('current_quantities', {})

    # Fetch the initial quantity for the given medicine_id from the session
    initial_quantity = initial_quantities.get(str(medicine_id), None)
    current_quantity = current_quantities.get(str(medicine_id), initial_quantity)  # Default to initial if not found

    if current_quantity is None:
        return jsonify({'success': False, 'message': 'Medicine not found in session'})

    # Update the current quantity based on the action
    if action == 'increment':
        new_quantity = current_quantity + 1
    elif action == 'decrement' and current_quantity > 0:
        new_quantity = current_quantity - 1
    else:
        return jsonify({'success': False, 'message': 'Invalid action or quantity'})

    # Update the current quantities in the session
    current_quantities[str(medicine_id)] = new_quantity
    session['current_quantities'] = current_quantities

    # Return the new quantity to update the front-end
    return jsonify({'success': True, 'new_quantity': new_quantity})
@app.route('/calculate_bill', methods=['GET'])
def calculate_bill():
    initial_quantities = session.get('initial_quantities', {})
    current_quantities = session.get('current_quantities', {})

    # Debug print statement to print the initial quantities
    print("Initial Quantities:", initial_quantities)
    print("Current Quantities:", current_quantities)

    connection = get_db_connection()
    cursor = connection.cursor()

    pharmacy_id = request.args.get('pharmacy_id')
    cursor.execute("SELECT id, name, quantity, price FROM medicines WHERE pharmacy_id = %s", (pharmacy_id,))
    medicines = cursor.fetchall()

    total_bill = 0
    purchased_items = []

    for medicine in medicines:
        medicine_id, name, price = medicine

        # Retrieve both initial and current quantities from session
        initial_quantity = initial_quantities.get(str(medicine_id))  # Default to current if not found
        current_quantity = current_quantities.get(str(medicine_id)) # Default to initial if not found

        # Debug print statements to track quantities
        print(f"Medicine: {name}, Initial Quantity: {initial_quantity}, Current Quantity: {current_quantity}")

        # Calculate purchased quantity and update total bill
        if initial_quantity > current_quantity:
            quantity_purchased = initial_quantity - current_quantity
            total_bill += quantity_purchased * price
            purchased_items.append((name, quantity_purchased, price))

    cursor.close()
    connection.close()

    return jsonify({'total_bill': total_bill, 'purchased_items': purchased_items})


@app.route('/checkout/<int:pharmacy_id>')
def checkout(pharmacy_id):
    initial_quantities = session.get('initial_quantities', {})
    # Debug print statement to print the initial quantities
    print("Initial Quantities:", initial_quantities)
    connection = get_db_connection()
    cursor = connection.cursor()
    
    cursor.execute("SELECT id, name, quantity, price FROM medicines WHERE pharmacy_id = %s", (pharmacy_id,))
    medicines = cursor.fetchall()
    
    total_bill = 0
    purchased_items = []

    for medicine in medicines:
        medicine_id, name, current_quantity, price = medicine
        print(f"Medicine: {name}, Current Quantity: {current_quantity}")
        initial_quantity = initial_quantities.get(medicine_id, current_quantity)

        # Print initial and current quantities to the console
        print(f"Medicine: {name}, Initial Quantity: {initial_quantity}, Current Quantity: {current_quantity}")

        if initial_quantity > current_quantity:
            quantity_purchased = initial_quantity - current_quantity
            total_bill += quantity_purchased * price
            purchased_items.append((name, quantity_purchased, price))

    cursor.close()
    connection.close()

    # Clear initial quantities from session after checkout
    session.pop('initial_quantities', None)
    session.modified = True  # Mark session as modified

    return render_template('checkout.html', purchased_items=purchased_items, total_bill=total_bill)




@app.route('/confirm_checkout')
def confirm_checkout():
    flash('Checkout confirmed! Thank you for your purchase.')
    return redirect(url_for('login_customer'))


@app.route('/logout')
def logout():
    # Clear session or redirect to the login page
    return redirect(url_for('login_pharmacist'))

if __name__ == '__main__':
    app.run(debug=True)


