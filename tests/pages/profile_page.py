import os

from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By

from page import Page

class ProfilePage(Page):
    def __init__(self, wd, host, url_slug="CarlBoettiger"):
        url = host + "/" + url_slug
        super(ProfilePage, self).__init__(wd, url)

    @property
    def name(self):
        return self.wd.find_element_by_tag_name("h2").text

    def login(self, username="", password=""):
        if not password:
            password = os.getenv("SUPERUSER_PW")

        self.wd.find_element_by_link_text("Log in").click()
        self.wd.find_element_by_name("login").click()
        self.wd.find_element_by_name("login").clear()
        self.wd.find_element_by_name("login").send_keys(username)
        self.wd.find_element_by_name("pass").click()
        self.wd.find_element_by_name("pass").clear()
        self.wd.find_element_by_name("pass").send_keys(password)
        self.wd.find_element_by_xpath("//div[@class='modal-footer']//button[.='Sign in']").click()

    def controls(self):
        return self.wd.find_elements_by_css_selector("div.admin-controls")









