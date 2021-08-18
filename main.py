import redis

r = redis.Redis()


def scan_keys(pattern, position: int = 0) -> list:
    shirts = []
    while True:
        position, value = r.scan(cursor=position, match=pattern)
        shirts = shirts + value
        if position == 0:
            break
    return shirts


def buy_items(r: redis.Redis, item_id) -> None:
    pipe = r.pipeline()

    while True:
        nleft: bytes = r.hget(item_id, "quantity")
        if nleft > b"0":
            pipe.hincrby(item_id, "quantity", -1)
            pipe.hincrby(item_id, "n_purchased", 1)
            pipe.execute()
            break
        else:
            print("Sorry", item_id, "out of stock")

        return None


shirts = scan_keys("shirt:*")
print(shirts)
buy_items(r, shirts[0])
