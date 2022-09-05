import asyncio
import time

import aiohttp
import pandas as pd
from fastapi import APIRouter
from redis_om import NotFoundError

from API.model import StarWarsInfo

asynchronous = APIRouter(prefix="/asynchronous", tags=["asynchronous"])


async def get_req(url):
    async with aiohttp.ClientSession(trust_env=True) as session:
        async with session.get(f"{url}", ssl=False) as response:
            try:
                return await response.json()
            except:
                print(f"in {url} something went wrong")


async def get_req_sleep(url):
    async with aiohttp.ClientSession() as session:
        async with session.get(f"{url}") as response:
            time.sleep(5)
            print(url)
            return await response.json()


async def fix_list(data):
    df = {"name": [], "planet": []}
    for i in data:
        if "name" in i:
            for j in data:
                if j is not None and "count" in j:
                    for a in j["results"]:
                        if i["homeworld"] == a["url"]:
                            df["name"].append(i["name"])
                            df["planet"].append(a["name"])
    star_wars_df = pd.DataFrame(df)
    return star_wars_df


async def get_async_values(number):
    task_1 = []
    for i in range(number):
        task_1.append(get_req(url=f"https://swapi.dev/api/people/{i}"))

    task_1.append(get_req(url=f"https://swapi.dev/api/planets/"))
    star_wars_people = await asyncio.gather(*task_1)
    star_wars_people = await fix_list(star_wars_people)
    return star_wars_people


@asynchronous.get("/")
async def async_star_wars(people: int):
    s = time.perf_counter()
    try:
        star_wars_people = StarWarsInfo.get(pk=people)
    except NotFoundError:
        star_wars_people = await get_async_values(people)

    return (star_wars_people, f"starwars run in {time.perf_counter() - s} seconds")


@asynchronous.post("/save_async_star_wars")
async def save_async_star_wars(people: int):
    star_wars_people = await get_async_values(people)
    star = StarWarsInfo(pk=people,
                        name=str(star_wars_people.to_dict('dict')["name"]),
                        planet=str(star_wars_people.to_dict('dict')["planet"])
                        )

    return star.save()
