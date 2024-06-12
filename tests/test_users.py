from mockito import when, mock
import urllib3
import json
from test_utils import sign_jwt_for_test

import gateway


def test_get_id():
    http = mock(urllib3.PoolManager())

    response = mock({
        "status": 200,
    })
    when(response).json().thenReturn({
        "title": "Test Listing"
    })
    when(http).request(...).thenReturn(response)
    token = sign_jwt_for_test({
        "uid": 1234
    })

    assert gateway.get_user_by_id(http, token, 5678) == {
        "statusCode": 200,
        "body": json.dumps({
            "title": "Test Listing"
        })
    }
