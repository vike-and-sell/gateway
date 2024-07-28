from shared import get_auth_token, mould_response
import gateway
import urllib3
http = urllib3.PoolManager()


def handler(event, context):
    auth_token = get_auth_token(event)
    result = gateway.get_charities(http, auth_token)
    return mould_response(result)
