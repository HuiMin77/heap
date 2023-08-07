import smtplib
import ssl
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import socket
from events.models import Attendance 



def send_QRcode(event):
  port = 465  # For SSL
  smtp_server = "smtp.gmail.com"
  sender_email = "excoverse99@gmail.com"  # Enter your address
  #receiver_email = "xinyi.choo.2021@business.smu.edu.sg"  # Enter receiver address
  password = 'eqqjfbpawcimiqjh'
  event_name = event.name
  
  # Create secure connection with server and send email
  context = ssl.create_default_context()

  attending = Attendance.objects.filter(event = event)

  try:
    with smtplib.SMTP_SSL(smtp_server, port, context=context) as server:
        server.login(sender_email, password)

        for i in attending:
          message = MIMEMultipart("alternative")
          message["Subject"] = event_name
          message["From"] = 'ExcoVerse <excoverse99@gmail.com>'
          print('name of person being sent to:',i.student.first_name)
          receiver_email = i.student.email
          print(receiver_email)

          # Image URL (publicly accessible)
          event_name = str(event.name)
          student_firstname = i.student.first_name
          student_lastname = i.student.last_name
          studentid = str(i.student.student_id)
          information = student_firstname + ' ' + student_lastname + ' ' + studentid + '-' + event_name
          image_url = "https://chart.googleapis.com/chart?chs=200x200&cht=qr&chl=" + information
          

          # Email content with inline image (HTML version)
          html = f"""\
          <html>
            <body>
              <p>Hi {student_firstname},</p>
              <p>You have signed up for {event}!</p>
              <p>Please find your QR code below for scanning your attendance on the day of the event:</p>
              <img src="{image_url}" alt="QR Code">
              <br>
              <a href="{image_url}">Click here for your QR code if the image is not loading</a>
            </body>
          </html>
          """

          # Turn the email content into MIMEText objects
          text = MIMEText(f"Greetings from ExcoVerse!\nYou have signed up for {event}", "plain")
          html_part = MIMEText(html, "html")

          # Attach the text and HTML parts to the email
          message.attach(text)
          message.attach(html_part)
         
          
          server.sendmail(sender_email, receiver_email, message.as_string())
        
  except smtplib.SMTPException as e:
          print(f"Failed to send email to {receiver_email}: {e}")
  except socket.gaierror as e:
      print(f"Failed to connect to SMTP server: {e}")
