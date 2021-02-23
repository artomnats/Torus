try:
    import sys
    import smtplib
    import requests
    import email.utils
    from django.conf import settings
    from email.mime.text import MIMEText
    from email.mime.multipart import MIMEMultipart
except ImportError as exception:
    print("%s - Please install the necessary libraries." % exception)
    sys.exit(0)

last_sended_email = {}

def send_email(recipient, subject, text, user_id):
    """
    Send email to recipient with given context.
    Args:
        recipient - email receiver.
        subject - email subject
        text - email body.
        user_id - user id for keeping verification code.
    """
    # Create message container - the correct MIME type is multipart/alternative.
    msg = MIMEMultipart('alternative')
    msg['Subject'] = subject
    msg['From'] = email.utils.formataddr((settings.AWS_S3_SENDERNAME, settings.AWS_S3_SENDER))
    msg['To'] = recipient

    # Record the MIME types of both parts - text/plain and text/html.
    part1 = MIMEText(text, 'plain')
    msg.attach(part1)

    # Try to send the message.
    try:
        server = smtplib.SMTP(settings.AWS_S3_HOST, settings.AWS_S3_PORT)
        server.ehlo()
        server.starttls()
        server.ehlo()
        server.login(settings.SMTP_USERNAME, settings.SMTP_PASSWORD)
        server.sendmail(settings.AWS_S3_SENDER, recipient, msg.as_string())
        server.close()
    # Display an error message if something goes wrong.
    except Exception as e:
        print ("Error: ", e)
    else:
        last_sended_email[user_id] = text.split('-')[-1].strip()
        print ("Email sent!")
