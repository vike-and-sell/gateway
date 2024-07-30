from shared import mould_response, get_auth_token, get_path_params
import gateway
import urllib3
http = urllib3.PoolManager()

# PATH: POST /recommendations/{listingId}/ignore


def handler(event, context):
    auth_token = get_auth_token(event)
    params = get_path_params(event)
    listing_id = params.get('listingId')
    result = gateway.ignore_listing(http, auth_token, listing_id)
    return mould_response(result)
