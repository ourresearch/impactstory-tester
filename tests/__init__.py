from selenium import webdriver
import testconfig
import os, logging, sys
import redis
import requests
import httplib
import base64
import json
import datetime

wd = None
host = None

# platforms for sauce are here:  https://saucelabs.com/platforms

#type_of_test = 'local_phantomjs'
#type_of_test = 'local_firefox'
#type_of_test = 'sauce_windows_chrome'

# call like this 
# nosetests --rednose --with-progressive --verbose --processes=4 --process-timeout=120 -A "not slow and not online" --tc=test_type:local_firefox 
# nosetests --with-html-output --rednose --with-progressive --verbose --processes=4 --process-timeout=120 -A "not slow and not online" --tc=test_type:sauce_windows_chrome tests/test_signup.py
# -s is to turn off output capture

# or 
# mynosy tests -s --verbose --processes=4 --process-timeout=120 -A \"not slow and not online\" --tc=test_type:local_phantomjs

#import sys; sys.path.append("/opt/local/Library/Frameworks/Python.framework/Versions/2.7/lib/python2.7/site-packages/selenium-2.39.0-py2.7.egg")

selenium_logger = logging.getLogger('selenium.webdriver.remote.remote_connection')
selenium_logger.setLevel(logging.WARNING)

sauce_operating_systems = {
    "windows": "Windows 8.1", 
    "mac": "OS X 10.8"
    } 

sauce_browsers = {
    "chrome": {"capabilities": webdriver.DesiredCapabilities.CHROME, "version": "31"},
    "firefox": {"capabilities": webdriver.DesiredCapabilities.FIREFOX, "version": "27"},
    "safari": {"capabilities": webdriver.DesiredCapabilities.SAFARI, "version": "6"},
    "ie": {"capabilities": webdriver.DesiredCapabilities.INTERNETEXPLORER, "version": "11"}
    }


def set_web_driver_and_host(type_of_test):
    print "setting type_of_test=", type_of_test

    if type_of_test.startswith("local"):
        host = "http://localhost:5000"
    else:
        host = "http://staging-impactstory.org"        

    if type_of_test == 'local_firefox':
        profile = webdriver.FirefoxProfile()
        profile.set_preference('webdriver.load.strategy', 'unstable')
        wd = webdriver.Firefox(profile)
    elif type_of_test == 'local_chrome':
        wd = webdriver.Chrome()
    elif type_of_test == 'local_safari':
        wd = webdriver.Safari()
    elif type_of_test == 'local_phantomjs':   
        service_args = [
            '--load-images=true', 
            '--ignore-ssl-errors=true'
            ]
        wd = webdriver.PhantomJS('phantomjs', service_args=service_args)
    elif type_of_test.startswith("sauce"):
        # code for others is here: https://saucelabs.com/platforms
        (sauce, operating_system, browser) = type_of_test.split("_")
        desired_capabilities = sauce_browsers[browser]["capabilities"]
        desired_capabilities["version"] = sauce_browsers[browser]["version"]
        desired_capabilities["platform"] = sauce_operating_systems[operating_system]
        desired_capabilities['name'] = "{type_of_test}".format(
            type_of_test=type_of_test, host=host)
        if not os.getenv("SAUCE_COMMAND_PATH"):
            print "need SAUCE_COMMAND_PATH environment variable"
            quit()
        wd = webdriver.Remote(
            desired_capabilities=desired_capabilities,
            command_executor=os.getenv("SAUCE_COMMAND_PATH")
        )

    return (wd, host)


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


def delete_all_test_accounts(host):
    url = host + u"/tests?key=" + os.getenv("API_ADMIN_KEY")
    print u"deleting all test accounts:", url
    r = requests.delete(url)
    print r.json()
    return r.json()


def delete_test_account(url_slug):
    global host
    url = host + u"/user/{url_slug}".format(
        url_slug=url_slug)
    print u"deleting test account:", url
    r = requests.delete(url)
    return r


def setup_package():
    global wd, host
    test_type = testconfig.config['test_type']
    (wd, host) = set_web_driver_and_host(test_type)
    delete_all_test_accounts(host)


def teardown_package():
    if "sauce" in testconfig.config['test_type']:
        print("Link to your job: https://saucelabs.com/jobs/%s" % wd.session_id)
        redis_url = os.getenv('REDISTOGO_URL', 'redis://localhost:6379')
        myredis = redis.from_url(redis_url)
        myredis.set(testconfig.config['test_type']+"job", wd.session_id)

        sauce_data = {"build": datetime.datetime.utcnow().isoformat()}
        set_test_status(wd.session_id, sauce_data)

    wd.quit()


