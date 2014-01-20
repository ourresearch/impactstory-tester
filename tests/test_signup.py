import os, requests, random

from selenium_test_case import SeleniumTestCase, slow, online, wd, host
import tests
from tests.pages import signup_page, landing_page
from nose.tools import assert_equals, raises




class TestSignup(SeleniumTestCase):
    
    def setUp(self):
        self.page = signup_page.SignupPage(self.wd, self.host)

    def test_signup(self):
        self.page.get()
        self.page.fill_name_form("Heather", "Piwowar")
        self.page.fill_url_slug_form("pretend" + str(random.randint(1000, 9999)))
        self.page.fill_import_github_import("tjv")
        self.page.fill_email_password("test" + str(random.randint(1000, 9999)), "pass123")

  
    