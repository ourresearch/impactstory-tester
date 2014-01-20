import time

from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.common.exceptions import TimeoutException, ElementNotVisibleException, NoSuchElementException


class Page(object):
    def __init__(self, wd, url, implicit_wait_time=10):
        self.wd = wd
        self.url = url
        self.implicit_wait_time = implicit_wait_time
        self.wd.implicitly_wait(self.implicit_wait_time)
        self.timeout = 20

    def get(self):
        return self.wd.get(self.url)

    @property
    def html(self):
        return self.wd.find_element_by_tag_name("html").text

    @property
    def h1(self):
        return self.wd.find_element_by_tag_name("h1").text

    @property
    def links(self):
        elements = self.wd.find_elements_by_xpath("//a")
        links = [link.get_attribute("href") for link in elements]
        valid_links = list(set([link for link in links if link and link.startswith("http")]))
        return valid_links

    def click_uservoice(self):
        element = self.wd.find_element_by_css_selector("a#uvTabLabel")
        element.click()
        element = self.wait_for_element_present(*(By.TAG_NAME, "iframe"))
        element = self.wd.switch_to_frame(self.wd.find_elements_by_tag_name("iframe")[0])
        # element = self.wd.switch_to_frame("uvw-iframe-undefined")
        return element



    # several methods reused from https://github.com/mozilla/remo-tests/blob/master/pages/page.py
    def is_element_present(self, *locator):
        """
        Return true if the element at the specified locator is present in the DOM.
        Note: It returns false immediately if the element is not found.
        """
        self.wd.implicitly_wait(0)
        try:
            self.wd.find_element(*locator)
            return True
        except NoSuchElementException:
            return False
        finally:
            # set the implicit wait back
            self.wd.implicitly_wait(self.implicit_wait_time)

    def is_element_visible(self, *locator):
        """
        Return true if the element at the specified locator is visible in the browser.
        Note: It uses an implicit wait if it cannot find the element immediately.
        """
        try:
            return self.wd.find_element(*locator).is_displayed()
        except (NoSuchElementException, ElementNotVisibleException):
            return False

    def is_element_not_visible(self, *locator):
        """
        Return true if the element at the specified locator is not visible in the browser.
        Note: It returns true immediately if the element is not found.
        """
        self.wd.implicitly_wait(0)
        try:
            return not self.wd.find_element(*locator).is_displayed()
        except (NoSuchElementException, ElementNotVisibleException):
            return True
        finally:
            # set the implicit wait back
            self.wd.implicitly_wait(self.implicit_wait_time)

    def wait_for_element_present(self, *locator):
        """Wait for the element at the specified locator to be present in the DOM."""
        count = 0
        while not self.is_element_present(*locator):
            time.sleep(1)
            count += 1
            if count == self.timeout:
                raise Exception(*locator + ' has not loaded')

    def wait_for_element_visible(self, *locator):
        """Wait for the element at the specified locator to be visible in the browser."""
        count = 0
        while not self.is_element_visible(*locator):
            time.sleep(1)
            count += 1
            if count == self.timeout:
                raise Exception(*locator + " is not visible")

    def wait_for_element_not_present(self, *locator):
        """Wait for the element at the specified locator to be not present in the DOM."""
        self.wd.implicitly_wait(0)
        try:
            WebDriverWait(self.wd, self.timeout).until(lambda s: len(self.find_elements(*locator)) < 1)
            return True
        except TimeoutException:
            Assert.fail(TimeoutException)
        finally:
            self.wd.implicitly_wait(self.implicit_wait_time)

