from datetime import datetime

from pymongo import MongoClient

# Connect to MongoDB
client = MongoClient("mongodb://localhost:27017/")
db = client['appointment_db']
appointments = db['appointments']

# Function to save an appointment in MongoDB
def save_appointment(register_object):
    appointment_data = {
        "name": register_object.name,
        "phone": register_object.phone,
        "mail": register_object.mail,
        "Date": register_object.Date.strftime("%Y-%m-%d"),
        "Reason": register_object.Reason
    }
    result = appointments.insert_one(appointment_data)

