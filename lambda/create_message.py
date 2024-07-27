from shared import mould_response, get_auth_token, get_body, get_path_params

import gateway
import urllib3
http = urllib3.PoolManager()


def handler(event, context):
    auth_token = get_auth_token(event)
    params = get_path_params(event)
    chat_id = params.get('chatId')
    body = get_body(event)
    content = body.get('content')
    result = gateway.write_message(http, auth_token, chat_id, content)
    return mould_response(result)
