import random
from typing import Optional

from fastapi import FastAPI, Query, HTTPException, Request, Depends

from adapters import InsuranceApiAdapter, get_default_config
from adapters.utils import get_insurance_urls

app = FastAPI()


#
# I made 4 separate api endpoints to simulate the 3 endpoints described in the problem as well as a third that raises
# an error 50% of the time.
#
@app.get("/api1")
async def api1(
    member_id: int = Query(..., description="The ID of the member to get"),
):
    """
    Simulates external Insurance API 1 endpoint

    Args:
        member_id (int): The ID of the member to get.

    Returns:
        dict: A JSON response with insurance info.
    """

    return {"oop_max": 10000, "remaining_oop_max": 9000, "copay": 1000}


@app.get("/api2")
async def api2(
    member_id: int = Query(..., description="The ID of the member to get"),
):
    """
    Simulates external Insurance API 2 endpoint

    Args:
        member_id (int): The ID of the member to get.

    Returns:
        dict: A JSON response with insurance info.
    """

    return {"oop_max": 20000, "remaining_oop_max": 9000, "copay": 50000}


@app.get("/api3")
async def api3(
    member_id: int = Query(..., description="The ID of the member to get"),
):
    """
    Simulates external Insurance API 3 endpoint

    Args:
        member_id (int): The ID of the member to get.

    Returns:
        dict: A JSON response with insurance info.
    """

    return {"oop_max": 10000, "remaining_oop_max": 8000, "copay": 1000}


@app.get("/api4")
async def api4(
    member_id: int = Query(..., description="The ID of the member to get"),
):
    """
    Simulates external Insurance API 4 endpoint

    Args:
        member_id (int): The ID of the member to get.

    Returns:
        dict: A JSON response with insurance info.
    """

    possible_resp = random.randint(1, 100)
    if possible_resp % 2 == 0:
        raise HTTPException(status_code=500, detail=f"API request failed.")

    return {"oop_max": 10000, "remaining_oop_max": 7000, "copay": 1000}


@app.get("/insurance-info")
async def insurance_info(
    member_id: int = Query(..., description="The ID of the member to get"),
    request: Request = None,
    coalesce_config: Optional[dict] = Depends(get_default_config),
):
    """
    Main endpoint where a user may retrieve their coalesced insurance information

    Args:
        member_id (int): The ID of the member to get.
        request (Request): The insurance request object.
        coalesce_config (dict): The coalesced insurance configuration object.

    Returns:
        dict: A JSON response with insurance info.
    """

    api_endpoints = get_insurance_urls(member_id=member_id, request=request)

    coalescer = InsuranceApiAdapter(member_id=member_id, urls=api_endpoints)

    result = await coalescer.get_coalesced_data(config=coalesce_config)

    return {
        key: int(value) if value not in [float("inf"), float("-inf")] else 0
        for key, value in result.items()
    }
