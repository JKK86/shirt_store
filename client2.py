import redis
import logging

r = redis.Redis()
logging.basicConfig()


class OutOfStockError(Exception):
    """Raised when shirts out of stock"""


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
        try:
            pipe.watch(item_id)
            nleft: bytes = r.hget(item_id, "quantity")
            if nleft > b"0":
                pipe.multi()
                pipe.hincrby(item_id, "quantity", -1)
                pipe.hincrby(item_id, "n_purchased", 1)
                pipe.execute()
                break
            else:
                pipe.unwatch()
                raise OutOfStockError(f"Sorry {item_id} is out of stock")
        except redis.WatchError:
            logging.warning("Watch error! Retrying")
    return None


shirts = scan_keys("shirt:*")
# print(shirts)
buy_items(r, shirts[0])
