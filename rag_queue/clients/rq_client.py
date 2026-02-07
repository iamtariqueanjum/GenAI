from redis import Redis
from rq import Queue

q = Queue(connection=Redis(
    host="localhost",
    port=6379
))
