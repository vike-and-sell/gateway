from shared import mould_response, get_auth_token, get_path_params, get_body
import gateway
import urllib3
http = urllib3.PoolManager()

# PATH: PATCH /listings/{listingId}


def handler(event, context):
    auth_token = get_auth_token(event)
    params = get_path_params(event)
    listing_id = params.get('listingId')
    body = get_body(event)
    title = params.get('title')
    price = params.get('price')
    address = params.get('location')
    status = params.get('status')
    buyer_username = params.get('buyerUsername')
    result = gateway.update_listing(
        http, auth_token, listing_id, title, price, address, status, buyer_username)
    return mould_response(result)
