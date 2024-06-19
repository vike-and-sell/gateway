from flask import Response


def make_response(result):
    return Response(result.get("body"), status=result.get("statusCode"), mimetype="application/json")
