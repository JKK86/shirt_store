import redis

r = redis.Redis()
id = 1

product = [{
    "color": "black",
    "price": 49.99,
    "style": "fitted",
    "quantity": 5,
    "n_purchased": 0,
    },
    {
    "color": "maroon",
    "price": 55,
    "style": "formal",
    "quantity": 10,
    "n_purchased": 0,
    },
    {
    "color": "white",
    "price": 35.99,
    "style": "fitted",
    "quantity": 3,
    "n_purchased": 0,
    }
]

shirts = dict()

for item in product:
    key = f"shirt:{id}"
    shirts[key] = item
    id += 1

print(shirts)

r.flushdb() # for development environment only

for s_id, shirt in shirts.items():
    for field, value in shirt.items():
        r.hset(s_id, field, value)

r.close()