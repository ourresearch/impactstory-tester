import os

from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.common.exceptions import TimeoutException, ElementNotVisibleException, NoSuchElementException

from page import Page

class SignupPage(Page):
    def __init__(self, wd, host):
        url = host + "/signup/name" 
        super(SignupPage, self).__init__(wd, url)

    def number_products_imported(self, importer_name):
        print self.wd.current_url
        self.wait_for_element_present(*(By.ID, importer_name + "-count"))   
        number_of_products = self.wd.find_element_by_id(importer_name + "-count").text
        return int(number_of_products)

    def fill_name_form(self, first_name, last_name):
        print self.wd.current_url
        self.wd.find_element_by_xpath("//div[@class='main-view']/form/div/div/div[2]/input").click()
        self.wd.find_element_by_xpath("//div[@class='main-view']/form/div/div/div[2]/input").clear()
        self.wd.find_element_by_xpath("//div[@class='main-view']/form/div/div/div[2]/input").send_keys(first_name)
        self.wd.find_element_by_xpath("//div[@class='main-view']/form/div/div/div[3]/input").click()
        self.wd.find_element_by_xpath("//div[@class='main-view']/form/div/div/div[3]/input").clear()
        self.wd.find_element_by_xpath("//div[@class='main-view']/form/div/div/div[3]/input").send_keys(last_name)
        self.wd.find_element_by_css_selector("button.next-button").click()

    def fill_url_slug_form(self, url_slug):
        print self.wd.current_url
        self.wd.find_element_by_name("url_slug").click()
        self.wd.find_element_by_name("url_slug").clear()
        self.wd.find_element_by_name("url_slug").send_keys(url_slug)
        self.wait_for_element_present(*(By.XPATH, "//button[@class='next-button enabled']"))
        self.wd.find_element_by_css_selector("button.next-button").click()


    def fill_import_tile(self, importer_name, import_content):
        print self.wd.current_url
        self.wait_for_element_present(*(By.ID, importer_name + "-tile"))
        self.wd.find_element_by_id(importer_name + "-tile").click()

        try:
            self.wd.find_element_by_xpath("//div[@class='importer-input']/textarea").click()
            self.wd.find_element_by_xpath("//div[@class='importer-input']/textarea").send_keys(import_content)
        except ElementNotVisibleException:
            self.wd.find_element_by_xpath("//div[@class='content']/form/div[1]/div/input").click()
            self.wd.find_element_by_xpath("//div[@class='content']/form/div[1]/div/input").send_keys(import_content)

        self.wd.find_element_by_xpath("//button[@type='submit']").click()
        self.wait_for_element_present(*(By.CSS_SELECTOR, "#"+importer_name+"-tile.has-run"))


    def finish_importers(self):
        print self.wd.current_url
        self.wait_for_element_present(*(By.XPATH, "//button[@class='next-button enabled']"))
        self.wd.find_element_by_css_selector("button.next-button").click()


    def fill_email_password(self, email, password):
        print self.wd.current_url
        self.wd.find_element_by_name("email").click()
        self.wd.find_element_by_name("email").send_keys(email)
        self.wd.find_element_by_name("password").click()
        self.wd.find_element_by_name("password").send_keys(password)
        self.wd.find_element_by_name("email").click()

        self.wait_for_element_present(*(By.XPATH, "//button[@class='next-button enabled']"))
        self.wd.find_element_by_css_selector("button.next-button").click()

        self.wait_for_element_present(*(By.CLASS_NAME, "profile-header"))





