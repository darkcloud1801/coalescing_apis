from httpx import Response
from httpx._models import Request


def create_mock_response(json_data, status_code=200):
    """Helper function to create a mock httpx.Response."""
    return Response(
        status_code=status_code,
        request=Request("GET", "http://mockapi"),  # Dummy request object
        json=json_data,
    )


async def async_side_effect_1(url, *args, **kwargs):
    if "api1" in url:
        return create_mock_response(
            {"oop_max": 10000, "remaining_oop_max": 9000, "copay": 1000}
        )
    elif "api2" in url:
        return create_mock_response(
            {"oop_max": 20000, "remaining_oop_max": 9000, "copay": 50000}
        )
    elif "api3" in url:
        return create_mock_response(
            {"oop_max": 10000, "remaining_oop_max": 8000, "copay": 1000}
        )
    else:
        return create_mock_response({}, status_code=500)


async def async_side_effect_2(url, *args, **kwargs):
    if "api1" in url:
        return create_mock_response(
            {"oop_max": 10000, "remaining_oop_max": 9000, "copay": 11000}
        )
    elif "api2" in url:
        return create_mock_response(
            {"oop_max": 20000, "remaining_oop_max": 9000, "copay": 50000}
        )
    elif "api3" in url:
        return create_mock_response(
            {"oop_max": 10000, "remaining_oop_max": 8000, "copay": 1000}
        )
    else:
        return create_mock_response({}, status_code=500)
