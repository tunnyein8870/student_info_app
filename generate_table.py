"""
Script Name: generate_table.py
Date: 19.Feb.2023
Installed Packages: flask, flask_mysqldb
Author: Tun Tun Nyein

Create students database that is corresponds to server.py
Change Database name from 'project' to 'students' on app.config['MYSQL_DB] = 'project'
run $py generate_table.py
goto browser and enter url, localhost:5500/create_students_table
Check your database. If you want to generate data, check generate_data.py
"""

from flask import Flask
from flask_mysqldb import MySQL

app = Flask(__name__)
app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = ''
app.config['MYSQL_DB'] = 'project'
mysql = MySQL(app)

class Create_DB:
    def __init__(self, app):
        self.app = app
        self.mysql = MySQL(app)

    def create_students_table(self):
        try:
            cur = self.mysql.connection.cursor()
            cur.execute("""
                CREATE TABLE students (
                    id INT AUTO_INCREMENT PRIMARY KEY,
                    f_name VARCHAR(50),
                    l_name VARCHAR(50),
                    nrc VARCHAR(50),
                    email VARCHAR(50),
                    phone VARCHAR(50),
                    address VARCHAR(100),
                    hobby VARCHAR(50),
                    city VARCHAR(20),
                    gender VARCHAR(20),
                    photo VARCHAR(50)
                )
            """)
            self.mysql.connection.commit()
            cur.close()
            return 'Table created!'
        except Exception as e:
            return str(e)

db_name = Create_DB(app)

@app.route('/create_students_table')
def create_students_table():
    return db_name.create_students_table()

if __name__ == '__main__':
    app.run(port=5500, debug=True)
