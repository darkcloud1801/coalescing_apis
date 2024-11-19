import asyncio
from typing import List, Optional

import httpx

from adapters.utils import get_default_config


class InsuranceApiAdapter:
    def __init__(self, member_id: int, urls: List[str]):
        """
        Initialize the insurance api adapter

        :param member_id: member_id for Member
        :param urls: right now this corresponds to the local urls defined.
        """
        self.member_id = member_id
        self.api_endpoints = urls

    async def get_data(self, url: str, client: httpx.AsyncClient) -> dict:
        """
        Makes a request to the url using the client and returns the response.

        :param url:
        :param client:
        :return:
        JSON Payload
        """
        try:
            response = await client.get(url)
            response.raise_for_status()  # Raise an exception for HTTP errors
            return response.json()
        except httpx.RequestError as e:
            print(f"Error fetching data from {url}: {e}")
            return {}
        except httpx.HTTPStatusError as e:
            print(f"HTTP error fetching data from {url}: {e}")
            return {}

    async def get_all_data(self) -> List[dict]:
        """
        Traverses all defined urls and makes requests of them in parallel

        :return:
        List of values

        or raises an Exception
        """
        async with httpx.AsyncClient() as client:
            tasks = [self.get_data(url, client) for url in self.api_endpoints]
            return await asyncio.gather(*tasks, return_exceptions=True)

    def coalesce_data(self, responses, config: Optional[dict] = None) -> dict:
        """
        Coalesce responses using defined rules.

        :param responses:
        :param config:
        """
        if config is None:
            config = {"oop_max": "min", "remaining_oop_max": "max", "copay": "min"}

        coalesced = dict()
        for attr in config:
            policy = config[attr]
            values = [response[attr] for response in responses if attr in response]

            match policy:
                case "min":
                    coalesced[attr] = min(values)
                case "max":
                    coalesced[attr] = max(values)
                case "avg":
                    coalesced[attr] = sum(values) // len(
                        values
                    )  # Integer division for cents
                case _ if callable(policy):
                    coalesced[attr] = policy(values)
                case _:
                    raise ValueError("Method currently unaccounted for.")

        # Convert back to cents if any invalid values were introduced
        return {
            key: int(value) if value not in [float("inf"), float("-inf")] else 0
            for key, value in coalesced.items()
        }

    async def get_coalesced_data(self, config: Optional[dict]) -> dict:
        """
        Helper function for retrieving and coalescing data

        :param config:
        :return:
        """
        responses = await self.get_all_data()
        return self.coalesce_data(responses, config)
