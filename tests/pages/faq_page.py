from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By

from page import Page

class FaqPage(Page):
    def __init__(self, wd, host):
        url = host + "/faq"
        super(FaqPage, self).__init__(wd, url)

    @property
    def title(self):
        return self.wd.find_element_by_tag_name("h2").text

    def wait_till_loaded(self):
        wait = WebDriverWait(self.wd, 10)
        element = wait.until(EC.presence_of_element_located((By.ID, 'whichmetrics')))





