import gateway
from shared import mould_response, get_body
import os
import smtplib

# PATH: POST /request_reset

SMTP_USERNAME = os.environ["SMTP_USERNAME"]
SMTP_PASSWORD = os.environ["SMTP_PASSWORD"]
SMTP_SERVER = os.environ["SMTP_SERVER"]
SMTP_PORT = int(os.environ["SMTP_PORT"])


def handler(event, context):
    body = get_body(event)
    email = body.get("email")
    callback = body.get("callback")
    with smtplib.SMTP_SSL(SMTP_SERVER, SMTP_PORT) as server:
        server.login(SMTP_USERNAME, SMTP_PASSWORD)
        result = gateway.request_reset(server, email, callback)
        return mould_response(result)
