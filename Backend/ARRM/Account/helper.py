EMAIL_REGEX = r"^[^0-9!@#$%^&*(+=)\\[\].></{}`]\w+([\.-_]?\w+)*@ashesi\.edu\.gh$"
PASSWORD_REGEX = r"^(?=(.*[A-Z]){2,})(?=(.*[a-z]){2,})(?=.*\d{2,})(?=.*[!@#$%^&()\-_<>.+]{2,}).{8,}$"


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


def read_user_data(filename):

    with open(filename, "r") as user_data_file:
        user_data_file.readline()       # skip the headers
        user_data = user_data_file.read().splitlines()
        user_data_file.close()
    
    return user_data


def build_account_dict(user_info):

    user_info = user_info.split(",")
    user_account_details = dict()
    user_account_details["employee_id"] = user_info[0].strip()
    user_account_details["firstname"] = user_info[1].strip()
    user_account_details["lastname"] = user_info[2].strip()
    user_account_details["email"] = user_info[3].strip()
    user_account_details["mobile_number"] = user_info[4].strip()
    user_account_details["role"] = user_info[5].strip()
    user_account_details["nationality"] = user_info[6].strip()

    return user_account_details