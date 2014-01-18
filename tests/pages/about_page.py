from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By

from page import Page

class AboutPage(Page):
    def __init__(self, wd, host):
        url = host + "/about"
        super(AboutPage, self).__init__(wd, url)

    @property
    def title(self):
        return self.wd.find_element_by_tag_name("h2").text
