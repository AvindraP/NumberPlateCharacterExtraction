import firebase_admin
from firebase_admin import credentials, firestore
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from datetime import datetime

# Initialize Firebase Admin SDK
cred = credentials.Certificate('serviceAccountKey.json')
firebase_admin.initialize_app(cred)

# Initialize Firestore database
db = firestore.client()

# Define a function to retrieve email based on vehicle number
def get_email_by_vehicle_number(vehicle_number):
    try:
        # Query Firestore to retrieve documents where vehicle_number equals the given value
        query = db.collection('details').where('vehicle_number', '==', vehicle_number).limit(1).get()

        # Iterate over the query results (there should be only one document)
        for doc in query:
            # Access the 'email' field of the document and return it
            return doc.to_dict().get('email')

    except Exception as e:
        print(f"Error retrieving email from Firestore: {e}")
        return None

def searchVehicleNumber(vehicle_number_to_search):

    # Retrieve the email associated with the vehicle number
    email = get_email_by_vehicle_number(vehicle_number_to_search)
    
    if email:
        print(f"The email associated with vehicle number '{vehicle_number_to_search}' is: {email}")
        print(f"Printing email for verification '{email}'")
        sendEmail(email)
    else:
        print(f"No email found for vehicle number '{vehicle_number_to_search}'")


def sendEmail(email):

    smtp_server = "mail.profitbank365.com"
    port = 465
    username = "pasan@profitbank365.com"
    password = "Teacher@123$"
    sender_name = "Sri Lanka Traffic Management System"
    
    current_datetime = datetime.now()
    current_date = current_datetime.strftime("%Y-%m-%d")
    current_time = current_datetime.strftime("%H:%M")
    
    msg = MIMEMultipart()
    msg['From'] = f"{sender_name} <{username}>"
    msg['To'] = email
    msg['Subject'] = "Traffic rule violation fine"
    
    message =  f"You have violated the helmet wearing traffic rule on the date of {current_date} at {current_time}. Please visit the nearest police station within 7days or pay the fine online"
    msg.attach(MIMEText(message, 'plain'))
    
    try:
        server = smtplib.SMTP_SSL(smtp_server, port)
        server.login(username, password)
        server.sendmail(msg['From'], msg['To'], msg.as_string())
        server.quit()
        print("Email sent successfully.")
    except Exception as e:
        print(f"An error occurred while sending the email: {e}")


def saveViolator(vehicle_number):
    try:
        violation_category = "Helmet wearing rule"
        current_datetime = datetime.now()
        current_date = current_datetime.strftime("%Y-%m-%d")
        current_time = current_datetime.strftime("%H:%M")

        doc_ref = db.collection('violations').document()
        doc_ref.set({
            'id': doc_ref.id,  # Include the auto-generated ID
            'vehicle_number': vehicle_number,
            'date': current_date,
            'time': current_time,
            'violation_Category': violation_category,
        })

        print("Violator data saved successfully.")
    except Exception as e:
        print(f"An error occurred while saving violator data: {e}")