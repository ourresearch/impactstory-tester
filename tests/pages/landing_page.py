import os

from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.common.exceptions import TimeoutException, ElementNotVisibleException, NoSuchElementException

from page import Page

class LandingPage(Page):
    def __init__(self, wd, host):
        url = host + "/" 
        super(LandingPage, self).__init__(wd, url)
        if self.is_logged_in:
            self.logout()

    @property
    def name(self):
        return self.wd.find_element_by_tag_name("h2").text

    @property
    def is_logged_in(self):
        try:
            self.wd.find_element_by_css_selector("a.logout").click()
            return True
        except (TimeoutException, ElementNotVisibleException, NoSuchElementException):
            return False

    # @property
    # def is_logged_in(self):
    #     wait = WebDriverWait(self.wd, 0.5)
    #     try:
    #         element = wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, 'a.logout')))
    #         return True
    #     except (TimeoutException, ElementNotVisibleException):
    #         return False

    def logout(self):
        return self.wd.find_element_by_css_selector("a.logout").click()

    def click_new_profile_button(self):
        return self.wd.find_element_by_link_text("Make my impact profile").click()

    def click_view_sample_profile_button(self):
        return self.wd.find_element_by_link_text("View a sample profile").click()









