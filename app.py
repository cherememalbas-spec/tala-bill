from flask import Flask, render_template, request, redirect, url_for

app = Flask(__name__)

# 🔐 BUILT-IN USERS (DICTIONARY)
users = {
    'admin': ['admin123', 'admin'],
    'user': ['user123', 'user']
}

current_user = None  # simple login tracker (no session)

customer_id_counter = 1110  # simple ID generator
# 📦 DATABASE (LIST)
customers= []

# -------------------------------
# 👤 CUSTOMER CLASS (OOP)
# -------------------------------
class Customer:
    def __init__(self, name, email, contact ):
        global customer_id_counter
        customer_id_counter += 1
        self.__id = customer_id_counter
        self.__name = name
        self.__email = email
        self.__contact = contact   

    # getters (encapsulation)
    def get_id(self):
        return self.__id

    def get_name(self):
        return self.__name

    def get_email(self):
        return self.__email

    def get_contact(self):
        return self.__contact


    # update method
    def update(self, name, email, contact):
        self.__name = name
        self.__email = email
        self.__contact = contact


# -------------------------------
# 🏠 HOME
# -------------------------------
@app.route('/')
def index():
    return render_template("index.html")


# -------------------------------
# 🔑 LOGIN (NO SESSION)
# -------------------------------
@app.route('/login', methods=['GET', 'POST'])
def login():
    global current_user

    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        if username in users and users[username][0] == password:
            current_user = username  # <--- CRITICAL: This sets the login state
            if users[username][1] == 'admin':
                return redirect(url_for('admindashboard')) # Use redirect, not render
            else:
                return render_template('userdashboard.html', massage=username)
        else:
             return render_template('login.html', massage='Invalid username or password')
    return render_template('login.html', massage='')

# -------------------------------
# 📊 DASHBOARD
# -------------------------------
@app.route('/admindashboard')
def admindashboard():
    global current_user
    if not current_user:
        return redirect(url_for('login'))
    
    search_query = request.args.get('search', '').lower()

    if search_query:
        filtered_customers = [
            c for c in customers 
            if search_query in str(c.get_id()) or search_query in c.get_name().lower()
        ]
    else:
        filtered_customers = customers

    return render_template("admindashboard.html", customers=filtered_customers)


# -------------------------------
# ➕ ADD CUSTOMER
# -------------------------------
@app.route('/add_customer', methods=['GET', 'POST'])
def add_customer():
    global current_user
    if not current_user:
        return redirect(url_for('login'))

    if request.method == 'POST':
        name = request.form['name']
        email = request.form['email']
        contact = request.form['contact']

        new_customer = Customer(name, email, contact,)
        customers.append(new_customer)

        return render_template("admindashboard.html", customers=customers, success_message="Customer added successfully!")

    return render_template("add_customer.html")


# -------------------------------
# ❌ DELETE CUSTOMER
# -------------------------------
@app.route('/delete/<int:id>')
def delete_customer(id):
    global customers

    customers = [c for c in customers if c.get_id() != id]
    return redirect(url_for('admindashboard'))


# -------------------------------
# ✏️ EDIT CUSTOMER
# -------------------------------
@app.route('/edit/<int:id>', methods=['GET', 'POST'])
def edit_customer(id):
    customer = next((c for c in customers if c.get_id() == id), None)

    if not customer:
        return "Customer not found", 404
    if request.method == 'POST':
        customer.update(
            request.form['name'],
            request.form['email'],
            request.form['contact'],
        )
        return render_template("admindashboard.html", customers=customers,success_msg="Customer updated successfully!")

    return render_template("edit.html", customer=customer)


# -------------------------------
# 🚪 LOGOUT
# -------------------------------
@app.route('/logout')
def logout():
    global current_user
    current_user = None
    return redirect(url_for('login'))


# -------------------------------
# ▶️ RUN
# -------------------------------
if __name__ == '__main__':
    app.run(debug=True)