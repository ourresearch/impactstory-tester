from selenium import webdriver
import testconfig
import os, logging, sys
import httplib
import base64
import json

wd = None
host = None

# platforms for sauce are here:  https://saucelabs.com/platforms

#type_of_test = 'local_phantomjs'
#type_of_test = 'local_firefox'
#type_of_test = 'sauce_windows_chrome'

# call like this 
# nosetests --rednose --with-progressive --verbose --processes=4 --process-timeout=120 -A "not slow and not online" --tc=test_type:local_firefox 
# -s is to turn off output capture

# or 
# mynosy tests -s --verbose --processes=4 --process-timeout=120 -A \"not slow and not online\" --tc=test_type:local_phantomjs


#import sys; sys.path.append("/opt/local/Library/Frameworks/Python.framework/Versions/2.7/lib/python2.7/site-packages/selenium-2.39.0-py2.7.egg")

selenium_logger = logging.getLogger('selenium.webdriver.remote.remote_connection')
selenium_logger.setLevel(logging.WARNING)

sauce_configs = {
    "sauce_windows_chrome": {"capabilities": webdriver.DesiredCapabilities.CHROME, "version":"31", "platform": "Windows 8.1"}, 
    "sauce_windows_ie": {"capabilities": webdriver.DesiredCapabilities.INTERNETEXPLORER, "version":"11", "platform": "Windows 8.1"}} 

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
        desired_capabilities = sauce_configs[type_of_test]["capabilities"]
        desired_capabilities['version'] = sauce_configs[type_of_test]["version"]
        desired_capabilities['platform'] = sauce_configs[type_of_test]["platform"]
        desired_capabilities['name'] = "test"
        if not os.getenv("SAUCE_COMMAND_PATH"):
            print "need SAUCE_COMMAND_PATH environment variable"
            quit()
        wd = webdriver.Remote(
            desired_capabilities=desired_capabilities,
            command_executor=os.getenv("SAUCE_COMMAND_PATH")
        )

    return (wd, host)


# based on https://gist.github.com/santiycr/1644439
def set_test_status(jobid, passed=True):
    body_content = json.dumps({"passed": passed})
    connection =  httplib.HTTPConnection("saucelabs.com")

    username=os.getenv("SAUCE_USERNAME")
    access_key=os.getenv("SAUCE_ACCESS_KEY")

    base64string = base64.encodestring("{username}:{access_key}".format(
        username=username, access_key=access_key))[:-1]

    connection.request('PUT', '/rest/v1/%s/jobs/%s' % (username, jobid),
                       body_content,
                       headers={"Authorization": "Basic %s" % base64string})
    result = connection.getresponse()
    return result.status == 200
 
def setup_package():
    global wd, host
    test_type = testconfig.config['test_type']
    (wd, host) = set_web_driver_and_host(test_type)
    if "sauce" in testconfig.config['test_type']:
        print "setting pass to false"
        set_test_status(wd.session_id, passed=False)  #default to failed
        print "****", sys.exc_info()


def teardown_package():
    print "****", sys.exc_info()
    if "sauce" in testconfig.config['test_type']:
        print("Link to your job: https://saucelabs.com/jobs/%s" % wd.session_id)
        if sys.exc_info() == (None, None, None):
            set_test_status(wd.session_id, passed=True)
    wd.quit()


