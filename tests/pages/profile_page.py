import os, re, time

from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By

from page import Page

class ProfilePage(Page):
    def __init__(self, wd, host, url_slug="CarlBoettiger"):
        url = "{host}/{url_slug}".format(
            host=host, url_slug=url_slug)
        super(ProfilePage, self).__init__(wd, url)

    @property
    def name(self):
        self.wait_for_element_visible(*(By.ID, "profile-owner-name"))
        return self.wd.find_element_by_id("profile-owner-name").text


    @property
    def number_products(self):
        self.wait_for_element_visible(*(By.ID, "number-products"))        
        return int(self.wd.find_element_by_id("number-products").text)

    @property
    def product_titles(self):
        self.wait_for_element_visible(*(By.CLASS_NAME, "title-text"))        
        title_lines = self.wd.find_elements_by_class_name("title-text")
        titles = [line.text for line in title_lines]
        return titles

    def awards(self, title):
        self.wait_for_element_visible(*(By.CLASS_NAME, "real-product"))        
        products = self.wd.find_elements_by_class_name("real-product")
        for product in products:
            self.wait_for_element_visible(*(By.CLASS_NAME, "title-text"))        
            if title == product.find_element_by_class_name("title-text").text:
                awards_list = product.find_elements_by_class_name("engagement-type")
                awards_list = [award.text for award in awards_list if award]
                return awards_list


    def extract_stats_from_hover_text(self, hover_text):
        print hover_text
        hover_text = re.sub("\s+", " ", hover_text)

        if "suggesting" in hover_text:
            response = re.findall("This item has (.*?) (.*), suggesting", hover_text)
        else:
            response = re.findall("This item has (.*?) (.*). That's better", hover_text)
        print response

        if not response:
            return {}
        (stat, metric_name) = response[0]
        response = {"stat":stat, "metric_name":metric_name}
        return ({"stat":stat, "metric_name":metric_name})

    def hover_stats(self, title):
        self.wait_for_element_visible(*(By.CLASS_NAME, "real-product"))        
        products = self.wd.find_elements_by_class_name("real-product")
        for product in products:
            if title == product.find_element_by_class_name("title-text").text:
                award_links = product.find_elements_by_class_name("ti-badge")
                hover_texts = [a.get_attribute("data-content") for a in award_links]
                stats = [self.extract_stats_from_hover_text(text) for text in hover_texts]
                stats = [stat for stat in stats if stat]
                return stats


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

    def wait_till_done_updating(self):
        import time
        # seems to need an extra second for some reason
        time.sleep(2)

        timeout_before = self.timeout
        self.timeout = 120
        self.wait_for_element_not_visible(*(By.ID, "products-still-updating"))        
        self.timeout = timeout_before

        # seems to need an extra second for some reason
        time.sleep(1)







