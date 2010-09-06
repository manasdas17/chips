def binary(integer, bits=None):
    """Returns binary string representation of an integer"""
    mask = (1<<(bits-1))
    string = '"'
    while mask:
        if integer & mask:
            string += "1"
        else:
            string += "0"
        mask = mask >> 1
    string += '"'
    return string
