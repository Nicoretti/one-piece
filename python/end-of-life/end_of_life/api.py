import requests
from pydantic import BaseModel, Field
from datetime import date


class Cycle(BaseModel):
    cycle: int | str
    eol: date
    latest: str
    latestReleaseDate: date
    releaseDate: date
    lts: bool
    link: str | None = Field(default=None)
    support: str | bool | None = Field(default=None)
    discontinued: bool | None = Field(default=None)


def product_cycle_details(product: str, cycle: str):
    response = requests.get(f"https://endoflife.date/api/{product}/{cycle}.json")
    if not response.ok:
        raise Exception("Could not fetch product details")
    return Cycle(**response.json(), cycle=cycle)


def product_details(product: str):
    response = requests.get(f"https://endoflife.date/api/{product}.json")
    if not response.ok:
        raise Exception("Could not fetch product details")
    return [Cycle(**p) for p in response.json()]


def product_versions(product: str):
    response = requests.get(f"https://endoflife.date/api/{product}.json")
    if not response.ok:
        raise Exception("Could not fetch product details")
    versions = set(entry['cycle'] for entry in response.json())
    return versions


def all_products():
    response = requests.get("https://endoflife.date/api/all.json")
    if not response.ok:
        raise Exception("Could not fetch list of supported products")
    return [p for p in response.json()]
