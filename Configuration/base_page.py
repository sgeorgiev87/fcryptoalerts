# -*- coding: utf-8 -*-

# START IMPORTS
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.action_chains import ActionChains
import traceback
import time

# END IMPORTS

"""
A Base Page to be inherited by all page objects
"""


class BasePage:
    def __init__(self, driver, timeout=10):
        self.driver = driver
        self.timeout = timeout
        self.wait = WebDriverWait(self.driver, self.timeout)

    def find_element(self, *selector):
     return self.driver.find_element(*selector)

    def find_elements(self, *selector):
      return self.driver.find_elements(*selector)

    def presence_of_element(self, selector):
        return self.wait.until(EC.presence_of_element_located(selector))

    def presence_of_elements(self, selector):
        return self.wait.until(EC.presence_of_all_elements_located(selector))

    def visibility_of_element(self, selector):
        return self.wait.until(EC.visibility_of_element_located(selector))

    def visibility_of_elements(self, selector):
        return self.wait.until(EC.visibility_of_any_elements_located(selector))

    def clickable_element(self, selector):
        return self.wait.until(EC.element_to_be_clickable(selector))

    def click_on_element(self, element_name, selector):
        try:
            self.clickable_element(selector=selector).click()
            print("--> {} clicked.".format(element_name))
        except:
            print("# {} not clicked! ".format(element_name) + str(selector))
            raise

    def is_element_displayed(self, selector):
        try:
            self.find_element(*selector)
        except:
            return False
        return True