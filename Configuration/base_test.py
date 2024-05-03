import unittest
from Configuration.drivers_setup import *


class BaseTest(unittest.TestCase):
    driver = None
    browser = ''
    test_name = ''
    tests_failed = False
    url = ''

    @classmethod
    def setUpClass(cls):
        cls.driver = driver_init()
        cls.driver.maximize_window()

    @classmethod
    def tearDownClass(cls):
        cls.driver.quit()
