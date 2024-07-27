from shared import mould_response, get_body
import gateway
import urllib3
http = urllib3.PoolManager()

# PATH: POST /verify_account


def handler(event, context):
    body = get_body(event)
    token = body.get('jwt')
    username = body.get('username')
    password = body.get('password')
    address = body.get('location')
    result = gateway.verify_account(http, token, username, password, address)
    return mould_response(result)
