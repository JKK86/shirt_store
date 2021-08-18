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


shirts = scan_keys("shirt:*")
print(shirts)
