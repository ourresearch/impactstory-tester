from selenium import webdriver
import testconfig
import os, logging

wd = None
host = None

#type_of_test = 'local_phantomjs'
#type_of_test = 'local_firefox'
#type_of_test = 'sauce_windows_chrome'

# call like this 
# nosetests -s --verbose --processes=4 --process-timeout=120 -A "not slow and not online" --tc=test_type:local_phantomjs 
# -s is to turn off output capture

# or 
# mynosy tests -s --verbose --processes=4 --process-timeout=120 -A \"not slow and not online\" --tc=test_type:local_phantomjs


#import sys; sys.path.append("/opt/local/Library/Frameworks/Python.framework/Versions/2.7/lib/python2.7/site-packages/selenium-2.39.0-py2.7.egg")

selenium_logger = logging.getLogger('selenium.webdriver.remote.remote_connection')
selenium_logger.setLevel(logging.WARNING)

def set_web_driver_and_host(type_of_test):
    if type_of_test.startswith("local"):
        host = "http://localhost:5000"
    else:
        host = "http://staging-impactstory.org"        

    if type_of_test == 'local_firefox':
        wd = webdriver.Firefox()
    elif type_of_test == 'local_chrome':
        wd = webdriver.Chrome()
    elif type_of_test == 'local_safari':
        wd = webdriver.Safari()
    elif type_of_test == 'local_phantomjs':     
        wd = webdriver.PhantomJS('phantomjs')
    elif type_of_test == 'sauce_windows_chrome':
        # code for others is here: https://saucelabs.com/platforms
        desired_capabilities = webdriver.DesiredCapabilities.CHROME
        desired_capabilities['version'] = '31'
        desired_capabilities['platform'] = "Windows 8.1"
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
    wd.quit()
    if "sauce" in testconfig.config['test_type']:
        print("Link to your job: https://saucelabs.com/jobs/%s" % wd.session_id)
