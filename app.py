from flask import Flask
from flaskext.mysql import MySQL
#from flask_mysqldb import MySQL

app = Flask(__name__)
mysql = MySQL()
app.config['MYSQL_DATABASE_USER'] = 'root'
app.config['MYSQL_DATABASE_PASSWORD'] = 'SnowCatter1995!'
app.config['MYSQL_DATABASE_DB'] = 'firearms'
app.config['MYSQL_DATABASE_HOST'] = 'localhost'
mysql.init_app(app)


@app.route('/')
def users():
    conn = mysql.connect()
    cursor = conn.cursor()
    cursor.execute("SELECT * from owners")
    data = cursor.fetchall()
    return str(data)


if __name__ == '__main__':
    app.debug = True
    app.run()
    app.run(debug=True)
