""" before running this flask app, you have to activate venv
open command prompt, (not powershell)
$ cd project_folder
$ py -m venv .
$ Script/activate
$ py server.py
"""


import os, json, ast, io
import pandas as pd
from flask import Flask, render_template, request, redirect, url_for, make_response, Response
from reportlab.pdfgen import canvas
from reportlab.lib.utils import ImageReader
from reportlab.lib.units import inch
from reportlab.lib.pagesizes import letter
from flask_mysqldb import MySQL
from fileinput import filename 
# import numpy as np


# create db connection config with MYSQL
# app = Flask(__name__, template_folder="templates")
app = Flask(__name__)
app.secret_key = b'_5#y2L"F4Q8z\n\xec]/'
app.config['MYSQL_HOST'] = 'localhost'
app.config["MYSQL_USER"] = 'root'
app.config["MYSQL_PASSWORD"] = ''
app.config["MYSQL_DB"] = 'flask_student'
app.config['UPLOAD_FOLDER'] = 'static/uploads'
app.config['ALLOWED_EXTENSIONS'] = set(['jpg', 'jpeg', 'png'])
mysql = MySQL(app)


PERPAGE = 6


def allowed_file(filename):
    """limit file extension concerned only with photos"""
    return '.' in filename and \
        filename.rsplit('.', 1)[1] in app.config['ALLOWED_EXTENSIONS']


def secure_filename(filename):
    """define secure file name"""
    filename, ext = os.path.splitext(filename)
    filename = ''.join(e for e in filename if e.isalnum())
    filename = filename + ext
    return filename


def get_all_students():
    """get students records from students database"""
    query = 'SELECT * FROM students'
    cur = mysql.connection.cursor()
    cur.execute(query)
    data = cur.fetchall()
    cur.close()
    return data


def create_dynamic_data(studentId):
    """insert data to subjects table with respective student_id"""
    cur = mysql.connection.cursor()
    front_data = {}
    for k,v in request.form.items():
        # loop POST request items into front_data {}
        if k.startswith('maths') or k.startswith('arts') or k.startswith('physics') or k.startswith('year'):
            subject = k.split('_')[0]
            if subject in front_data:
                front_data[subject].append(v)
            else:
                front_data[subject] = [v]
    # print(front_data)
    if front_data:  # if there front_data {} is not empty, this will work
        for i in range(len(front_data['maths'])):
            # print(front_data['maths'], front_data['arts'])
            maths = front_data['maths'][i] if front_data['maths'][i] is not None else ""
            arts = front_data['arts'][i] if front_data['arts'][i] is not None else ""
            physics = front_data['physics'][i] if front_data['physics'][i] is not None else ""
            year = front_data['year'][i] if front_data['year'][i] is not None else ""
            if not maths == '' or arts == '' or physics == '' or year == '':   # check empty string, ''
                cur.execute(
                "INSERT INTO subjects \
                    (maths, arts, physics, year, student_id) \
                    VALUES \
                    (%s , %s, %s, %s, %s)",
                (maths, arts, physics, year, studentId))
                mysql.connection.commit()


def search(keyword=""):
    """search related data"""
    cur = mysql.connection.cursor()
    query = ("""SELECT * FROM students WHERE CONCAT_WS(' ', id, f_name, l_name, nrc, email, phone, address, hobby, city, gender, photo) LIKE %s""")
    cur.execute(query, ('%' + keyword + '%',))
    search_data = cur.fetchall()
    cur.close()
    return search_data


@app.route('/sort/<string:sort_field>/<string:sort_order>', methods=["GET", "POST"])
def sort(sort_field, sort_order):
    """sort data by id asc or desc, can extend if required"""
    data = get_all_students()
    if request.method == "POST":
        keyword = request.form.get('search')
        data = search(keyword)
        return render_template('view.html', student=data, page=1, total_pages=1, keyword=keyword)
    else:
        if sort_field == 'id' and sort_order == 'asc':
            data = sorted(data)
        elif sort_field == 'id' and sort_order == 'desc':
            data = sorted(data, reverse=True)
    return render_template('view.html', student=data, page=1, total_pages=1)


