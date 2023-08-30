import logging
import azure.functions as func
import os
from datetime import datetime
import psycopg2
from sendgrid import SendGridAPIClient
from sendgrid.helpers.mail import Mail

# Database connection details
db_host = 'udacitylearning.postgres.database.azure.com:5432'
db_name = 'techconfdb'
db_user = 'phucadmin@udacitylearning'
db_password = 'Abcde12345-+'

ADMIN_EMAIL_ADDRESS = 'tridp.it@gmail.com'
SENDGRID_API_KEY = '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'


def main(msg: func.ServiceBusMessage):

    notification_id = str(msg.get_body().decode('utf-8'))
    logging.info('Python ServiceBus queue trigger processed message: %s', notification_id)

    # TODO: Get connection to database
    conn = psycopg2.connect(host=db_host, dbname=db_name, user=db_user, password=db_password)
    cursor = conn.cursor()

    try:
        # TODO: Get notification message and subject from database using the notification_id
        query = "SELECT subject, message FROM notification WHERE id = %s;"
        cursor.execute(query, (notification_id,))
        result = cursor.fetchone()
        subject = result[0]
        message = result[1]

        # TODO: Get attendees email and name
        query = "SELECT email, first_name FROM attendee;"
        cursor.execute(query)
        attendees = cursor.fetchall()

        # TODO: Loop through each attendee and send an email with a personalized subject
        for attendee in attendees:
            first_name = attendee[0]
            email = attendee[1]
            personalized_subject = subject.replace('{{first_name}}', first_name)
            personalized_message = message.replace('{{first_name}}', first_name)

        send_email(email, personalized_subject, personalized_message)

        # TODO: Update the notification table by setting the completed date and updating the status with the total number of attendees notified
        query = "UPDATE notification SET status = %s, completed_date = %s WHERE id = %s;"
        cursor.execute(query, ('Notified {} attendees'.format(len(attendees)), datetime.utcnow(), notification_id,))

    except (Exception, psycopg2.DatabaseError) as error:
        logging.error(error)
    finally:
        # TODO: Close connection
        conn.commit()
        cursor.close()
        conn.close()


def send_email(email, subject, body):
    message = Mail(
        from_email=ADMIN_EMAIL_ADDRESS,
        to_emails=email,
        subject=subject,
        plain_text_content=body)

    sg = SendGridAPIClient(SENDGRID_API_KEY)
    sg.send(message)