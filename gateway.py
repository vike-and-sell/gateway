import os
import json
import urllib3
http = urllib3.PoolManager()

DATA_URL = os.environ["GATEWAY_DATA_URL"]

def get_listing_by_id(auth_token, listing_id):
    # TODO: implement get_listing_by_id
    return None


def not_implemented():
    return {
        "statusCode": 501,
        "body": json.dumps({
            "message": "NOT IMPLEMENTED"
        })
    }