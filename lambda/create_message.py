from shared import mould_response, get_auth_token, get_body

import gateway
import urllib3
http = urllib3.PoolManager()


def handler(event, context):
    auth_token = get_auth_token(event)
    body = get_body(event)
    chat_id = body.get('chatId')
    content = body.get('content')
    result = gateway.write_message(http, auth_token, chat_id, content)
    return mould_response(result)
