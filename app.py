from flask import Flask, render_template, request, redirect, url_for, flash
from flask_mysqldb import MySQL
import json

# initializations
app = Flask(__name__)

# Mysql Connection
app.config['MYSQL_USER'] = 'sql9381394'
app.config['MYSQL_PASSWORD'] = 'T2kcIdSRiK'#bldMH5YFcg'
app.config['MYSQL_DB'] = 'sql9381394'#'sql9380119'
app.config['MYSQL_HOST'] = 'sql9.freemysqlhosting.net'
app.config['MYSQL_CURSORCLASS'] = 'DictCursor'
db = MySQL(app)
# settings
app.secret_key = "mysecretkey"

#W(D4@#]Nu>T?|e^c

# routes
@app.route('/')
def Index():
    cur = db.connection.cursor()
    cur.execute('SELECT * FROM Owner')
    data = cur.fetchall()
    cur.close()
    info = ["Owners in Database"]
    return render_template('index.html', owners=data, info=info)

@app.route('/test', methods = ['POST', 'GET'])
def test():
    cur = db.connection.cursor()
    query = "SELECT * FROM Owner WHERE ssn = 122432343;"
    print(query)
    try:
        cur.execute(query)
        data = cur.fetchall()
        return str(data)#render_template('index.html', guns=data, owners=data)
    except Exception as e:
        print(str(e))
        return render_template('index.html')


@app.route('/search', methods=['GET', 'POST'])
def search(search_value=None, search_param=None):
    try:
        if request.method == 'POST':
            cur = db.connection.cursor()
            search_value = request.form['search_val']
            search_param = request.form['search_param']
            owner_query = "SELECT DISTINCT * FROM Owner WHERE " + search_param + "='" + search_value + "';"
            cur.execute(owner_query)
            owner_results = cur.fetchall()
            ssn = owner_results[0]['ssn']
            gun_query = "SELECT DISTINCT * FROM Gun, Seller, Manufacturer WHERE Gun.ssn = {0} AND Gun.serial_number = Seller.serial_number AND Gun.model=Manufacturer.model;".format(ssn)
            cur.execute(gun_query)
            gun_results = cur.fetchall()
            db.connection.commit()
            cur.close()
            info = ["Individual", "Guns Owned by " + owner_results[0]['first_name'] + " " + owner_results[0]['last_name']]
            return render_template('index.html', owners=owner_results, guns=gun_results, info=info)

    except Exception as e:
        flash(str(e))
        return redirect(url_for('Index'))


@app.route('/add_owner', methods=['POST'])
def add_owner():
    try:
        if request.method == 'POST':
            fname = request.form['fname']
            lname = request.form['lname']
            bday = request.form['bday']
            addr = request.form['addr']
            phone = request.form['phone']
            ssn = request.form['ssn']
            if len(ssn) != 9:
                flash("Incorrect social security format")
                return render_template('index.html')
            if len(phone) != 10:
                flash("Incorrect phone number format")
                return render_template('index.html')
            cur = db.connection.cursor()
            cur.execute("INSERT INTO Owner (ssn, first_name, last_name, birthday, address, phone) VALUES (%s,%s,%s,%s,%s,%s)", (ssn, fname, lname, str(bday), addr, phone))
            db.connection.commit()
            flash('Contact Added successfully')
            cur.close()
            return redirect(url_for('Index'))
    except Exception as e:
        flash(str(e))
        return redirect(url_for('Index'))

@app.route('/edit_owner/<string:id>', methods=['POST', 'GET'])
def edit_owner(id):
    cur = db.connection.cursor()
    query = "SELECT * FROM Owner WHERE ssn = '{0}';".format(id)
    cur.execute(query)
    data = cur.fetchall()
    print(str(data))
    cur.close()
    return render_template('edit-owner.html', owner=data[0])

