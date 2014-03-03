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
        self.page.fill_name_form("Heather", "Piwowar")
        url_slug = "pretend" + str(random.randint(1000, 9999))
        self.page.fill_url_slug_form(url_slug)

        self.page.fill_import_tile("github", "tjv")
        number_of_products = self.page.number_products_imported("github")
        # assert_equals(number_of_products, 4)

        self.page.fill_import_tile("products-by-url", "http://starbucks.com")
        number_of_products = self.page.number_products_imported("products-by-url")
        assert_equals(number_of_products, 1)
        
        self.page.finish_importers()
        self.page.fill_email_password("test" + str(random.randint(1000, 9999)), "pass123")

        profile_url = self.wd.current_url

        #url_slug = "pretend6195"


        self.profile_page = profile_page.ProfilePage(self.wd, self.host, url_slug)


        #self.profile_page.get()


        assert_equals(self.profile_page.name, "Heather Piwowar")
        # assert_equals(self.profile_page.number_products, 5)

        assert_in("hapnotes", self.profile_page.product_titles)
        assert_in("Starbucks Coffee Company", self.profile_page.product_titles)
        assert_in("semantic_similarity", self.profile_page.product_titles)

        assert_equals(self.profile_page.awards("hapnotes"), [u'recommended', u'cited'])
        assert_equals(self.profile_page.awards("Starbucks Coffee Company"), [u'saved'])

        assert_equals(self.profile_page.hover_stats("Starbucks Coffee Company"), [{'stat': u'79', 'metric_name': u'Delicious bookmarks'}])
        assert_equals(self.profile_page.hover_stats("hapnotes"), [{'stat': u'1', 'metric_name': u'GitHub star'}, {'stat': u'1', 'metric_name': u'GitHub fork'}])


