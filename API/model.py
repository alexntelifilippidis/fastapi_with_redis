from redis_om import HashModel, get_redis_connection

redis = get_redis_connection(
    host="127.0.0.1",
    port="6379",
    password="password",
    decode_responses=True,
)


class StarWarsInfo(HashModel):
    name: str
    planet: str

    class Meta:
        database = redis
