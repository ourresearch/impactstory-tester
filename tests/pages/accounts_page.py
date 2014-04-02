import os
import time

from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.common.exceptions import TimeoutException, ElementNotVisibleException, NoSuchElementException

from page import Page

class AccountsPage(Page):
    def __init__(self, wd, host, url_slug):
        self.url_slug = url_slug
        url = "{host}/{url_slug}/accounts".format(
            host=host, url_slug=url_slug)
        super(AccountsPage, self).__init__(wd, url)


    def fill_account_tile(self, importer_name, import_content):
        # scroll to bottom of the page to get all the importers on
        self.wd.execute_script("window.scrollTo(0, document.body.scrollHeight);")

        self.wait_for_element_clickable(*(By.ID, importer_name + "-account-tile"))
        self.wd.find_element_by_id(importer_name + "-account-tile").click()

        self.wait_for_element_clickable(*(By.ID, importer_name + "-account-username-input"))
        self.wd.find_element_by_id(importer_name + "-account-username-input").click()
        
        self.wd.find_element_by_id(importer_name + "-account-username-input").send_keys(import_content)

        self.wait_for_element_clickable(*(By.ID, importer_name + "-account-username-submit"))
        self.wd.find_element_by_id(importer_name + "-account-username-submit").click()


    def is_account_connected(self, importer_name):
        self.wait_for_element_visible(*(By.ID, importer_name + "-account-toggle"))
        found = True

        # maybe needs extra sleep
        import time
        time.sleep(1)
        
        try:
            timeout = self.timeout
            self.timeout = 2
            self.wait_for_element_visible(*(By.ID, importer_name + "-account-toggle-on"))
        except Exception:
            found = False
        self.timeout = timeout   

        return found


    def start_connected_accounts(self):
        self.wait_for_element_clickable(*(By.PARTIAL_LINK_TEXT, "Import my"))
        self.wd.find_element_by_partial_link_text("Import my").click()

    def finish_connected_accounts(self):
        self.wait_for_element_clickable(*(By.PARTIAL_LINK_TEXT, "back to profile"))
        self.wd.find_element_by_partial_link_text("back to profile").click()

    def wait_till_import_done(self):
        self.wait_for_element_visible(*(By.ID, importer_name + "-account-tile"))







