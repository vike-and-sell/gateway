from shared import mould_response, get_auth_token, get_body
import gateway
import urllib3
http = urllib3.PoolManager()

# PATH: GET /listings?minPrice=...&maxPrice=...&status=...&sortBy=...&isDescending=...


def handler(event, context):
    auth_token = get_auth_token(event)
    # TODO: fix this as it's super insecure/definitely exposes critical security vulnerabilities
    result = gateway.get_sorted_listings(
        http, auth_token, event.get('rawQueryString'))
    return mould_response(result)
