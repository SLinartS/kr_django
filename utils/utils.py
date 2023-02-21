import random
import string


def generate_session_id():
    return ''.join(random.choice(
        string.ascii_letters + string.digits) for x in range(20))


def generate_file_url():
    return ''.join(random.choice(
        string.ascii_letters + string.digits) for x in range(40))

def generate_access_code():
    return ''.join(random.choice(
        string.ascii_letters + string.digits) for x in range(20))
