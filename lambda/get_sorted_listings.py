from shared import mould_response, get_auth_token, get_query_params
import gateway
import urllib3
http = urllib3.PoolManager()

# PATH: GET /listings?minPrice=...&maxPrice=...&status=...&sortBy=...&isDescending=...


def handler(event, context):
    auth_token = get_auth_token(event)
    params = get_query_params(event)
    if params:
        max_price = params.get("maxPrice")
        min_price = params.get("minPrice")
        status = params.get("status")
        sort_by = params.get("sortBy")
        is_descending_raw = params.get("isDescending")
        if is_descending_raw == "true":
            is_descending = True
        else:
            is_descending = False
    else:
        max_price = None
        min_price = None
        status = None
        sort_by = None
        is_descending = None
    result = gateway.get_sorted_listings(
        http, auth_token, max_price, min_price, status, sort_by, is_descending)
    return mould_response(result)
