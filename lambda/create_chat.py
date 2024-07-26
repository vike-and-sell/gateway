from shared import get_auth_token, get_body, mould_response
import gateway
import urllib3
http = urllib3.PoolManager()


# PATH: POST /chats


def handler(event, context):
    auth_token = get_auth_token(event)
    body = get_body(event)
    listingId = body.get('listingId')
    result = gateway.create_chat(http, auth_token, listingId)
    return mould_response(result)
