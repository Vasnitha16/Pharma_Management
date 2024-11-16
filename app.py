from flask import Flask, render_template, request, redirect, url_for, jsonify, session, flash
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

@app.route('/login_pharmacist', methods=['GET', 'POST'])
def login_pharmacist():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        pharmacy_id = request.form['pharmacy_id']

        # Authenticate the pharmacist
        query = "SELECT * FROM pharmacy_credentials WHERE username = %s AND password = %s AND pharmacy_id = %s"
        user = fetch_one(query, (username, password, pharmacy_id))

        if user:
            # If authentication succeeds, fetch suppliers associated with this pharmacy
            supplier_query = "SELECT * FROM suppliers WHERE pharmacy_id = %s"
            suppliers = fetch_all(supplier_query, (pharmacy_id,))

            # Render supplier list page with the fetched suppliers
            return render_template('supplier_list.html', suppliers=suppliers, pharmacy_id=pharmacy_id)
        else:
            flash('Invalid username, password, or pharmacy ID')

    return render_template('login_pharmacist.html')

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
    if pharmacy:
            session['pharmacy_id'] = pharmacy['id']  # Store user ID in session
    return render_template('medicine_list.html', medicines=medicines, pharmacy_name=pharmacy['name'], pharmacy_id=pharmacy_id)

@app.route('/add_to_cart/<int:medicine_id>', methods=['POST'])
def add_to_cart(medicine_id):
    user_id = session.get('user_id')  # Placeholder, replace with actual user ID from session

    # Check if the medicine is already in the cart for this user
    query = "SELECT * FROM cart WHERE user_id = %s AND medicine_id = %s"
    existing_item = fetch_one(query, (user_id, medicine_id))
    if existing_item:
        session['medicine_id']=existing_item['medicine_id']

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
    pharmacy_id = session.get('pharmacy_id')
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
    # Insert billing data into bills table
    for item in cart_items:
        try:
            medicine_id = item['medicine_id']
            quantity = item['quantity']
            query = """
            INSERT INTO bills (user_id, medicine_id, pharmacy_id, quantity, total_price)
            VALUES (%s, %s, %s, %s, %s)
        """
            execute_query(query, (user_id, medicine_id, pharmacy_id, quantity, total_price))
        except Exception as e:
            print(f"Error inserting bill: {e}")

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


# @app.route('/billing')
# def billing():
#     # Retrieve the total price from the session
#     user_id = session.get('user_id')

#     total_price = session.get('total_price', 0.0)
#     print(f"Received Total Price from session: {total_price}")  # Debug log
#     pharmacy_id = session.get('pharmacy_id')
#     query = "INSERT INTO bills (user_id, medicine_id,pharmacy_id total_price) VALUES (%s, %s, %d)"
#     execute_query(query, (user_id,pharmacy_id,total_price))

#     return render_template('billing.html', total_price=total_price)

@app.route('/billing')
def billing():
    user_id = session.get('user_id')
    pharmacy_id = session.get('pharmacy_id')

    # Retrieve the total price from the session
    total_price = session.get('total_price', 0.0)
    print(f"Received Total Price from session: {total_price}")  # Debug log

    # Assuming cart_items are stored in the session as in previous logic
    cart_items = session.get('cart_items', [])

<<<<<<< HEAD
    # # Insert billing data into bills table
    # for item in cart_items:
    #     medicine_id = item['medicine_id']
    #     quantity = item['quantity']
    #     query = "INSERT INTO bills (user_id, medicine_id, pharmacy_id, quantity, total_price) VALUES (%s, %s, %s, %s, %s)"
    #     execute_query(query, (user_id, medicine_id, pharmacy_id, quantity, total_price))

=======
    # Insert billing data into bills table
    for item in cart_items:
        try:
            medicine_id = item['medicine_id']
            quantity = item['quantity']
            query = """
            INSERT INTO bills (user_id, medicine_id, pharmacy_id, quantity, total_price)
            VALUES (%s, %s, %s, %s, %s)
        """
            execute_query(query, (user_id, medicine_id, pharmacy_id, quantity, total_price))
        except Exception as e:
            print(f"Error inserting bill: {e}")
>>>>>>> 18ae18b9c207c798c51892ecb7dbb6298521604b
    return render_template('billing.html', total_price=total_price)


