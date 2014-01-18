import unittest
import os

import testconfig
from selenium import webdriver

from tests import wd, host


def slow(f):
    f.slow = True
    return f

def online(f):
    f.online = True
    return f



class SeleniumTestCase(unittest.TestCase):

    @classmethod
    def setup_class(self):
        from tests import wd, host

        self.wd = wd
        self.host = host



