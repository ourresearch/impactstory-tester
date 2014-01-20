import os, requests

from selenium_test_case import SeleniumTestCase, slow, online, wd, host
import tests
from tests.pages import landing_page
from nose.tools import assert_equals, assert_in, raises




class TestLandingPage(SeleniumTestCase):
    
    def setUp(self):
        self.page = landing_page.LandingPage(self.wd, self.host)

    def test_load(self):
        self.page.get()
        #print self.page.h1
        assert_equals(self.page.h1, u'Share the full story of your\nresearch impact.')

    def test_start_new_profile(self):
        self.page.get()
        assert "/signup/name" not in self.wd.current_url
        reaction = self.page.click_new_profile_button()
        assert "/signup/name" in self.wd.current_url

    def test_view_sample_profile(self):
        self.page.get()
        assert "/CarlBoettiger" not in self.wd.current_url
        reaction = self.page.click_view_sample_profile_button()
        assert "/CarlBoettiger" in self.wd.current_url
  
    # def test_uservoice_popup(self):
    #     self.page.get()
    #     reaction = self.page.click_uservoice()
    #     assert_in("How can we make ImpactStory better?", self.page.html)

    @slow
    @online
    def test_all_links(self):
        self.page.get()
        print self.page.links
        # expected = [u'http://twitter.com/#!/ImpactStory_now', u'http://feedback.impactstory.org/', u'http://blog.impactstory.org/', u'http://localhost:5000/faq', u'http://localhost:5000/CarlBoettiger', u'http://github.com/total-impact', u'http://localhost:5000/about', u'http://localhost:5000/signup/name', u'http://sloan.org/', u'http://localhost:5000/settings/profile', u'http://nsf.gov/', u'https://github.com/total-impact', u'http://localhost:5000/faq#tos', u'http://localhost:5000/', u'http://twitter.com/#!/ImpactStory', u'http://localhost:5000/signup', u'http://creativecommons.org/licenses/by/2.0/']
        # assert_equals(self.page.links, expected)

        for url in self.page.links:
            print url
            r = requests.get(url, verify=False)  # don't check SSL certificates
            assert_equals(r.status_code, 200)      
