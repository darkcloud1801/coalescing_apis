from typing import Optional, List
import statistics as stats
from fastapi import Request


def get_default_config() -> Optional[dict]:
    """
    Helper function used for determining default policy used in data coalescing, and
    for writing unit tests.

    :return:
    Data Coalescence Config or None
    """
    return {"oop_max": "min", "remaining_oop_max": "max", "copay": "min"}


def get_insurance_urls(member_id: int, request: Request) -> List[str]:
    """
    Helper function for getting insurance urls for a member_id.

    :param member_id: member id of the member
    :param request: Request object

    :return:
    List of insurance urls
    """
    api_endpoint_names = ["api1", "api2", "api3", "api4"]

    return [
        f"{request.url_for(api_name)}?member_id={member_id}"
        for api_name in api_endpoint_names
    ]


def get_mode_or_avg(nums: List[int]) -> Optional[int]:
    """
    Return the average of the list of numbers if a mode does not exist.
    A Mode of a list is the value that appears the most.

    :param nums:
    :return:
    """
    try:
        return stats.mode(nums)
    except ValueError:
        return stats.median(nums)
