from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By


class Page(object):
    def __init__(self, wd, url):
        self.wd = wd
        self.url = url

    def get(self):
        return self.wd.get(self.url)

    @property
    def html(self):
        return self.wd.find_element_by_tag_name("html").text

    @property
    def links(self):
        elements = self.wd.find_elements_by_xpath("//a")
        links = [link.get_attribute("href") for link in elements]
        valid_links = list(set([link for link in links if link and link.startswith("http")]))
        return valid_links




