from flask import Flask, render_template, request, redirect, url_for, flash
from flask_mysqldb import MySQL
import json

# initializations
app = Flask(__name__)

# Mysql Connection
app.config['MYSQL_USER'] = 'sql9380119'
app.config['MYSQL_PASSWORD'] = 'bldMH5YFcg'
app.config['MYSQL_DB'] = 'sql9380119'
app.config['MYSQL_HOST'] = 'sql9.freemysqlhosting.net'
app.config['MYSQL_CURSORCLASS'] = 'DictCursor'
app.secret_key = "mysecretkey"
db = MySQL(app)
# settings
app.secret_key = "mysecretkey"


# routes
@app.route('/')
def Index():
    cur = db.connection.cursor()
    cur.execute('SELECT * FROM Owner')
    data = cur.fetchall()
    cur.close()
    return render_template('index.html', owners=data)

@app.route('/test', methods = ['POST', 'GET'])
def test():
    cur = db.connection.cursor()
    query = "SELECT DISTINCT * FROM Gun, Manufacturer, Seller WHERE Gun.ssn = 123751294;"
    print(query)
    try:
        cur.execute(query)
        data = cur.fetchall()
        return render_template('index.html', guns=data, owners=data)
    except Exception as e:
        print(str(e))
        return render_template('index.html')


@app.route('/search', methods=['GET', 'POST'])
def search(search_value=None, search_param=None):
    if request.method == 'POST':
        cur = db.connection.cursor()
        search_value = request.form['search_val']
        search_param = request.form['search_param']
        owner_query = "SELECT * FROM Owner WHERE " + search_param + "='" + search_value + "';"
        cur.execute(owner_query)
        owner_results = cur.fetchall()
        ssn = owner_results[0]['ssn']
        #gun_query = "SELECT DISTINCT Gun.serial_number, Gun.ssn, Gun.model, Gun.type, Gun.caliber, Seller.name, Seller.address, Manufacturer.name, Manufacturer.country_of_origin FROM Gun, Manufacturer, Seller WHERE Gun.ssn = {0} AND Seller.ssn={0} AND Manufacturer.model=Gun.model;".format(ssn)
        gun_query = "SELECT DISTINCT * FROM Gun, Seller, Manufacturer WHERE Gun.ssn = {0} AND Seller.ssn = {0} AND Gun.model=Manufacturer.model;".format(ssn)
        cur.execute(gun_query)
        gun_results = cur.fetchall()
        db.connection.commit()
        cur.close()
        return render_template('index.html', owners=owner_results, guns=gun_results)

@app.route('/add_owner', methods=['POST'])
def add_owner():
    if request.method == 'POST':
        fname = request.form['fname']
        lname = request.form['lname']
        bday = request.form['bday']
        addr = request.form['addr']
        phone = request.form['phone']
        ssn = request.form['ssn']
        cur = db.connection.cursor()
        cur.execute("INSERT INTO Owner (ssn, first_name, last_name, birthday, address, phone) VALUES (%s,%s,%s,%s,%s,%s)", (ssn, fname, lname, str(bday), addr, phone))
        db.connection.commit()
        flash('Contact Added successfully')
        cur.close()
        return render_template('index.html')

@app.route('/edit_owner/<string:id>', methods=['POST'])
def edit_owner(id):
    return render_template('edit-owner.html')

@app.route('/delete_owner/<id>', methods=['GET', 'POST'])
def delete_owner(id):
    cur = db.connection.cursor()
    owner_query = "DELETE FROM Owner WHERE Owner.ssn = {0}".format(id)
    gun_query = "DELETE FROM Gun WHERE ssn = {0}".format(id)
    seller_query = "DELETE FROM Seller WHERE ssn = {0}".format(id)
    cur.execute(owner_query)
    cur.execute(gun_query)
    cur.execute(seller_query)
    db.connection.commit()
    flash('Owner Deleted Successfully')
    return render_template('index.html', owners=id)

@app.route('/add_gun', methods=['POST'])
def add_gun():
    if request.method == 'POST':
        gun_type = request.form['type']
        ssn = request.form['ssn']
        serial = request.form['serial_number']
        manufacturer = request.form['manufacturer']
        model = request.form['model']
        caliber = request.form['caliber']
        country = request.form['country']
        seller_name = request.form['seller']
        seller_addr = request.form['seller_addr']
        gun_query = "INSERT INTO Gun VALUES (" + str(serial) + ",'" + gun_type + "'," + str(ssn) + ",'" + model + "','" + caliber + "');"
        seller_query = "INSERT INTO Seller VALUES ('" + seller_name + "','" + seller_addr + "'," + ssn + "," + serial + ");"
        manufacturer_query = "INSERT INTO Manufacturer VALUES ('" + manufacturer + "','" + country + "','" + model + "','" + caliber + "');"
        cur = db.connection.cursor()
        cur.execute(gun_query)
        db.connection.commit()
        cur.execute(seller_query)
        db.connection.commit()
        pk_check = cur.execute("SELECT EXISTS (SELECT * FROM Manufacturer WHERE model='" + str(model) + "');")
        if not pk_check:
            cur.execute(manufacturer_query)
        db.connection.commit()
        flash('New Firearm Registered')
        return render_template('index.html')

@app.route('/edit_gun/<string:id>', methods = ['POST', 'GET'])
def edit_gun(id):
    cur = db.connection.cursor()
    query = "SELECT * FROM Gun WHERE serial_number = {0}".format(id)
    cur.execute(query)
    data = cur.fetchall()
    cur.close()
    print(data)
    return render_template('edit-gun.html', gun=data)

@app.route('/update_gun/<string:id>', methods = ['POST', 'GET'])
def update_gun(id):
    if request.method == 'POST':
        cur = db.connection.cursor()
        type = request.form['type']
        model = request.form['model']
        caliber = request.form['caliber']
        serial = eval(str(id))
        query = "UPDATE Gun SET type='" + str(type) + "', model='" + str(model) + "', caliber='" + str(caliber) + "' WHERE serial_number={0};".format(str(serial['serial_number']))
        try:
            cur.execute(query)
            db.connection.commit()
            flash("Gun updated successfully")
            return render_template('index.html')
        except Exception as e:
            flash(str(e))
            return redirect(url_for('Index'))


@app.route('/delete_gun/<string:id>', methods=['GET', 'POST'])
def delete_gun(id):
    cur = db.connection.cursor()
    gun_query = "DELETE FROM Gun WHERE serial_number = {0}".format(id)
    cur.execute(gun_query)
    db.connection.commit()
    seller_query = "DELETE FROM Seller WHERE serial_number = {0}".format(id)
    cur.execute(seller_query)
    db.connection.commit()
    flash('Gun Deleted Successfully')
    return redirect(url_for('Index'))

@app.template_filter('strftime')
def _jinja2_filter_datetime(date, fmt=None):
    format='%b %d, %Y'
    return date.strftime(format)

# starting the app
if __name__ == "__main__":
    app.run(port=3000, debug=True)
