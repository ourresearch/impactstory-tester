from selenium import webdriver
import testconfig
import os, logging, sys
import redis

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



 
def setup_package():
    global wd, host
    test_type = testconfig.config['test_type']
    (wd, host) = set_web_driver_and_host(test_type)


def teardown_package():
    print "****", sys.exc_info()
    if "sauce" in testconfig.config['test_type']:
        print("Link to your job: https://saucelabs.com/jobs/%s" % wd.session_id)
        redis_url = os.getenv('REDISTOGO_URL', 'redis://localhost:6379')
        myredis = redis.from_url(redis_url)
        myredis.set(testconfig.config['test_type']+"job", wd.session_id)
    wd.quit()


