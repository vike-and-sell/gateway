from shared import mould_response, get_auth_token, get_path_params, get_body
import gateway
import urllib3
http = urllib3.PoolManager()

# PATH: POST /review/{listingId}


def handler(event, context):
    auth_token = get_auth_token(event)
    params = get_path_params(event)
    listing_id = params.get('listingId')
    body = get_body(event)
    content = body.get('reviewContent')
    result = gateway.post_review_by_listing_id(
        http, auth_token, int(listing_id), content)
    return mould_response(result)
