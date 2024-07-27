from shared import mould_response, get_auth_token, get_body
import gateway
import urllib3
http = urllib3.PoolManager()

# PATH: PATCH /users/me


def handler(event, context):
    auth_token = get_auth_token(event)
    body = get_body(event)
    address = body.get('location')
    result = gateway.update_user(http, auth_token, address)
    return mould_response(result)
