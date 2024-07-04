from shared import get_body, mould_response
import gateway
import urllib3
http = urllib3.PoolManager()

# PATH: POST /login


def handler(event, context):
    body = get_body(event)
    username = body.get("username")
    password = body.get("password")
    result = gateway.login(http, username, password)
    return mould_response(result)
