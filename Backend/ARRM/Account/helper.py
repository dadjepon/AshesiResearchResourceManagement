from os import path
from magic import from_buffer
from django.core.mail import EmailMultiAlternatives, BadHeaderError


# EMAIL_REGEX = r"^[^0-9!@#$%^&*(+=)\\[\].></{}`]\w+([\.-_]?\w+)*@(ashesi\.edu\.gh|aucampus\.onmicrosoft\.com)$"
EMAIL_REGEX = r"^[^0-9!@#$%^&*(+=)\\[\].></{}`]\w+([\.-_]?\w+)*@([a-z\d-]+)\.([a-z]{2,})(\.[a-z]{2,})?$"
PASSWORD_REGEX = r"^(?=(.*[A-Z]){2,})(?=(.*[a-z]){2,})(?=(.*\d){2,})(?=(.*[!#$%&()*+,-.:;<=>?@_~]){2,}).{8,}$"


def read_country_file(filename):
    """
    COUNTRY FILE COLUMNS:
        COUNTRY_NAME, COUNTRY_CODE, INT_DIALING
    """

    COUNTRY_CODES = dict()
    country_file = open(filename, "r")

    # skip the first line (headers)
    country_file.readline()

    COUNTRY_NAME_INDEX = 0
    INT_DIALING_INDEX = 1

    for line in country_file:
        line = line.split(",")
        
        # currently countries that have multiple dialing codes are not supported
        # so we only take the first one     ==>     change this later
        if line[-1] != '':
            COUNTRY_CODES[line[COUNTRY_NAME_INDEX].strip().lower()] = f"+{line[INT_DIALING_INDEX].strip()}"

    country_file.close()
    return COUNTRY_CODES


def read_user_data(user_data_file):
    # function expects an already opened file (InMemoryUploadedFile)

    user_data_file.readline()       # skip the headers
    user_data = user_data_file.read().splitlines()
    user_data_file.close()
    
    return user_data


import random
import string

def generate_password():
    """
    generates a random password for a user
    password generated is at least 8 characters long and must contain:
        - 2 uppercase letters
        - 2 lowercase letters
        - 2 digits
        - 2 special characters
    """
    uppercase_chars = random.choices(string.ascii_uppercase, k=2)
    lowercase_chars = random.choices(string.ascii_lowercase, k=2)
    digit_chars = random.choices(string.digits, k=2)
    special_chars = random.choices('!#$%&()*+,-.:;<=>?@_~', k=2)

    all_chars = uppercase_chars + lowercase_chars + digit_chars + special_chars

    # while len(all_chars) < 8:
    #     all_chars.append(random.choice(string.ascii_letters + string.digits + string.punctuation))

    random.shuffle(all_chars)
    password = ''.join(all_chars)
    return password


def build_account_dict(user_info):
    password = generate_password()

    user_info = user_info.decode("utf-8").split(",")
    user_account_details = dict()
    user_account_details["firstname"] = user_info[0].strip()
    user_account_details["lastname"] = user_info[1].strip()
    user_account_details["email"] = user_info[2].strip()
    user_account_details["mobile_number"] = user_info[3].strip()
    user_account_details["role"] = user_info[4].strip()
    user_account_details["nationality"] = user_info[5].strip()
    user_account_details["password"] = password
    user_account_details["confirm_password"] = password

    return user_account_details


def disseminate_email(subject, message, sender, recipient_list, attachment_path=None):
    """
    sends an email to the recipient_list
    """

    try:
        email = EmailMultiAlternatives(subject, '', sender, recipient_list)
        email.attach_alternative(message, "text/html")

        if attachment_path:
            with open(attachment_path, "rb") as attachment:
                content = attachment.read()

            mime_type = from_buffer(content, mime=True)
            filename = path.basename(attachment_path)
            email.attach(filename, content, mime_type)

        email.send()
    except BadHeaderError:
        return None            