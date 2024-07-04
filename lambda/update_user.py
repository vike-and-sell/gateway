from shared import mould_response, get_auth_token, get_path_params, get_body
import gateway
import urllib3
http = urllib3.PoolManager()

# PATH: PATCH /users/{userId}


def handler(event, context):
    auth_token = get_auth_token(event)
    params = get_path_params(event)
    user_id = params.get('userId')
    body = get_body(event)
    address = body.get('address')
    result = gateway.update_user_by_id(http, auth_token, user_id, address)
    return mould_response(result)
