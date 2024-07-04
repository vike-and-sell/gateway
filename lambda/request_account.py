from shared import get_body, mould_response
import gateway
import json
import urllib3
http = urllib3.PoolManager()

# PATH: POST /request_account


def handler(event, context):
    body = get_body(event)
    email = body.get("email")
    callback = body.get("callback")
    result = gateway.request_account(email, callback)
    return mould_response(result)