@app.route('/', methods=["GET", "POST"])
@app.route('/index', methods=["GET", "POST"])
def index():
    """index page to create new infomation of a student"""
    # get next student id and sent to index.html for dynamic input
    stu_id = get_all_students()[-1][0] + 1
    filename = ""
    if request.method == "POST":
        create_dynamic_data(stu_id)
        cur = mysql.connection.cursor()
        students = request.form
        f_name = students['f_name']
        l_name = students['l_name']
        nrc = students['nrc']
        email = students['email']
        phone = students['phone']
        address = students['address']
        opt_hobby = request.form.getlist("hobby")
        hobby = (','.join(opt_hobby),)
        city = request.form.get('city')
        gender = request.form.get('gender')
        photo = request.files['photo']
        if photo and allowed_file(photo.filename):
            filename = secure_filename(photo.filename)
            photo.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
        # print(photo)
        cur.execute(
            "INSERT INTO students \
                (f_name, l_name, nrc, email, phone, address, hobby, city, gender, photo) \
                VALUES \
                (%s , %s, %s, %s, %s, %s, %s, %s, %s, %s)",
            (f_name, l_name, nrc, email, phone, address, hobby, city, gender, filename))
        mysql.connection.commit()
        cur.close()
        return redirect("/view_default")
    return render_template("index.html", pic=filename, stu_id=stu_id, form_type="create")


@app.route('/view_default')  # view fist
def view_default():
    """first page of pagination"""
    return redirect(url_for('view', page=1))


@app.route('/view_last')  # view last
def view_last():
    """last page of pagination"""
    data = get_all_students()
    total_rows = len(data)
    total_pages = (total_rows + PERPAGE - 1) // PERPAGE
    return redirect(url_for('view', page=total_pages))


@app.route('/view_all', methods=['GET', 'POST'])  # view all
def view_all():
    """to view all records in a single page."""
    data = get_all_students()
    keyword = request.form.get('search')
    if request.method == "POST":
        keyword = request.form.get('search')
        data = search(keyword)  # can only use under POST method
    return render_template("view.html", student=data, page=1, total_pages=1, keyword=keyword if request.method == "POST" else '')


@app.route('/view/<int:page>', methods=['GET', 'POST'])
def view(page=1):
    """to view page according to pagination page number."""
    data = get_all_students()
    # dict_data = convert_tuple_dict(data)
    total_rows = len(data)
    total_pages = (total_rows + PERPAGE - 1) // PERPAGE
    if request.method == "POST":
        keyword = request.form.get('search')
        data = search(keyword)
        return render_template("view.html", student=data[(page-1)*PERPAGE:page*PERPAGE], keyword=keyword, page=page, total_pages=total_pages)
    return render_template("view.html", student=data[(page-1)*PERPAGE:page*PERPAGE], page=page, total_pages=total_pages)


# display data
@app.route('/<id>/edit')
def edit(id):
    """to display existing student details according to student_id"""
    cur = mysql.connection.cursor()
    cur.execute("SELECT * FROM students WHERE id=%s", (id,))
    student = cur.fetchone()
    # students auto fill data
    if student:
        soption = student[7].split(',')
    else:
        soption = []
    cur.close()
    cur = mysql.connection.cursor()
    cur.execute("SELECT * FROM subjects WHERE student_id=%s", (id,))
    subjects = cur.fetchall()
    # print(subjects)
    if len(subjects) != 0:
        result = [[elem for elem in sublist[:-1]] for sublist in subjects]
        json_data = json.dumps(result)
    else:
        json_data = {}
    cur.close()
    return render_template("index.html", record=student, stu_id=id, json_data=json_data, soption=soption, form_type="update")    


