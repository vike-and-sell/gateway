from shared import mould_response, get_auth_token, get_path_params
import gateway
import urllib3
http = urllib3.PoolManager()

# PATH: GET /messages/{chatId}


def handler(event, context):
    auth_token = get_auth_token(event)
    params = get_path_params(event)
    chat_id = params.get('chatId')
    result = gateway.get_messages(http, auth_token, chat_id)
    return mould_response(result)
