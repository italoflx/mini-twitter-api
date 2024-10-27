from django.core.mail import send_mail
from django.conf import settings
from celery import Celery

app = Celery('my_tasks', broker='redis://localhost:6379/0')

@app.task
def send_follow_notification(follower_username, followed_username, followed_email):
    try:
        subject = f'{followed_username} You have a new follower!'
        message = f'{follower_username} started following you!'
        recipient_list = [followed_email]

        print(subject, message, recipient_list)
        
        send_mail(subject, message, settings.DEFAULT_FROM_EMAIL, recipient_list)
    except Exception as e:
        print(f"Error sending email: {e}")