import random
import string


def generate_session_id():
    return ''.join(random.choice(
        string.ascii_letters + string.punctuation) for x in range(15))


def generate_file_url():
    return ''.join(random.choice(
        string.ascii_letters) for x in range(50))
