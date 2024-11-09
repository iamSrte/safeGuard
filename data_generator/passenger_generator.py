import random
from faker import Faker


record_number = 1000

fake = Faker()


def generate_passenger(passenger_index):
    passenger_id = f'{passenger_index:09d}'
    passport = f'{fake.unique.random_number(digits=9):0>9d}'
    first_name = fake.first_name()
    last_name = fake.last_name()
    sex = random.choice(['M', 'F'])
    birthdate = str(fake.date_of_birth(minimum_age=18, maximum_age=90))
    phone_number = f'{fake.unique.random_number(digits=11):0>11d}'
    email_address = fake.email()
    country = fake.country()
    city = fake.city()
    street = fake.street_address()
    zip_code = ''.join(random.choices('0123456789', k=10))

    first_name = first_name.replace("'", "''")
    last_name = last_name.replace("'", "''")
    street = street.replace("'", "''")
    country = country.replace("'", "''")
    city = city.replace("'", "''")

    sql_record = f"('{passenger_id}', '{passport}', '{first_name}', '{last_name}', '{sex}', '{birthdate}', '{phone_number}', '{email_address}', '{country}', '{city}', '{street}', '{zip_code}')"
    return sql_record


passenger_values = [generate_passenger(i) for i in range(1, record_number)]
values_string = ",\n".join(passenger_values)
sql_statement = f"INSERT INTO passengers\n(passenger_id, passport, first_name, last_name, sex, birthdate, phone_number, email_address, country, city, street, zip_code)\nVALUES\n{values_string};"

with open('passengers_inserts.sql', 'w') as file:
    file.write(sql_statement)
    file.close()
