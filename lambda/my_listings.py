from shared import mould_response, get_auth_token
import gateway
import urllib3
http = urllib3.PoolManager()

# PATH: GET /listings/me


def handler(event, context):
    auth_token = get_auth_token(event)
    result = gateway.get_my_listings(http, auth_token)
    return mould_response(result)
