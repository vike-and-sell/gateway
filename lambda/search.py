from shared import mould_response, get_auth_token, get_query_params
import gateway
import urllib3
http = urllib3.PoolManager()

# PATH: GET /search


def handler(event, context):
    auth_token = get_auth_token(event)
    params = get_query_params(event)
    query = params.get('q')
    result = gateway.get_search(http, auth_token, query)
    return mould_response(result)