@app.route('/update_owner/<string:id>', methods=['GET', 'POST'])
def update_owner(id):
    try:
        if request.method == 'POST':
            cur = db.connection.cursor()
            fname = request.form['fname']
            lname = request.form['lname']
            address = request.form['address']
            phone = request.form['phone']
            if len(phone) != 10:
                cur.execute("SELECT * FROM Owner WHERE ssn={0}".format(id))
                data = cur.fetchall()
                flash("Incorrect phone number format")
                return render_template('edit-owner.html', owner=data[0])
            query = "UPDATE Owner SET first_name='{0}', last_name='{1}', address='{2}', phone='{3}' WHERE ssn='{4}';".format(fname, lname, address, str(phone), id)
            print(query)
            cur.execute(query)
            db.connection.commit()
            flash("Owner Updated Successfully")
            return redirect(url_for('Index'))
    except Exception as e:
        flash(str(e))
        print(request.form)
        cur = db.connection.cursor()
        cur.execute("SELECT * FROM Owner WHERE ssn={0}".format(id))
        data = cur.fetchall()
        return render_template('edit-owner.html', owner=data[0])


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
    return render_template('index.html')

@app.route('/add_gun', methods=['POST'])
def add_gun():
    try:
        if request.method == 'POST':
            cur = db.connection.cursor()
            gun_type = request.form['type']
            ssn = request.form['ssn']
            serial = request.form['serial_number']
            manufacturer = request.form['manufacturer']
            model = request.form['model']
            caliber = request.form['caliber']
            country = request.form['country']
            seller_name = request.form['seller']
            seller_addr = request.form['seller_addr']
            ssn_query = "SELECT EXISTS (SELECT * FROM Gun, Owner WHERE Owner.ssn={0});".format(ssn)
            cur.execute(ssn_query)
            response = cur.fetchall()
            ssn_check = list(response[0].values())
            print(ssn_check[0])
            if len(ssn) != 9:
                flash("Incorrect SSN format")
                return redirect(url_for('Index'))
            if not ssn_check[0]:
                flash("Social Security Number not in Database")
                return redirect(url_for('Index'))
            gun_query = "INSERT INTO Gun VALUES (" + str(serial) + ",'" + gun_type + "'," + str(ssn) + ",'" + model + "','" + caliber + "');"
            seller_query = "INSERT INTO Seller VALUES ('" + seller_name + "','" + seller_addr + "'," + ssn + "," + serial + ");"
            manufacturer_query = "INSERT IGNORE INTO Manufacturer VALUES ('" + manufacturer + "','" + country + "','" + model + "','" + caliber + "');"
            cur.execute(gun_query)
            db.connection.commit()
            cur.execute(seller_query)
            db.connection.commit()
            cur.execute(manufacturer_query)
            db.connection.commit()
            flash('New Firearm Registered')
            return redirect(url_for('Index'))
    except Exception as e:
        flash(str(e))
        return redirect(url_for('Index'))


@app.route('/edit_gun/<string:id>', methods = ['POST', 'GET'])
def edit_gun(id):
    cur = db.connection.cursor()
    query = "SELECT * FROM Gun WHERE serial_number = {0}".format(id)
    cur.execute(query)
    data = cur.fetchall()
    cur.close()
    print(data)
    return render_template('edit-gun.html', gun=data[0])

@app.route('/update_gun/<string:id>', methods = ['POST', 'GET'])
def update_gun(id):
    try:
        if request.method == 'POST':
            print(str(request.form))
            cur = db.connection.cursor()
            gun_type = request.form['type']
            model = request.form['model']
            caliber = request.form['caliber']
            serial = eval(str(id))
            print(type(model))
            cur.execute("SELECT * FROM Manufacturer WHERE model = (SELECT model FROM Gun WHERE serial_number={0});".format(id))
            manu_data = cur.fetchall()
            db.connection.commit()
            gun_query = "UPDATE Gun SET type='" + gun_type + "', model='" + str(model) + "', caliber='" + str(caliber) + "' WHERE serial_number={0};".format(serial)
            cur.execute(gun_query)
            db.connection.commit()
            print(manu_data[0]['name'])
            manufacturer_query = "INSERT IGNORE INTO Manufacturer VALUES ('" + manu_data[0]['name'] + "','" + manu_data[0]['country_of_origin'] + "','" + model + "','" + caliber + "');"
            cur.execute(manufacturer_query)
            db.connection.commit()
            flash("Gun updated successfully")
            return redirect(url_for('Index'))
    except Exception as e:
        cur = db.connection.cursor()
        cur.execute("SELECT * FROM Manufacturer WHERE model = (SELECT model FROM Gun WHERE serial_number={0});".format(id))
        data = cur.fetchall()
        db.connection.commit()
        print(str(e))
        return render_template('edit-gun.html', gun=data[0])


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
