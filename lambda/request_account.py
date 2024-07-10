from shared import get_body, mould_response
import gateway
import os
import smtplib
import urllib3
http = urllib3.PoolManager()

# PATH: POST /request_account

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
        result = gateway.request_account(server, email, callback)
        return mould_response(result)
