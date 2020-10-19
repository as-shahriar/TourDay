import string
import random
import threading
from django.core.mail import send_mail
from time import sleep

districts = {

"Bagerhat" : "26",
"Bandarban" : "56",
"Barguna" : "32",
"Barisal" : "31",
"Bhola" : "37",
"Bogra" : "11",
"Brahmanbaria" : "41",
"Chandpur" : "44",
"Chapainawabganj" : "10",
"Chattogram" : "54",
"Chuadanga" : "25",
"Comilla" : "43",
"Cox's Bazar" : "59",
"Dhaka" : "73",
"Dinajpur" : "4",
"Faridpur" : "70",
"Feni" : "51",
"Gaibandha" : "7",
"Gazipur" : "76",
"Gopalganj" : "71",
"Habiganj" : "64",
"Jamalpur" : "66",
"Jessore" : "19",
"Jhalokati" : "30",
"Jhenaidah" : "17",
"Joypurhat" : "16",
"Khagrachhari" : "55",
"Khulna" : "22",
"Kishoreganj" : "83",
"Kurigram" : "6",
"Kushtia" : "23",
"Lakshmipur" : "45",
"Lalmonirhat" : "3",
"Madaripur" : "75",
"Magura" : "18",
"Manikganj" : "72",
"Meherpur" : "24",
"Moulvibazar" : "65",
"Munshiganj" : "79",
"Mymensingh" : "67",
"Naogaon" : "15",
"Narail" : "20",
"Narayanganj" : "78",
"Narsingdi" : "77",
"Natore" : "12",
"Netrokona " : "68",
"Nilphamari" : "0",
"Noakhali" : "46",
"Pabna" : "9",
"Panchagarh" : "1",
"Patuakhali" : "33",
"Pirojpur" : "29",
"Rajbari" : "69",
"Rajshahi" : "13",
"Rangamati" : "57",
"Rangpur" : "5",
"Satkhira" : "21",
"Shariatpur" : "74",
"Sherpur" : "66a",
"Sirajganj" : "14",
"Sunamganj" : "62",
"Sylhet" : "63",
"Tangail" : "84",
"Thakurgaon" : "2",

}


def threading_send_mail(subject, message, EMAIL_HOST_USER, user_email):
    send_mail(subject, message, EMAIL_HOST_USER,
              [user_email], fail_silently=True)


def async_send_mail(subject, message, EMAIL_HOST_USER, user_email):
    """ use thread to send mail """
    thread = threading.Thread(target=threading_send_mail, args=[
                              subject, message, EMAIL_HOST_USER, user_email])
    thread.start()


def number_to_location(number):
    """Take number and return location"""
    return list(districts.keys())[list(districts.values()).index(number)]


def get_random_string(length):
    letters = string.ascii_lowercase
    result_str = ''.join(random.choice(letters) for i in range(length))
    return result_str