@app.route('/supplier_list')
def show_suppliers():
    # Fetching all suppliers from the suppliers table
    query = "SELECT * FROM suppliers "
    suppliers = fetch_all(query)
    return render_template('supplier_list.html', suppliers=suppliers)


@app.route('/supplier_medicines/<int:supplier_id>')
def supplier_medicines(supplier_id):
    query = "SELECT * FROM medicines WHERE supplier_id = %s"
    medicines = fetch_all(query, (supplier_id,))
    print(medicines)  # Debugging: Check the format of medicines
    supplier = fetch_one("SELECT * FROM suppliers WHERE id = %s", (supplier_id,))
    return render_template('supplier_medicines.html', medicines=medicines, supplier_name=supplier['name'])

<<<<<<< HEAD
=======
def fetch_all(query, params=None):
    conn = mysql.connector.connect(**db_config)
    cursor = conn.cursor(dictionary=True)  # Ensure we get dictionary results
    cursor.execute(query, params)
    result = cursor.fetchall()
    cursor.close()
    conn.close()
    return result

# Function to fetch one result as a dictionary
def fetch_one(query, params=None):
    conn = mysql.connector.connect(**db_config)
    cursor = conn.cursor(dictionary=True)  # Ensure we get dictionary results
    cursor.execute(query, params)
    result = cursor.fetchone()
    cursor.close()
    conn.close()
    return result


>>>>>>> 18ae18b9c207c798c51892ecb7dbb6298521604b

@app.route('/increment_quantity/<int:medicine_id>', methods=['POST'])
def increment_quantity(medicine_id):
    connection = get_db_connection()
    cursor = connection.cursor(dictionary=True)
    
    try:
        # Increment quantity by 1
        update_query = "UPDATE medicines SET quantity = quantity + 1 WHERE id = %s"
        cursor.execute(update_query, (medicine_id,))
        connection.commit()
        
        # Get the new quantity to send back to the client
        select_query = "SELECT quantity FROM medicines WHERE id = %s"
        cursor.execute(select_query, (medicine_id,))
        new_quantity = cursor.fetchone()['quantity']
    finally:
        cursor.close()
        connection.close()

    return {'new_quantity': new_quantity}


@app.route('/supplier/<int:supplier_id>/medicines')
def show_medicines(supplier_id):
    # Establish MySQL connection
    connection = mysql.connector.connect(**db_config)
    cursor = connection.cursor(dictionary=True)

    # Query to get medicines from the database
    query = "SELECT id, name, quantity, price FROM medicines WHERE supplier_id = %s"
    cursor.execute(query, (supplier_id,))
    medicines = cursor.fetchall()

    # Close the database connection
    cursor.close()
    connection.close()

    return render_template('medicines.html', supplier_name="Supplier Example", medicines=medicines)


@app.route('/generate_bill/<int:medicine_id>', methods=['POST'])
def generate_bill(medicine_id):
    data = request.get_json()
    quantity_needed = data['quantity_needed']

    # Create a database connection
    conn = mysql.connector.connect(**db_config)
    cursor = conn.cursor(dictionary=True)

    try:
        # Fetch the current available quantity of the medicine
        cursor.execute("SELECT * FROM medicines WHERE id = %s", (medicine_id,))
        medicine = cursor.fetchone()

        if not medicine:
            return jsonify({"error": "Medicine not found"}), 404

        # Check if enough stock is available
        if medicine['quantity'] < quantity_needed:
            return jsonify({"error": "Not enough stock"}), 400

        # Deduct the quantity
        new_quantity = medicine['quantity'] - quantity_needed

        # Update the quantity in the database
        cursor.execute(
            "UPDATE medicines SET quantity = %s WHERE id = %s", 
            (new_quantity, medicine_id)
        )

        # Commit the transaction to the database
        conn.commit()

        return jsonify({"new_quantity": new_quantity, "message": "Bill generated successfully!"})

    except mysql.connector.Error as err:
        # Rollback the transaction in case of error
        conn.rollback()
        return jsonify({"error": f"Database error: {err}"}), 500

    finally:
        # Close the cursor and connection
        cursor.close()
        conn.close()

if __name__ == '__main__':
    app.run(debug=True)