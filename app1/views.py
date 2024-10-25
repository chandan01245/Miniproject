from django.http import HttpResponse
from django.shortcuts import render


# Create your views here.
def login_data(request):
    if request.method == 'POST':
        users = ['chandan']
        #Perform Your checks here
        if request.POST.get("username") in users:
            return render(request, 'Dashboard.html')
        else:
            return render(request,"Login.html",{"errordata":"Enter Valid Details"})
        
    return render(request,"Login.html")


def qr_code(request):
    import os
    import smtplib
    from email import encoders
    from email.mime.base import MIMEBase
    from email.mime.multipart import MIMEMultipart
    from email.mime.text import MIMEText

    import png
    import pyqrcode
    formMail =" "
    formdata =" "
    if request.method == 'POST':
        formMail = request.POST.get("mail")
        formdata = request.POST.get("data")
        string =" "
        # String which represents the QR code
        s = [formdata]
        for i in range(len(s)):
            string += s[i]
        # Generate QR code
        hell = pyqrcode.create(string)

        # Create and save the png file naming "myqr.png"
        hell.png('myqr.png', scale = 6)

        # Email and password for the sender's email account
        sender_email = "thisisatestornotatest@gmail.com"
        password = "bmbhmamziowqeszs"

        # Email details
        receiver_email = formMail
        subject = "QR code test"
        body = "Please find the attached image."

        # Create a multipart message
        msg = MIMEMultipart()
        msg['From'] = sender_email
        msg['To'] = receiver_email
        msg['Subject'] = subject

        # Attach the email body
        msg.attach(MIMEText(body, 'plain'))

        # Specify the image file to attach
        filename = "myqr.png"  # Make sure this file exists in the current directory or provide a full path
        attachment_path = os.path.join(os.getcwd(), filename)

        # Open the image file in binary mode and attach it to the email
        with open(attachment_path, "rb") as attachment:
            part = MIMEBase("application", "octet-stream")
            part.set_payload(attachment.read())

        # Encode the file to base64
        encoders.encode_base64(part)

        # Add header
        part.add_header(
            "Content-Disposition",
            f"attachment; filename={filename}",
        )

        # Attach the file to the message
        msg.attach(part)

        # Set up the SMTP server
        smtp_server = "smtp.gmail.com"  # Use your SMTP server address (e.g., smtp.gmail.com for Gmail)
        smtp_port = 587  # Use 465 for SSL, 587 for TLS

        # Send the email
        server = None  # Define the server before the try block

        try:
            # Create an SMTP session
            server = smtplib.SMTP(smtp_server, smtp_port)
            server.starttls()  # Secure the connection
            server.login(sender_email, password)

            # Send the email
            text = msg.as_string()
            server.sendmail(sender_email, receiver_email, text)
            print("Email sent successfully!")

        except Exception as e:
            print(f"Failed to send email: {e}")

        finally:
            if server:
                server.quit()  # Close the connection properly
    
    return render(request,"patients.html")

def load_vending_machine(request):
    if request.method == 'POST':
        qr_code = request.POST.get("qrCode")
        
        print("QR Code: ",qr_code)
        return HttpResponse("Backend Response: "+qr_code)

    return render(request,"VendingMachine.html")