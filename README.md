# student_info_app
A CRUD application with search, pagination, excel import &amp; export, dynamic form... Using Python (Flask), JavaScript, HTML/CSS/Bootstrap
Faker is used to generate data.

.. | A local server is required. This module uses MySQL using Xampp. |

# Required modules:
$ pip install Flask
$ pip install flask_mysqldb
$ pip install mysql-connector-python
$ pip install pandas
$ pip install reportlab

# Create a database and to generate table check the following generate_table file for database customization. For data, check module comments in generate_data file.
# If you don't want to create, import sql in phpMyAdmin of Mysql.

For fake data: 
$ py generate_table.py
$ py generate_data.py

# Run app
$ py server.py or python server.py or python3 server.py

$ Dynamic form uses Javascript DOM to control class names.
## Note! every images uploaded in the form view will be saved in the static/uploads folder.





