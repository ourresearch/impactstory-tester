import redis
import sys
import os

test_type = "sauce_windows_ie"

run_command = 'nosetests --with-html-output --rednose --with-progressive --verbose --processes=4 --process-timeout=120 -A "not slow and not online" --tc=test_type:{test_type} tests/test_signup.py'.format(
    test_type=test_type)
os.system(run_command)

redis_url = os.getenv('REDISTOGO_URL', 'redis://localhost:6379')
myredis = redis.from_url(redis_url)

with os.open("results.html", "r") as results:
    myredis.set(test_type, results.read())




