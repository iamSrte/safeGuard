import random
from faker import Faker
from datetime import timedelta

record_number = 400

fake = Faker()


def generate_flight():
    flight_number = \
        f"{fake.random_uppercase_letter()}{fake.random_uppercase_letter()}{fake.unique.random_number(digits=5):05d}"
    to_country = fake.country()
    to_city = fake.city()
    departure_date_time = fake.date_time_this_decade().replace(microsecond=0)
    departure_date = str(departure_date_time.date())
    departure_time = str(departure_date_time.time())

    arrival_date_time = departure_date_time + timedelta(
        days=0,
        hours=random.randint(1, 9),
        minutes=random.randint(1, 59)
    )
    arrival_date = str(arrival_date_time.date())
    arrival_time = str(arrival_date_time.time())

    to_country = to_country.replace("'", "''")
    to_city = to_city.replace("'", "''")

    sql_record = f"('{flight_number}', '{to_country}', '{to_city}', '{departure_date}', '{departure_time}', '{arrival_date}', '{arrival_time}')"

    return sql_record


flight_values = [generate_flight() for i in range(record_number)]
values_string = ",\n".join(flight_values)
sql_statement = f"INSERT INTO outgoing_flights\n(flight_number, to_country, to_city, departure_date, departure_time, arrival_date, arrival_time)\nVALUES\n{values_string};"

with open('flights_inserts.sql', 'w') as file:
    file.write(sql_statement)
    file.close()
