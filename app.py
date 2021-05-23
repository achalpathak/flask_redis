from flask import Flask, request
from flask_caching import Cache
from time import sleep

app = Flask(__name__)
cache = Cache(
    app,
    config={
        "CACHE_TYPE": "redis",
        "CACHE_KEY_PREFIX": "server1_",
        "CACHE_REDIS_HOST": "localhost",
        "CACHE_REDIS_PORT": "6379",
        "CACHE_REDIS_URL": "redis://localhost:6379",
    },
)


def big_function(search):
    print("[X] Executing big function")
    sleep(10)
    response = "big data"
    cache.set(f"{search}_resp", response)
    return response


@app.route("/")
def hello_world():
    search = request.args.get("search")
    if cache.get(search) == "STARTED":
        # will be executed for the subsequent requests
        val = cache.get(f"{search}_resp")
        while val is None:
            # Sleep and retry here after every 500 ms
            sleep(0.5)
            val = cache.get(f"{search}_resp")
        return val

    else:
        # will only be executed for the first time
        cache.set(search, "STARTED")
        return big_function(search)
