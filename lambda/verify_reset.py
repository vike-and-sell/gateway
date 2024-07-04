from shared import mould_response, get_body
import gateway
import urllib3
http = urllib3.PoolManager()

# PATH: POST /verify_reset


def handler(event, context):
    body = get_body(event)
    token = body.get('jwt')
    password = body.get('password')
    result = gateway.verify_reset(http, token, password)
    return mould_response(result)
