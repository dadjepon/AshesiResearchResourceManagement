def read_country_file():
    """
    
    """

    COUNTRY_CODES = dict()
    country_file = open("country-codes.csv", "r")

    # skip the first line (headers)
    country_file.readline()

    """
    COUNTRY FILE COLUMNS:
    COUNTRY_NAME, COUNTRY_CODE, INT_DIALING
    """

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