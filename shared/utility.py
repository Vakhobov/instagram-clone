
import re
import threading
from twilio.rest import Client

import config
import phonenumbers
from decouple import config

from django.core.mail import EmailMessage
from django.template.loader import render_to_string
from rest_framework.exceptions import ValidationError

email_regex = re.compile(r"^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$")
phone_regex = re.compile(r"^\+?(\d{1,3})?[-.\s]?\(?\d{2,4}\)?[-.\s]?\d{3,4}[-.\s]?\d{4}$")
username_regex = re.compile(r"^[a-zA-Z0-9_.-]+$")

def check_email_or_phone(email_or_phone):
    # phone_number = phonenumbers.parse(email_or_phone)
    if re.fullmatch(email_regex, email_or_phone):
        return 'email'

    try:
        parsed_number = phonenumbers.parse(email_or_phone, None)
        if phonenumbers.is_valid_number(parsed_number):
            return "phone"
    except phonenumbers.NumberParseException:
        pass

        # If neither email nor phone, raise a validation error
    raise ValidationError(
        {
            "success": False,
            "message": "You must enter a valid email or phone number.",
           }
    )


def check_user_type(user_input):
    # phone_number = phonenumbers.parse(user_input)

    if re.fullmatch(email_regex, user_input):
        user_input = 'email'
    elif re.fullmatch(phone_regex, user_input):
        user_input = 'phone'
    elif re.fullmatch(username_regex, user_input):
        user_input = 'username'
    else:
        data = {
            "success": False,
            "message": "Email, username yoki telefon raqam noto'g'ri"
        }
        raise ValidationError(data)
    return user_input


class EmailThread(threading.Thread):
    def __init__(self, email):
        self.email = email
        threading.Thread.__init__(self)

    def run(self):
        self.email.send()


class Email:
    @staticmethod
    def sent_email(data):
        email = EmailMessage(
            subject=data['subject'],
            body=data['body'],
            to=[data['to_email']]
        )
        if data.get('content_type') == "html":
            email.content_subtype = "html"
        EmailThread(email).start()

def send_email(email, code):
    html_content = render_to_string(
        'email/authentication/activate_account.html',
        {"code": code}
    )
    Email.sent_email(
        {
            "subject": "Ro'yxatdan o'tish",
            "to_email": email,
            "body": html_content,
            "content_type": "html"
        }
    )

def send_phone_code(phone, code):
    account_sid = config('account_sid')
    auth_token = config('auth_token')
    client = Client(account_sid, auth_token)
    client.messages.create(
        body=f"Salom sizning tasdiqlash Kodingiz: {code}\n",
        from_='+998904703372',
        to=f"+{phone}"
    )
