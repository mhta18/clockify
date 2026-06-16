from django.core.mail import send_mail


def send_otp_email(email, code):
    send_mail(
        subject="Your Login Code",
        message=f"Your login code is: {code}",
        from_email="m@gmail.com",
        recipient_list=[email],
    )
