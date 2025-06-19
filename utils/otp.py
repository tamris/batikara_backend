# import random
# from flask_mail import Message
# from flask import current_app

# def generate_otp():
#     return str(random.randint(100000, 999999))

# # def send_otp_email(email, otp):
# #     msg = Message('Your Verification Code', sender=current_app.config['MAIL_USERNAME'], recipients=[email])
# #     msg.body = f'Your OTP code is: {otp}'
# #     current_app.mail.send(msg)
