import redis
import sys
import os
import httplib
import base64
import json
import datetime
import subprocess
import time

# based on https://gist.github.com/santiycr/1644439
def set_sauce_data(jobid, sauce_data):

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


def decide_pass_fail(result_contents):
    passed = False
    if "OK" in result_contents:
        passed = True 
    return passed



def run_tests(test_type):
    passed = True
    run_command = 'nosetests --verbose --processes=4 --process-timeout=120 -A "not slow and not online" --tc=test_type:{test_type} tests/test_signup_and_accounts.py'.format(
        test_type=test_type)
    try:
        nose_output = subprocess.check_output(run_command,
             stderr=subprocess.STDOUT,
             shell=True)
    except subprocess.CalledProcessError as e:
        passed = False
        nose_output = e.output
    return (passed, nose_output)



def update_job_status(passed, build, nose_output):
    redis_url = os.getenv('REDISTOGO_URL', 'redis://localhost:6379')
    myredis = redis.from_url(redis_url)
    job_id = myredis.get(test_type+"job")
    sauce_data = {
        "passed": passed,
        "build": build,
        "custom-data": {"nose_output": nose_output}}
    set_sauce_data(job_id, sauce_data)
    myredis.set(test_type+"results", nose_output)
    return job_id


# our biggest uses: https://www.google.com/analytics/web/?hl=en#report/visitors-browser/a23384030w45814434p46013062/%3Fexplorer-segmentExplorer.segmentId%3Danalytics.operatingSystem%26explorer-table.plotKeys%3D%5B%5D%26explorer-table.secSegmentId%3Danalytics.browser/
build = datetime.datetime.now().isoformat()[0:16]
for test_type in ["sauce_windows_chrome", "sauce_windows_firefox", "sauce_mac_chrome", "sauce_mac_safari"]:
    (passed, nose_output) = run_tests(test_type)
    # so that they don't create the same url at the same time
    time.sleep(5)
    print nose_output
    if "sauce" in test_type:
        job_id = update_job_status(passed, build, nose_output)
    print test_type, "PASSED=", passed, job_id

