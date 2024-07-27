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
    title = body.get('title')
    price = body.get('price')
    address = body.get('location')
    status = body.get('status')
    buyer_username = body.get('buyerUsername')
    charity = body.get('forCharity')
    result = gateway.update_listing(
        http, auth_token, listing_id, title, price, address, status, buyer_username, charity)
    return mould_response(result)
