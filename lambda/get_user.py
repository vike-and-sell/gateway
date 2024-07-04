from shared import mould_response, get_auth_token, get_path_params
import gateway
import urllib3
http = urllib3.PoolManager()

# PATH: GET /users/{userId}


def handler(event, context):
    auth_token = get_auth_token(event)
    params = get_path_params(event)
    user_id = params.get('userId')
    result = gateway.get_user_by_id(http, auth_token, user_id)
    return mould_response(result)
