""" This module will generate data in mysql database 'students' table
Script Name: generate_data.py
Date: 18.Feb.2023
Installed Packages: faker, mysql.connector
Author: Tun Tun Nyein

You can change database name in the constructor.
Usage: py <filename.py> <number_of_records>
number_of_records should be the record number you want to input
"""


from faker import Faker
import mysql.connector
import random
import sys


class DataGenerator:
    faker = Faker()
    # If you have connection problems with your database, change these with to your database contents
    def __init__(self, num_records, host='localhost', user='root', password='', database='flask_student'):
        self.num_records = num_records
        self.host = host
        self.user = user
        self.password = password
        self.database = database


    def generate_nrc(self):
        valid_starting_digits = [1, 3, 5, 8, 12, 14]
        random_digit = random.choice(valid_starting_digits)
        random_letters = ''.join(random.choices('ABCDEFGHIJKLMNOPQRSTUVWXYZ', k=3))
        random_digits = ''.join(random.choices('0123456789', k=6))
        return f"{random_digit}/{random_letters}(N){random_digits}"


    def limit_email(self):
        name_words = [word for word in self.faker.name().split() if '.' not in word]
        num_words = self.faker.random_int(min=1, max=min(5, len(name_words)))
        username = name_words[:num_words][0][:6].lower()
        return f'{username}@gmail.com'


    def generate_data(self):
        mydb = mysql.connector.connect(
            host=self.host,
            user=self.user,
            password=self.password,
            database=self.database
        )
        cur = mydb.cursor()
        for i in range(self.num_records):
            f_name = self.faker.first_name() or self.faker.name_male() or self.faker.name_female()
            l_name = self.faker.last_name() or self.faker.name_male() or self.faker.name_female()
            nrc = self.generate_nrc()
            email = self.limit_email()
            phone = self.faker.phone_number().split('x')[0].strip()
            address = self.faker.random_element(elements=("Sanchaung", "Mayangone", "Bahan", "Tamwe", "Kyauk Myaung", "Hlaing"))
            city = self.faker.random_element(elements=("Yangon", "Mandalay", "Myitkyina", "Taunggyi", "Naypyidaw"))
            hobby = self.faker.random_element(elements=("reading", "walking"))
            gender = self.faker.random_element(elements=("male", "female"))
            # If there occurs related to your database table, change INSERT INTO 'students' to your table name.
            sql_query = "INSERT INTO students (f_name, l_name, nrc, email, phone, address, hobby, city, gender) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)"
            try:
                cur.execute(sql_query, (f_name, l_name, nrc, email, phone, address, hobby, city, gender))
                print("Data Insert OK.")
            except mysql.connector.Error as err:
                print(f"Error: {err}")
        cur.close()
        mydb.commit()
        mydb.close()


if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python <filename.py> <number_of_records:int>")
        sys.exit()
    else:
        number_of_records = int(sys.argv[1])
        generator = DataGenerator(number_of_records)
        generator.generate_data()
        

