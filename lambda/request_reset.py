from shared import mould_response, get_body
import gateway

# PATH: POST /request_reset


def handler(event, context):
    body = get_body(event)
    email = body.get("email")
    callback = body.get("callback")
    result = gateway.request_reset(email, callback)
    return mould_response(result)
