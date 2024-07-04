from shared import mould_response, get_auth_token, get_path_params, get_body
import gateway
import urllib3
http = urllib3.PoolManager()

# PATH: POST /rating/{listingId}


def handler(event, context):
    auth_token = get_auth_token(event)
    params = get_path_params(event)
    listing_id = params.get('listingId')
    body = get_body(event)
    value = body.get('ratingValue')
    result = gateway.post_rating_by_listing_id(
        http, auth_token, listing_id, value)
    return mould_response(result)
