"""Flask routes library"""
import hashlib
import socket

HOST, PORT  = "time-b-g.nist.gov", 13

def get_exe_id():
    """
    Return SHA256 checksum of TCP daytime (from time-b-g.nist.gov)
    """
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.connect((HOST, PORT))
        data = bytes()
        while True:
            chunk = s.recv(1024)
            if len(chunk) <= 0:
                break
            data = data + chunk
            
    time_str = data.decode('utf-8').strip() # remove \n and spacing
    exe_id = hashlib.sha256(time_str.encode("utf-8")).hexdigest()
    # print(time_str, exe_id)
    return exe_id

def validate_positive_int_error(input):
    """
    Return True if input is not positive integer, else False
    """
    try:
        if int(input) < 0:
            raise ValueError
    except (ValueError, TypeError):
        return True
    return False

def validate_zero_positive_int_error(input):
    """
    Return True if input is neither zero or positive integer, else False
    """
    try:
        if int(input) <= 0:
            raise ValueError
    except (ValueError, TypeError):
        return True
    return False
