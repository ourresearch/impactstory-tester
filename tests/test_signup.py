import os, requests, random

from selenium_test_case import SeleniumTestCase, slow, online, wd, host
import tests
from tests.pages import signup_page, profile_page
from nose.tools import assert_equals, assert_in, raises




class TestSignup(SeleniumTestCase):
    
    def setUp(self):
        self.page = signup_page.SignupPage(self.wd, self.host)

    def tearDown(self):
        pass

    def test_signup(self):
        self.page.get()
        test_email = "test" + str(random.randint(1000, 9999)) + "@test-impactstory.org"
        self.page.fill_signup_form("Heather", "Impactstorytester", test_email, "pass123")

        self.page.start_connected_accounts()

        assert_equals(self.page.is_account_connected("github"), False)

        self.page.fill_account_tile("github", "tjv")

        assert_equals(self.page.is_account_connected("github"), True)

        self.page.finish_connected_accounts()

        self.profile_page = profile_page.ProfilePage(self.wd, self.host, self.page.url_slug)

        # ideally won't need these
        self.profile_page.get()
        #self.wd.refresh()

        print self.wd.current_url

        assert_equals(self.profile_page.number_products, 4)
        assert_equals(self.profile_page.name, "Heather Impactstorytester")

        assert_in("hapnotes", self.profile_page.product_titles)
        assert_in("semantic_similarity", self.profile_page.product_titles)

        assert_equals(self.profile_page.awards("hapnotes"), [u'recommended', u'cited'])
        assert_equals(self.profile_page.hover_stats("hapnotes"), [{'stat': u'1', 'metric_name': u'GitHub star'}, {'stat': u'1', 'metric_name': u'GitHub fork'}])
