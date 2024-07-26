from shared import mould_response, get_auth_token, get_query_params
import gateway
import urllib3
http = urllib3.PoolManager()

# PATH: GET /search


def handler(event, context):
    auth_token = get_auth_token(event)
    params = get_query_params(event)
    query = params.get('q')
    max_price = params.get('maxPrice')
    min_price = params.get('minPrice')
    status = params.get('status')
    sort_by = params.get('sortBy')
    is_descending = params.get('isDescending')
    if is_descending == "true":
        is_descending = True
    else:
        is_descending = False
    if min_price:
        min_price = float(min_price)
    if max_price:
        max_price = float(max_price)

    result = gateway.get_search(http, auth_token, query, min_price, max_price, status, sort_by, is_descending)
    return mould_response(result)