# update values in the database
@app.route('/<id>/update', methods=["POST"])
def update(id):
    """to update information of students and subjects"""
    # create result data [] which contains information of subjects and student_id
    cur = mysql.connection.cursor()
    result = []
    temp = []
    for k, v in request.form.items():
        # print(k, v)
        if not k.startswith(('f_name', 'l_name', 'nrc', 'email', 'phone', 'address', 'city', 'hobby', 'gender', 'stu_id', 'json_data')):
            temp.append(v)
            if 'year' in k:
                temp[-1] = str(temp[-1])
                result.append(temp)
                temp = []
    # subjects data or result data [] is generated by request.form.items()
    json_data = request.form.get('json_data')   # json_data [] sent from /edit and occess here from frontend request.form
    json_data = ast.literal_eval(json_data)
    json_data = [[str(element) for element in sub_list] for sub_list in json_data]
    print("Result", result, "Json Data", json_data)
    subject_list = [lst for lst in result if 'subjectId' in lst[0]]
    if subject_list:
        print("insert section works")
        # when dynamic form add button is clicked, data will fill in subject_list which are new records
        for subject in subject_list:
            maths = subject[1]
            arts = subject[2]
            physics = subject[3]
            year = subject[4]
            if not maths == '' or arts == '' or physics == '' or year == '':
                cur.execute(
                "INSERT INTO subjects \
                    (maths, arts, physics, year, student_id) \
                    VALUES \
                    (%s , %s, %s, %s, %s)",
                (maths, arts, physics, year, id))
                mysql.connection.commit()
    # length json_data and result are compared to update or create new data in subjects
    if len(json_data) <= len(result) or len(json_data) >= len(result):
        # in update section, it contains delete function to control variaous actions
        print("update section works")
        for i, subject in enumerate(result):
            maths = subject[1]
            arts = subject[2]
            physics = subject[3]
            year = subject[4]
            subject_id = subject[0]
            if not maths == '' or arts == '' or physics == '' or year == '':
                cur.execute(
                    "UPDATE subjects \
                    SET maths=%s, arts=%s, physics=%s, year=%s \
                    WHERE subject_id=%s",
                    (maths, arts, physics, year, subject_id))
            for i, subject in enumerate(json_data):
                subject_id = subject[0]
                found = any(subject_id == res_subject[0] for res_subject in result)
                if not found:
                    print("delete section works.")
                    cur.execute("DELETE FROM subjects WHERE subject_id=%s", (subject_id,))
                mysql.connection.commit()
    # all student infomation of students table
    f_name, l_name, nrc, email, phone, address, city, gender = [
    request.form.get(field) for field in ['f_name', 'l_name', 'nrc', 'email', 'phone', 'address', 'city', 'gender']]
    opt_hobby = request.form.getlist("hobby")
    hobby = (','.join(opt_hobby),)
    photo = request.files['photo']
    filename = ""
    # check photo is choosed or not
    if photo and allowed_file(photo.filename):
        filename = secure_filename(photo.filename)
        photo.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
    if filename:
        cur.execute("UPDATE students SET \
            f_name = %s, l_name = %s, nrc = %s, email = %s, \
            phone = %s, address = %s, hobby = %s, city = %s, \
            gender = %s, photo = %s \
            WHERE id = %s",
                    (f_name, l_name, nrc, email, phone, address, hobby, city, gender, filename, id,))
    else:
        cur.execute("UPDATE students SET \
            f_name = %s, l_name = %s, nrc = %s, email = %s, \
            phone = %s, address = %s, hobby = %s, city = %s, \
            gender = %s \
            WHERE id = %s",
                    (f_name, l_name, nrc, email, phone, address, hobby, city, gender, id,))
    mysql.connection.commit()
    cur.close()
    return redirect(url_for("edit", id=id))
    # return redirect(url_for('view_default'))      # want to go to student details, use view_default


@app.route("/<sid>/delete")
def delete(sid):
    """this is the delte route to delete students data in view.html"""
    cur = mysql.connection.cursor()
    cur.execute("DELETE FROM students WHERE id=%s", (sid,))
    mysql.connection.commit()
    cur.close()
    return redirect(url_for('view_all'))


@app.route('/import', methods=['GET', 'POST'])
def import_data():
    """excel import function"""
    if request.method == 'POST':
        file = request.files['file']    # read file using flask request
        data = pd.read_excel(file)      # parse data as pandas data frame type
        data = data.fillna(value="")    # replace NaN Types into ""
        cur = mysql.connection.cursor()
        insert_query = "INSERT INTO students \
        (f_name, l_name, nrc, email, phone, address, hobby, city, gender, photo) \
        VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"
        values = []
        for row in data.itertuples(index=False):
            values.append(tuple(row[1:]))  # remove id from tuple when appending to values []
        for f_name, l_name, nrc, email, phone, address, hobby, city, gender, photo in values:
            cur.execute(insert_query, (f_name, l_name, nrc, email, phone, address, hobby, city, gender, photo),)
        mysql.connection.commit()
        cur.close()
        return redirect(url_for('view_all'))
    return render_template('view.html')


@app.route('/export_excel')
def export_excel():
    """excel export function"""
    data = get_all_students()  # get data from mysql students table
    # Convert result set to pandas data frame and add columns
    df = pd.DataFrame((tuple(t) for t in data),
         columns=('ID', 'First ', 'Last', 'NIC No.', 'Email', 'Phone', 'Address', 'Hobby', 'City', 'Gender', 'Photo' ))
    out = io.BytesIO()  # Creating output and writer (pandas excel writer)
    writer = pd.ExcelWriter(out, engine='xlsxwriter')  # Export data frame to excel
    df.to_excel(excel_writer=writer, index=False, sheet_name='Sheet1')
    writer.save()
    writer.close()
    r = make_response(out.getvalue())  # Flask create response 
    # Defining correct excel headers
    r.headers["Content-Disposition"] = "attachment; filename=export.xlsx"
    r.headers["Content-type"] = "application/x-xls"
    return r  # Finally return response


