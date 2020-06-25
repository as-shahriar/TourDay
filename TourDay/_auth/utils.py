from django.utils.crypto import get_random_string
import hashlib

def get_code():
    """ Return random 8 character code"""
    code = get_random_string(length=8,allowed_chars='ABCDEFGHIGKLMNOPQRSTWXYZ0123456789')
    return code

def get_hash(value):
    salt = "27a0091dee99016f8fb6599da096feff"
    slated_value = value+salt
    final_value = hashlib.md5(slated_value.encode())
    return final_value.hexdigest()