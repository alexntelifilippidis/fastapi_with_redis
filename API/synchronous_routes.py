import time

import pandas as pd
import requests
from fastapi import APIRouter

synchronous = APIRouter(prefix="/synchronous", tags=["synchronous"])


def get_req_sunc(number):
    starwars_list = []
    for i in range(number):
        try:
            starwars = requests.get(f"https://swapi.dev/api/people/{i}").json()
            starwars_list.append(starwars)
        except:
            print(f"in https://swapi.dev/api/people/{i} something went wrong")
    starwars_planets = requests.get(f"https://swapi.dev/api/planets/").json()
    starwars_list.append(starwars_planets)
    return starwars_list


def fix_list(data):
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


def get_sync_values(number):
    star_wars_people = get_req_sunc(number)
    star_wars_people = fix_list(star_wars_people)
    return star_wars_people


@synchronous.get("/")
def sync_star_wars(people: int):
    s = time.perf_counter()
    starwars = get_sync_values(people)
    return (starwars, f"starwars run  in {time.perf_counter() - s} seconds")
