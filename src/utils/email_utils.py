"""
  A utility to send emails
"""
import os

import boto3
from src.utils.logger import info


def send_reset_password_email(email=None, auth_key=None):
    """ send reset password email """
    api_host_url = os.environ["API_HOST_URL"]
    reset_password_page_url = "{}{}".format(api_host_url, "reset-password")
    reset_password_api_endpoint = "{}{}".format(api_host_url, "api/v1/user/resetPassword")

    reset_password_link = "{}?nextUrl={}&authKey={}".format(reset_password_page_url, reset_password_api_endpoint, auth_key)
    info(reset_password_link)

    text = "<h3>Reset Your password</h3><p>Please click on the link below to reset your password</p>"
    link = '<p><a class="ulink" href="{}" target="_blank">Click to change Password</a></p>'.format(reset_password_link)
    body_text = "Reset your password by copying the link in new browser`s tab:\n\n {}".format(reset_password_link)
    send_mail(recipient=email, subject="Alethea: Reset Your Password", body_html="{}{}".format(text, link), body_text=body_text)


def send_mail(recipient=None, subject=None, body_html=None, body_text=None):
    """sends email using amazon ses service"""
    sender = os.environ["SES_SOURCE_EMAIL"]
    client = boto3.client("ses")
    charset = "UTF-8"
    client.send_email(
        Destination={"ToAddresses": [recipient]},
        Message={
            "Body": {"Html": {"Charset": charset, "Data": body_html}, "Text": {"Charset": charset, "Data": body_text}},
            "Subject": {"Charset": charset, "Data": subject},
        },
        Source=sender,
    )
