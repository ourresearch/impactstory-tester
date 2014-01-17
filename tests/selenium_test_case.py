from selenium import webdriver
import unittest
import os
import testconfig


#type_of_test = 'local_phantomjs'
#type_of_test = 'local_firefox'
#type_of_test = 'sauce_windows_chrome'

# call like this 
# nosetests -s --verbose --processes=4 --process-timeout=120 -A "not slow and not online" --tc=test_type:local_phantomjs 
# -s is to turn off output capture

def slow(f):
    f.slow = True
    return f

def online(f):
    f.online = True
    return f





class SeleniumTestCase(unittest.TestCase):

    def setUp(self):
        test_type = testconfig.config['test_type']
        self.set_web_driver_and_host(test_type)
        self.wd.implicitly_wait(60)
        
    def tearDown(self):
        self.wd.quit()
        if "sauce" in testconfig.config['test_type']:
            print("Link to your job: https://saucelabs.com/jobs/%s" % self.wd.session_id)


    def set_web_driver_and_host(self, type_of_test):
        if type_of_test == 'local_firefox':
            self.wd = webdriver.Firefox()
            self.host = "http://localhost:5000"

        elif type_of_test == 'local_phantomjs':     
            self.wd = webdriver.PhantomJS('phantomjs')
            self.host = "http://localhost:5000"

        elif type_of_test == 'sauce_windows_chrome':
            # code for others is here: https://saucelabs.com/platforms
            desired_capabilities = webdriver.DesiredCapabilities.CHROME
            desired_capabilities['version'] = '31'
            desired_capabilities['platform'] = "Windows 8.1"
            desired_capabilities['name'] = self.id()
            if not os.getenv("SAUCE_COMMAND_PATH"):
                print "need SAUCE_COMMAND_PATH environment variable"
                quit()
            self.wd = webdriver.Remote(
                desired_capabilities=desired_capabilities,
                command_executor=os.getenv("SAUCE_COMMAND_PATH")
            )
            self.host = "http://staging-impactstory.org"
