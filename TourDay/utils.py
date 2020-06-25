import threading
from django.core.mail import send_mail
from time import sleep

def threading_send_mail(subject,message,EMAIL_HOST_USER,user_email):
    send_mail(subject, message, EMAIL_HOST_USER, [user_email], fail_silently = True)
    
def async_send_mail(subject,message,EMAIL_HOST_USER,user_email):
    """ use thread to send mail """
    thread = threading.Thread(target=threading_send_mail,args=[subject,message,EMAIL_HOST_USER,user_email])
    thread.start()
