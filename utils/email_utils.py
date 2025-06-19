import random
from flask_mail import Message
from flask import current_app, render_template_string

def generate_otp():
    return str(random.randint(100000, 999999))

def send_email(email, otp):
    subject = "Kode Verifikasi BatikKara Anda"
    # body = f"Your OTP code is {otp}. It will expire in 5 minutes."

    # HTML template untuk tampilan email yang lebih menarik
    html = render_template_string(""" 
    <html>
    <body style="font-family: Arial, sans-serif; color: #333; background-color: #f4f4f4; padding: 20px;">
        <div style="max-width: 600px; margin: auto; padding: 20px; background-color: #ffffff; border-radius: 8px; box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1);">

            <!-- Header -->
            <div style="background-color: #C14A6C; padding: 10px 20px; border-radius: 8px 8px 0 0; color: #ffffff; text-align: center;">
                <h2 style="margin: 0;">Kode Verifikasi (OTP)</h2>
            </div>

            <!-- Body -->
            <div style="padding: 20px; text-align: center;">
                <p>Halo,</p>
                <p>Berikut adalah kode OTP untuk verifikasi alamat email Anda. Kode ini hanya berlaku selama <strong>5 menit</strong>.</p>
                
                <div style="font-size: 24px; font-weight: bold; margin: 20px auto; padding: 10px 20px; display: inline-block; background-color: #f0f0f0; border: 2px dashed #C14A6C; border-radius: 8px;">
                    {{ otp }}
                </div>

                <p style="margin-top: 30px; font-size: 12px; color: #777;">
                    Jika Anda tidak meminta kode ini, silakan abaikan email ini.
                </p>
            </div>
        </div>
    </body>
    </html>
    """, otp=otp)


    msg = Message(subject=subject,
                  sender=current_app.config['MAIL_USERNAME'],
                  recipients=[email])
    
    # msg.body = body  # Fallback untuk client email non-HTML
    msg.html = html  # Versi HTML

    current_app.mail.send(msg)
