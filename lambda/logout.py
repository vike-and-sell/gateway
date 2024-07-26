from shared import get_body, mould_response
import gateway
import urllib3
http = urllib3.PoolManager()

# PATH: DELETE /login


def handler(event, context):
    result = gateway.logout()
    return mould_response(result)
