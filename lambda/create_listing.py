from shared import mould_response, get_auth_token, get_body
import gateway
import urllib3
http = urllib3.PoolManager()

# PATH: POST /listings


def handler(event, context):
    auth_token = get_auth_token(event)
    body = get_body(event)
    title = body.get('title')
    price = body.get('price')
    address = body.get('location')
    charity = body.get('forCharity')
    result = gateway.create_listing(http, auth_token, title, price, address, charity)
    return mould_response(result)
