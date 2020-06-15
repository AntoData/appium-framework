from appium import webdriver
from appium.webdriver.common.mobileby import MobileBy
from selenium.common.exceptions import WebDriverException
from selenium.webdriver.support import expected_conditions
from selenium.webdriver.support.wait import WebDriverWait
from appium.webdriver import webelement
import time

from utils.screenshot_utils import ScreenshotUtils

"""
To get to know how to use this project: https://github.com/AntoData/appium-framework/wiki
"""


class WebDriverFindUtils:
    """
    This class provides methods that will be used in the property locators in the classes for our page objects
    for finding webelements using implicit waits (we wait until the elements is displayed or the time runs out)
    Also, we provided a feature to take screenshots that will be saved in the session folder

    """
    def __init__(self, driver: webdriver):
        """
        This class has two properties:
        - A webdriver object that will perform the implicit wait and the methods to find elements
        - Timeout, the amount of seconds we keep waiting for the element to appear
        :param driver: Webdriver object we will assign to our driver property
        """
        self.__driver: webdriver = driver
        self.__timeout: int = 10
        # We have a object ScreenshotUtils that will perform the operation of taking a screenshot everytime we
        # find an element using the custom made class for this in this property
        self.__screenshot_utils = ScreenshotUtils(self.__driver)

    @property
    def driver(self) -> webdriver:
        """
        This method returns the property .__driver which is not reachable outside this class
        There won't be a set method for this
        :return: property driver (object webdriver)
        """
        return self.__driver

    @property
    def timeout(self) -> int:
        """
        This method returns the value of the property .__timeout (which sets the timeout to wait for an element
        to be present) which is not reachable outside this class
        :return: The value of the property timeout
        """
        return self.__timeout

    @timeout.setter
    def timeout(self, timeout: int) -> None:
        """
        This method allows the user to set a new timeout for this class to wait to find an element.
        :param timeout: New timeout
        :return: None
        """
        self.__timeout: int = timeout

    def find_element_by_xpath(self, xpath: str) -> webelement:
        """
        This method waits until a web element is display searching it using the parameter xpath. If it is found before
        the timeout, we return the element found
        :param xpath: Xpath selector to find our web element
        :return: The web element found (None in case the element is not present)
        """
        # As there are unsolved issues in appium with the WebDriverWait, we use a try/except block
        try:
            # We use the WebDriverWait setting the timeout to our property timeout and we wait until the element is
            # present by xpath (or until the timeout)
            WebDriverWait(self.driver, self.timeout).\
                until(expected_conditions.presence_of_element_located((MobileBy.XPATH, xpath)))
        except WebDriverException:
            # We catch any possible exception derived of these current issues appium has with WebDriverWait and in that
            # case we wait the same amount of time than the timeout
            time.sleep(self.timeout)
        # We take a screenshot that will be saved in the folder created in folder screenshots for this test
        self.__screenshot_utils.take_screenshot()
        # We search for the element by xpath and return it
        return self.driver.find_element_by_xpath(xpath)
    """
    All the other methods follow the same pattern using different selectors
    """

    def find_elements_by_xpath(self, xpath: str) -> webelement:
        try:
            WebDriverWait(self.driver, self.timeout).\
                until(expected_conditions.presence_of_element_located((MobileBy.XPATH, xpath)))
        except WebDriverException:
            time.sleep(self.timeout)
        self.__screenshot_utils.take_screenshot()
        return self.driver.find_elements_by_xpath(xpath)

    def find_element_by_id(self, v_id: str) -> webelement:
        try:
            WebDriverWait(self.driver, self.timeout).\
                until(expected_conditions.presence_of_element_located((MobileBy.ID, v_id)))
        except WebDriverException:
            time.sleep(self.timeout)
        self.__screenshot_utils.take_screenshot()
        return self.driver.find_element_by_id(v_id)

    def find_element_by_class_name(self, class_name: str) -> webelement:
        try:
            WebDriverWait(self.driver, self.timeout).\
                until(expected_conditions.presence_of_element_located((MobileBy.CLASS_NAME, class_name)))
        except WebDriverException:
            time.sleep(self.timeout)
        self.__screenshot_utils.take_screenshot()
        return self.driver.find_element_by_class_name(class_name)

    def find_element_by_accessibility_id(self, accessibility_id: str) -> webelement:
        try:
            WebDriverWait(self.driver, self).\
                until(expected_conditions.presence_of_element_located((MobileBy.ACCESSIBILITY_ID, accessibility_id)))
        except WebDriverException:
            time.sleep(self.timeout)
        self.__screenshot_utils.take_screenshot()
        return self.driver.find_element_by_accessibility_id(accessibility_id)

    def find_element_by_css_selector(self, css_selector: str) -> webelement:
        try:
            WebDriverWait(self.driver, self.timeout).\
                until(expected_conditions.presence_of_element_located((MobileBy.CSS_SELECTOR, css_selector)))
        except WebDriverException:
            time.sleep(self.timeout)
        self.__screenshot_utils.take_screenshot()
        return self.driver.find_element_by_css_selector(css_selector)

    def find_element_by_custom(self, custom: str) -> webelement:
        try:
            WebDriverWait(self.driver, self.timeout).\
                until(expected_conditions.presence_of_element_located((MobileBy.CUSTOM, custom)))
        except WebDriverException:
            time.sleep(self.timeout)
        self.__screenshot_utils.take_screenshot()
        return self.driver.find_element_by_css_selector(custom)

    def find_element_by_image(self, image: str) -> webelement:
        try:
            WebDriverWait(self.driver, self.timeout).\
                until(expected_conditions.presence_of_element_located((MobileBy.IMAGE, image)))
        except WebDriverException:
            time.sleep(self.timeout)
        self.__screenshot_utils.take_screenshot()
        return self.driver.find_element_by_image(image)

    def find_element_by_link_text(self, link_text: str) -> webelement:
        try:
            WebDriverWait(self.driver, self.timeout).\
                until(expected_conditions.presence_of_element_located((MobileBy.LINK_TEXT, link_text)))
        except WebDriverException:
            time.sleep(self.timeout)
        self.__screenshot_utils.take_screenshot()
        return self.driver.find_element(MobileBy.LINK_TEXT, link_text)

    def find_element_by_partial_link_text(self, link_text: str) -> webelement:
        try:
            WebDriverWait(self.driver, self.timeout).\
                until(expected_conditions.presence_of_element_located((MobileBy.PARTIAL_LINK_TEXT, link_text)))
        except WebDriverException:
            time.sleep(self.timeout)
        self.__screenshot_utils.take_screenshot()
        return self.driver.find_element_by_partial_link_text(link_text)

    def find_element_by_name(self, name: str) -> webelement:
        try:
            WebDriverWait(self.driver, self.timeout).\
                until(expected_conditions.presence_of_element_located((MobileBy.NAME, name)))
        except WebDriverException:
            time.sleep(self.timeout)
        self.__screenshot_utils.take_screenshot()
        return self.driver.find_element_by_name(name)

    def find_element_by_tag_name(self, tag_name: str) -> webelement:
        try:
            WebDriverWait(self.driver, self.timeout).\
                until(expected_conditions.presence_of_element_located((MobileBy.TAG_NAME, tag_name)))
        except WebDriverException:
            time.sleep(self.timeout)
        self.__screenshot_utils.take_screenshot()
        return self.driver.find_element_by_tag_name(tag_name)

    def find_element_by_android_data_matcher(self, android_data_matcher: str) -> webelement:
        try:
            WebDriverWait(self.driver, self.timeout).\
                until(expected_conditions.
                      presence_of_element_located((MobileBy.ANDROID_DATA_MATCHER, android_data_matcher)))
        except WebDriverException:
            time.sleep(self.timeout)
        self.__screenshot_utils.take_screenshot()
        return self.driver.find_element_by_android_data_matcher(android_data_matcher)

    def find_element_by_android_uiautomator(self, android_uiautomator: str) -> webelement:
        try:
            WebDriverWait(self.driver, self.timeout).\
                until(expected_conditions.presence_of_element_located((MobileBy.ANDROID_UIAUTOMATOR,
                                                                       android_uiautomator)))
        except WebDriverException:
            time.sleep(self.timeout)
        self.__screenshot_utils.take_screenshot()
        return self.driver.find_element_by_android_uiautomator(android_uiautomator)

    def find_element_by_android_view_matcher(self, android_view_matcher: str) -> webelement:
        try:
            WebDriverWait(self.driver, self.timeout).\
                until(expected_conditions.
                      presence_of_element_located((MobileBy.ANDROID_VIEW_MATCHER, android_view_matcher)))
        except WebDriverException:
            time.sleep(self.timeout)
        self.__screenshot_utils.take_screenshot()
        return self.driver.find_element_by_android_view_matcher(android_view_matcher)

    def find_element_by_android_viewtag(self, android_viewtag: str) -> webelement:
        try:
            WebDriverWait(self.driver, self.timeout).\
                until(expected_conditions.presence_of_element_located((MobileBy.ANDROID_VIEWTAG, android_viewtag)))
        except WebDriverException:
            time.sleep(self.timeout)
        self.__screenshot_utils.take_screenshot()
        return self.driver.find_element_by_android_viewtag(android_viewtag)

    def find_element_by_ios_class_chain(self, ios_class_chain: str) -> webelement:
        try:
            WebDriverWait(self.driver, self.timeout).\
                until(expected_conditions.presence_of_element_located((MobileBy.IOS_CLASS_CHAIN, ios_class_chain)))
        except WebDriverException:
            time.sleep(self.timeout)
        self.__screenshot_utils.take_screenshot()
        return self.driver.find_element_by_ios_class_chain(ios_class_chain)

    def find_element_by_ios_predicate(self, ios_predicate: str) -> webelement:
        try:
            WebDriverWait(self.driver, self.timeout).\
                until(expected_conditions.presence_of_element_located((MobileBy.IOS_PREDICATE, ios_predicate)))
        except WebDriverException:
            time.sleep(self.timeout)
        self.__screenshot_utils.take_screenshot()
        return self.driver.find_element_by_ios_predicate(ios_predicate)

    def find_element_by_ios_uiautomation(self, ios_uiautomation: str) -> webelement:
        try:
            WebDriverWait(self.driver, self.timeout).\
                until(expected_conditions.presence_of_element_located((MobileBy.IOS_UIAUTOMATION, ios_uiautomation)))
        except WebDriverException:
            time.sleep(self.timeout)
        self.__screenshot_utils.take_screenshot()
        return self.driver.find_element_by_ios_uiautomation(ios_uiautomation)

    def find_element_by_windows_uiautomation(self, windows_uiautomation: str) -> webelement:
        try:
            WebDriverWait(self.driver, self.timeout).\
                until(expected_conditions.
                      presence_of_element_located((MobileBy.WINDOWS_UI_AUTOMATION, windows_uiautomation)))
        except WebDriverException:
            time.sleep(self.timeout)
        self.__screenshot_utils.take_screenshot()
        return self.driver.find_element_by_windows_uiautomation(windows_uiautomation)

    def find_elements_xpath(self, xpath: str) -> [webelement]:
        try:
            WebDriverWait(self.driver, self.timeout).\
                until(expected_conditions.
                      presence_of_element_located((MobileBy.XPATH, xpath)))
        except WebDriverException:
            time.sleep(self.timeout)
        self.__screenshot_utils.take_screenshot()
        elements: [webelement] = self.driver.find_elements_xpath(xpath)
        return elements

    def take_screenshot(self):
        """
        This method allows as to take a screenshot that will be saved in the folder of our current session
        :return: None
        """
        self.__screenshot_utils.take_screenshot()
