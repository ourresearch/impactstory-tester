import redis
import sys
import os
import httplib
import base64
import json

# based on https://gist.github.com/santiycr/1644439
def set_test_status(jobid, sauce_data):

    username=os.getenv("SAUCE_USERNAME")
    access_key=os.getenv("SAUCE_ACCESS_KEY")
    base64string = base64.encodestring("{username}:{access_key}".format(
        username=username, access_key=access_key))[:-1]

    connection =  httplib.HTTPConnection("saucelabs.com")
    connection.request('PUT', '/rest/v1/%s/jobs/%s' % (username, jobid),
                       json.dumps(sauce_data),
                       headers={"Authorization": "Basic %s" % base64string})
    result = connection.getresponse()
    return result.status == 200


test_type = "sauce_windows_chrome"

os.system("rm results.html")
run_command = 'nosetests --with-html-output --verbose --processes=4 --process-timeout=120 -A "not slow and not online" --tc=test_type:{test_type} tests/test_signup.py'.format(
    test_type=test_type)
os.system(run_command)

redis_url = os.getenv('REDISTOGO_URL', 'redis://localhost:6379')
myredis = redis.from_url(redis_url)
job_id = myredis.get(test_type+"job")
with open("results.html", "r") as results_file:
    results_contents = results_file.read()
passed = "most recent call last" not in results_contents
print "JOB ID:", job_id, "PASSED:", passed
sauce_data = {
    "passed": passed,
    "custom-data": {"results.html":results_contents}}
set_test_status(job_id, sauce_data)
myredis.set(test_type+"results", results_contents)


