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

    def fill_name_form(self, first_name, last_name):
        self.wd.find_element_by_xpath("//div[@class='main-view']/form/div/div/div[2]/input").click()
        self.wd.find_element_by_xpath("//div[@class='main-view']/form/div/div/div[2]/input").clear()
        self.wd.find_element_by_xpath("//div[@class='main-view']/form/div/div/div[2]/input").send_keys(first_name)
        self.wd.find_element_by_xpath("//div[@class='main-view']/form/div/div/div[3]/input").click()
        self.wd.find_element_by_xpath("//div[@class='main-view']/form/div/div/div[3]/input").clear()
        self.wd.find_element_by_xpath("//div[@class='main-view']/form/div/div/div[3]/input").send_keys(last_name)
        return self.wd.find_element_by_css_selector("button.next-button").click()

    def fill_url_slug_form(self, url_slug):
        self.wd.find_element_by_name("url_slug").click()
        self.wd.find_element_by_name("url_slug").clear()
        self.wd.find_element_by_name("url_slug").send_keys(url_slug)
        return self.wd.find_element_by_css_selector("button.next-button").click()

    def fill_import_github_import(self, github_name):
        self.wait_for_element_present(*(By.XPATH, "//img[contains(@src,'/static/img/logos/github.png')]"))
        self.wd.find_element_by_xpath("//img[contains(@src,'/static/img/logos/github.png')]").click()
        self.wd.find_element_by_xpath("//div[@class='content']/form/div[1]/div/input").click()
        self.wd.find_element_by_xpath("//div[@class='content']/form/div[1]/div/input").clear()
        self.wd.find_element_by_xpath("//div[@class='content']/form/div[1]/div/input").send_keys("tjv")
        self.wd.find_element_by_xpath("//div[@class='buttons']//button[normalize-space(.)='Import']").click()
        return self.wd.find_element_by_css_selector("button.next-button").click()

    def fill_email_password(self, email, password):
        self.wd.find_element_by_name("email").click()
        self.wd.find_element_by_name("email").clear()
        self.wd.find_element_by_name("email").send_keys(email)
        self.wd.find_element_by_name("password").click()
        self.wd.find_element_by_name("password").clear()
        self.wd.find_element_by_name("password").send_keys(password)
        self.wd.find_element_by_name("email").click()
        self.wd.find_element_by_name("email").clear()
        return self.wd.find_element_by_css_selector("button.next-button").click()