@app.route('/<int:id>/export_pdf')
def export_pdf(id):
    """pdf export function including formatting pdf layout."""
    cursor = mysql.connection.cursor()
    cursor.execute("SELECT * FROM subjects WHERE student_id=%s", (id,))
    subjects_data = cursor.fetchall()
    cursor.execute("SELECT * FROM students where id=%s", (id,))
    students_data = cursor.fetchone()
    output = io.BytesIO()
    pdf = canvas.Canvas(output, pagesize=letter)
    pdf.setFont("Helvetica-Bold", 14)
    pdf.drawCentredString(300, 750, "Student Information")
    image_url = students_data[10]
    print(os.getcwd())
    if image_url:
        print('image url is not empty')
        # img = ImageReader("uploads/"+image_url)
        # pdf.rect(80, 600, 1.5 * inch, 1.5 * inch, stroke=True, fill=False) # draw a rectangle around the image
        # pdf.drawImage(img, 80, 600, width=1.5, height=1.5)
        image_path = os.path.join(os.path.abspath(os.path.dirname(__file__)), "static/uploads", image_url)
        if os.path.exists(image_path):
            img = ImageReader(image_path)
            pdf.rect(80, 600, 1.5 * inch, 1.5 * inch, stroke=True, fill=False) # draw a rectangle around the image
            pdf.drawImage(img, 80, 600, width=1.5*inch, height=1.5*inch)
        else:
            print(f"Image file {image_path} not found.")
    else:
        print('image url is empty')
        pdf.rect(80, 600, 1.5 * inch, 1.5 * inch, stroke=True, fill=False) # draw a rectangle around the image
    pdf.setFont("Helvetica", 12)
    y = 550
    x = 80  # left student title
    # students data header
    student_info = ["Student ID", "First Name", "Last Name", "NRC", "Email", "Phone", "Address", "Hobby", "City", "Gender"]
    for student in student_info:
        pdf.drawString(x, y, student)
        y -= 30
    pdf.setFont("Helvetica-Bold", 12)
    # students data table
    x = 280  # right student data
    y = 550
    l = 50
    r = 520
    for info in range(len(students_data[:10])):    
        pdf.drawString(x, y, str(students_data[info]))
        y -= 30
    # border of student section
    pdf.rect(l, 50, r, 730, stroke=True, fill=False)
    y -= 20
    if subjects_data:
        if y <= 50:  # go to next page
            pdf.showPage()
        pdf.drawCentredString(300, y, "Subjects")
        pdf.rect(l, y-25, r, 40)
        # subjects data header
        pdf.setFont("Helvetica-Bold", 12)
        print(y)
        x = 80
        y -= 20
        subject_info = ["Subject ID", "Maths", "Arts", "Physics", "Year"]
        for title in subject_info:
            pdf.drawString(x, y, title)
            x += 100
        pdf.rect(l, y-25, r, 40, stroke=True, fill=False)
        y -= 20
        # subjects data table
        pdf.setFont("Helvetica", 12)
        x_values = [80+(i*100) for i in range(5)]
        for row in subjects_data:
            for i, item in enumerate(row[:5]):
                pdf.drawString(x_values[i], y, str(item))
            pdf.rect(l, y-5, r, 20, stroke=True, fill=False)
            y -= 20
    pdf.save()
    output.seek(0)
    response = make_response(output.read())
    response.headers.set('Content-Disposition', 'attachment', filename='export.pdf')
    response.headers.set('Content-Type', 'application/pdf')
    return response


if __name__ == "__main__":
    app.run(debug=True)


"""When user wants to delete each record immediately use this route.
It works with JavaScript Dom. Check in dyanmic_form.js"""
# delete data directly when del-btn in JavaScript is clicked.
# @app.route("/delete", methods = ["POST"])
# def delete_subject():
#     subject_id = request.form['subject_id']
#     cur = mysql.connection.cursor()
#     cur.execute("SELECT * FROM subjects WHERE subject_id = %s", (subject_id,))
#     res = cur.fetchone()
#     student_id = res[-1]
#     print(student_id)
#     cur.execute("DELETE from subjects WHERE subject_id=%s", (subject_id,))
#     mysql.connection.commit()
#     cur.close()
#     return redirect(url_for('edit', id=student_id))


"""If data used in this app are required to convert into dictionary, use this function."""
# def convert_tuple_dict(tuple_data):
#     keys = ['id', 'f_name', 'l_name', 'nrc', 'email', 'phone',
#             'address', 'hobby', 'city', 'gender', 'photo']
#     dict_data = [dict(zip(keys, values)) for values in tuple_data]
#     return dict_data

