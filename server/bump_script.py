from database.user import list_users
from framework.database import make_db_connection, close_db_connection
from framework.mail import send_mail


db_conn = make_db_connection()

users = list_users(db_conn, {})

for user in users:
    send_mail(
        subject='Welcome to Sagefy',
        recipient=user['email'],
        body="""
        Welcome to Sagefy!

        If you are interested in biweekly updates on Sagefy's progress,
        sign up at http://newsletter.sagefy.org/up

        Thank you!
        """
    )

close_db_connection(db_conn)
