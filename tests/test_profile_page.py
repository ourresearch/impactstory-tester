import os, requests

from selenium_test_case import SeleniumTestCase, slow, online, wd, host
import tests
from tests.pages import profile_page
from nose.tools import assert_equals, raises




class TestProfile(SeleniumTestCase):
    
    def setUp(self):
        self.page = profile_page.ProfilePage(self.wd, self.host)

    def test_title(self):
        self.page.get()
        print self.page.name
        assert_equals(self.page.name, "Carl Boettiger")

    def test_login_controls(self):
        self.page.get()
        self.page.login("team@impactstory.org")

        print [a.text for a in self.page.controls()]
        assert_equals(1, "Carl Boettiger")
  
      
