from http.cookies import SimpleCookie
import json


def get_auth_token(event):
    cookies = event.get("cookies")
    if cookies:
        for cookie in cookies:
            if cookie.startswith("Authorization"):
                return cookie.split("=")[1]


def get_body(event) -> dict:
    return json.loads(event.get('body'))


def get_path_params(event):
    return event.get('pathParameters')


def get_query_params(event):
    return event.get('queryStringParameters')


def mould_response(gateway_response):
    response = {}
    response["statusCode"] = gateway_response.get("statusCode")

    headers = gateway_response.get("headers")
    if not headers:
        headers = {}
    headers["Access-Control-Allow-Origin"] = "*"
    response["headers"] = headers

    body = gateway_response.get("body")
    if body:
        response["body"] = body

    auth = gateway_response.get("auth")
    if auth:
        c = SimpleCookie()
        c["Authorization"] = auth["jwt"]
        c["Authorization"]["expires"] = 10800  # 3 hours in seconds
        c["Authorization"]["samesite"] = "None"
        c["Authorization"]["httponly"] = True
        c["Authorization"]["secure"] = True
        c["Authorization"]["path"] = "/"
        response["cookies"] = [c.output(header="")]

    print("response:")
    print(response)
    return response
