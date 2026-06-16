import string
import secrets


def generate_secure_otp(length=6):

    pool = string.ascii_uppercase + string.digits

    return "".join(secrets.choice(pool) for _ in range(length))
