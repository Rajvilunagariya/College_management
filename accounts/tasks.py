# accounts/tasks.py

from background_task import background
from django.core.mail import EmailMessage
from django.template.loader import render_to_string
from django.conf import settings
import os

# The @background decorator turns this function into a background task.
# The 'schedule' parameter will be used to tell it when to run.
@background(schedule=0)
def send_approval_email_task(username, email_address):
    """
    A background task to send an approval email with an attachment.
    """
    subject = 'Your Registration has been Approved!'
    context = {'username': username}
    message_body = render_to_string('emails/approval_email.txt', context)

    email = EmailMessage(
        subject,
        message_body,
        settings.DEFAULT_FROM_EMAIL,
        [email_address]
    )

    attachment_path = os.path.join(settings.BASE_DIR, 'attachments', 'welcome_guide.txt')
    email.attach_file(attachment_path)
    
    email.send()
    print(f"Approval email successfully sent to {email_address}")


@background(schedule=0)
def send_rejection_email_task(username, email_address):
    """
    A background task to send a rejection email.
    """
    subject = 'Your Registration Status'
    context = {'username': username}
    message_body = render_to_string('emails/rejection_email.txt', context)

    email = EmailMessage(
        subject,
        message_body,
        settings.DEFAULT_FROM_EMAIL,
        [email_address]
    )
    email.send()
    print(f"Rejection email successfully sent to {email_address}")