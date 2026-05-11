import random
import string


def generate_otp(length=6):
    char = string.ascii_uppercase + string.digits
    return "".join(random.choice(char) for _ in range(length))
