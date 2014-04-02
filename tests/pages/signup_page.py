import os
import time

from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.common.exceptions import TimeoutException, ElementNotVisibleException, NoSuchElementException

from page import Page

class SignupPage(Page):
    def __init__(self, wd, host):
        url = "{host}/signup".format(
            host=host)
        super(SignupPage, self).__init__(wd, url)

    def fill_signup_form(self, first_name, last_name, email, password):
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

        self.wait_for_element_clickable(*(By.CLASS_NAME, "btn-primary"))
        self.wd.find_element_by_class_name("btn-primary").click()

        self.wait_for_element_present(*(By.CLASS_NAME, "profile-header"))
        profile_url = self.wd.current_url
        self.url_slug = profile_url.rsplit("/", 1)[1]








