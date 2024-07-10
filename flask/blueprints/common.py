from flask import Response


def make_response(result: dict):
    resp = Response(result.get("body"), status=result.get(
        "statusCode"))
    auth = result.get("auth")
    if auth:
        jwt = auth["jwt"]
        expiration = auth["exp"]
        resp.set_cookie('Authorization', jwt,
                        expires=expiration, httponly=True, samesite="None", secure=False)

    return resp
