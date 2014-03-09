import os, requests, random, time

from selenium_test_case import SeleniumTestCase, slow, online, wd, host
import tests
from tests.pages import signup_page, accounts_page, profile_page
from nose.tools import assert_equals, assert_in, assert_greater_equal, assert_items_equal, raises




class TestSignupAndAccunts(SeleniumTestCase):


    def create_user(self, given_name, surname):
        test_email = "test" + str(random.randint(1000, 9999)) + "@test-impactstory.org"
        self.page.fill_signup_form(given_name, surname, test_email, "pass123")


    def connect_accounts(self, account_testing_data):
        self.page.start_connected_accounts()

        for account_name in account_testing_data:
            print "Connecting account", account_name
            assert_equals(self.page.is_account_connected(account_name), False)
            self.page.fill_account_tile(account_name, account_testing_data[account_name]["username"])
            assert_equals(self.page.is_account_connected(account_name), True)

        self.page.finish_connected_accounts()



    def check_products(self, account_testing_data):
        total_products = sum([account_testing_data[account]["number_products"] for account in account_testing_data])
        # assert_equals(self.profile_page.number_products, total_products)

        for account_name in account_testing_data:
            print "Checking account", account_name

            for product in account_testing_data[account_name]["products"]:
                if "title" in product:
                    title = product["title"]
                    print title
                    assert_in(title, self.profile_page.product_titles)
                    if "awards" in product:
                        self.awards_equal(self.profile_page.awards(title), product["awards"])
                    if "hover_stats" in product:
                        self.hover_stats_equal(self.profile_page.hover_stats(title), product["hover_stats"])


    def check_profile_page(self, full_name):
        assert_equals(self.profile_page.name, full_name)

    def awards_equal(self, list_a, list_b):
        print list_a, list_b
        list_a = [stat.replace("highly ", "") for stat in list_a]
        list_b = [stat.replace("highly ", "") for stat in list_b]
        assert_items_equal(list_a, list_b)

    def hover_stats_equal(self, list_a, list_b):
        print list_a, list_b
        for (stat_a, stat_b) in zip(list_a, list_b):
            assert_equals(stat_a["metric_name"], stat_b["metric_name"])
            assert_greater_equal(int(stat_a["stat"]), int(stat_b["stat"]))


    def test_signup_and_accounts(self):
        self.page = signup_page.SignupPage(self.wd, self.host)

        given_name = "Clark"
        surname = "Kent"

        account_testing_data = {
            "github": {
                "username": "tjv",
                "number_products": 4,
                "products": [{
                    "title": "hapnotes",
                    "awards": [u'recommended', u'cited'],
                    "hover_stats": [{'stat': u'1', 'metric_name': u'GitHub star'}, {'stat': u'1', 'metric_name': u'GitHub fork'}]
                }]
            },
            "orcid": {
                "username": "0000-0001-6187-6610",
                "number_products": 4,
                "products": [{
                    "title": "How and why scholars cite on Twitter",
                    "awards": [u'cited', u'saved', u'saved', u'discussed'],
                    "hover_stats": [{'stat': u'16', 'metric_name': u'Scopus citations'}, {'stat': u'129', 'metric_name': u'Mendeley readers'}, {'stat': u'1', 'metric_name': u'Delicious bookmark'}, {'stat': u'18', 'metric_name': u'Altmetric.com tweets'}]
                }]
            },
            "figshare": {
                "username": "http://figshare.com/authors/Jason_Priem/100944",
                "number_products": 2,
                "products": [{
                    "title": "Toward a comprehensive impact report for every software project",
                    "awards": [u'discussed', u'viewed', u'saved', u'discussed'],
                    "hover_stats": [{'stat': u'16', 'metric_name': u'figshare shares'}, {'stat': u'344', 'metric_name': u'figshare views'}, {'stat': u'4', 'metric_name': u'Delicious bookmarks'}, {'stat': u'30', 'metric_name': u'Altmetric.com tweets'}]
                }]
            },     
            "slideshare": {
                "username": "jaybhatt",
                "number_products": 9,
                "products": [{
                    "title": "ENDNOTE presentation",
                    "awards": [u'recommended', u'saved', u'discussed', u'viewed'],
                    "hover_stats": [{'stat': u'3', 'metric_name': u'SlideShare favorites'}, {'stat': u'1', 'metric_name': u'Delicious bookmark'}, {'stat': u'1', 'metric_name': u'SlideShare comment'}, {'stat': u'7603', 'metric_name': u'SlideShare views'}]
                }]
            }
            # ,                                     
            # "google_scholar": {
            #     "username": "http://scholar.google.ca/citations?user=AwwuwS0AAAAJ",
            #     "number_products": 0
            # }
        }        

        self.page.get()
        self.wd.maximize_window()
        self.create_user(given_name, surname)

        self.page = accounts_page.AccountsPage(self.wd, self.host, self.page.url_slug)

        self.connect_accounts(account_testing_data)

        # self.page.url_slug = "ClarkKent" #comment
        self.profile_page = profile_page.ProfilePage(self.wd, self.host, self.page.url_slug)
        
        # comment this out after get refresh code
        self.profile_page.get() #comment

        print self.wd.current_url
        print "waiting till done updating"
        self.profile_page.wait_till_done_updating()

        self.check_profile_page(given_name+" "+surname)
        print "DONE updating"
        self.check_products(account_testing_data)




