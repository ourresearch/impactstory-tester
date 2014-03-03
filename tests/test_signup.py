import os, requests, random

from selenium_test_case import SeleniumTestCase, slow, online, wd, host
import tests
from tests.pages import signup_page, profile_page
from nose.tools import assert_equals, assert_in, raises




class TestSignup(SeleniumTestCase):
    
    def setUp(self):
        self.page = signup_page.SignupPage(self.wd, self.host)

    def test_signup(self):
        self.page.get()
        test_email = "test" + str(random.randint(1000, 9999)) + "@e.com"
        self.page.fill_signup_form("Heather", "Piwowar", test_email, "pass123")

        self.page.start_importers()

        self.page.fill_import_tile("github", "tjv")
        self.page.wait_till_import_done()

        profile_url = self.wd.current_url
        url_slug = profile_url.rsplit("/", 1)[1]
        print url_slug

        self.profile_page = profile_page.ProfilePage(self.wd, self.host, url_slug)
        #self.profile_page.get()

        assert_equals(self.profile_page.number_products, 4)
        assert_equals(self.profile_page.name, "Heather Piwowar")

        assert_in("hapnotes", self.profile_page.product_titles)
        assert_in("semantic_similarity", self.profile_page.product_titles)

        assert_equals(self.profile_page.awards("hapnotes"), [u'recommended', u'cited'])
        assert_equals(self.profile_page.hover_stats("hapnotes"), [{'stat': u'1', 'metric_name': u'GitHub star'}, {'stat': u'1', 'metric_name': u'GitHub fork'}])
