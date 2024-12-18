import smtplib
from datetime import datetime

from pymongo import MongoClient

# Connect to MongoDB
client = MongoClient("mongodb://localhost:27017/")
db = client['appointment_db']
appointments = db['appointments']


# Function to save an appointment in MongoDB
def save_appointment(register_object):
    Date = register_object.Date.strftime("%Y-%m-%d")
    mail = register_object.mail
    remainder(Date,mail)
    appointment_data = {
        "name": register_object.name,
        "phone": register_object.phone,
        "mail": register_object.mail,
        "Date": register_object.Date.strftime("%Y-%m-%d"),
        "Reason": register_object.Reason
    }
    result = appointments.insert_one(appointment_data)


def remainder(appointment_date,formMail):
    print(f" date: {appointment_date}")

    # Email and password for the sender's email account
    sender_email = "thisisatestornotatest@gmail.com"
    password = "bmbhmamziowqeszs"

    # Email details
    receiver_email = formMail
    subject = "Appointment Reminder"
    body = f"You have an appointment scheduled on {appointment_date}."
    message = f"Subject: {subject}\n\n{body}"

    with smtplib.SMTP('smtp.gmail.com', 587) as connection:
        connection.starttls()
        connection.login(user=sender_email, password=password)
        connection.sendmail(from_addr=sender_email, to_addrs=receiver_email,msg=message)



