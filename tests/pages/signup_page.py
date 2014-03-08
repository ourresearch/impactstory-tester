import os
import time

from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.common.exceptions import TimeoutException, ElementNotVisibleException, NoSuchElementException

from page import Page

class SignupPage(Page):
    def __init__(self, wd, host):
        url = host + "/signup" 
        super(SignupPage, self).__init__(wd, url)

    # def number_products_imported(self, importer_name):
    #     print self.wd.current_url
    #     self.wait_for_element_present(*(By.ID, importer_name + "-count"))   
    #     number_of_products = self.wd.find_element_by_id(importer_name + "-count").text
    #     return int(number_of_products)

    def fill_signup_form(self, first_name, last_name, email, password):
        print self.wd.current_url
        self.wd.find_element_by_id("signup-given-name").click()
        self.wd.find_element_by_id("signup-given-name").clear()
        self.wd.find_element_by_id("signup-given-name").send_keys(first_name)
        self.wd.find_element_by_id("signup-surname").click()
        self.wd.find_element_by_id("signup-surname").clear()
        self.wd.find_element_by_id("signup-surname").send_keys(last_name)
        self.wd.find_element_by_id("signup-email").click()
        self.wd.find_element_by_id("signup-email").send_keys(email)
        self.wd.find_element_by_id("signup-password").click()
        self.wd.find_element_by_id("signup-password").send_keys(password)

        self.wait_for_element_present(*(By.CLASS_NAME, "btn-primary"))
        self.wd.find_element_by_class_name("btn-primary").click()

        self.wait_for_element_present(*(By.CLASS_NAME, "profile-header"))
        profile_url = self.wd.current_url
        self.url_slug = profile_url.rsplit("/", 1)[1]
        print self.url_slug


    def fill_account_tile(self, importer_name, import_content):
        print self.wd.current_url
        self.wait_for_element_visible(*(By.ID, importer_name + "-account-tile"))
        self.wd.find_element_by_id(importer_name + "-account-tile").click()

        self.wait_for_element_clickable(*(By.ID, importer_name + "-account-username-input"))

        self.wd.find_element_by_id(importer_name + "-account-username-input").click()
        self.wd.find_element_by_id(importer_name + "-account-username-input").send_keys(import_content)

        self.wd.find_element_by_id(importer_name + "-account-username-submit").click()


    def is_account_connected(self, importer_name):
        print self.wd.current_url
        self.wait_for_element_visible(*(By.ID, importer_name + "-account-toggle"))
        found = True
        try:
            timeout = self.timeout
            self.timeout = 2
            self.wait_for_element_visible(*(By.ID, importer_name + "-account-toggle-on"))
        except Exception:
            found = False
        self.timeout = timeout           
        return found


    def start_connected_accounts(self):
        print self.wd.current_url
        self.wait_for_element_visible(*(By.PARTIAL_LINK_TEXT, "Import my"))
        self.wd.find_element_by_partial_link_text("Import my").click()

    def finish_connected_accounts(self):
        print self.wd.current_url
        self.wait_for_element_visible(*(By.PARTIAL_LINK_TEXT, "back to profile"))
        self.wd.find_element_by_partial_link_text("back to profile").click()


    def wait_till_import_done(self):
        self.wait_for_element_visible(*(By.ID, importer_name + "-account-tile"))







