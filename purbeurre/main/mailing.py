import time
from celery import shared_task
from django.contrib import messages
from django.core.mail import EmailMultiAlternatives




@shared_task
def mailer(const):
    subject = const.get('subject')
    text_content = const.get('content')
    from_email = const.get('from_email')
    to = const.get('email')
    html_content = const.get('html_content')
    msg = EmailMultiAlternatives(subject, text_content, from_email, [to])
    msg.attach_alternative(html_content, "text/html")
    msg.send()
    print('EMAIL SENDED')
    return True