from appium.webdriver import webdriver
from datetime import datetime
from selenium.common.exceptions import WebDriverException

"""
To get to know how to use this project: https://github.com/AntoData/appium-framework/wiki
"""


class ScreenshotUtils:
    """
    This class provides a key tool for this framework as it is the missing piece that automates the process of getting
    screenshots and saves then in the right folder with the right name
    """
    def __init__(self, driver: webdriver):
        """
        This class receives a webdriver that will be used to get the screenshot and using the custom made capability
        "screenshots_path" that we added in the abstract class appwindowobject to know in which folder we want these
        screenshots to be saved
        :param driver: Instance of webdriver
        """
        self.__driver = driver

    def take_screenshot(self) -> None:
        """
        This method takes a screenshot in the right folder for the test that is current being run
        :return: None
        """
        # We get the current date and time
        now = datetime.now()
        # We turn it to string with precision to the millisecond, this will be the name of the screenshot
        current_timestamp = now.strftime("%Y_%m_%d-%H_%M_%S_%f")
        # We get the path for the folder where we will save the screenshot for the capability "screenshots_path"
        # that was added to that instance of the driver in the constructor
        intial_path: str = self.__driver.capabilities["screenshots_path"]
        # We build the whole path to the png file
        intial_path = intial_path + "//" + current_timestamp + ".png"
        # We use a try/except block to perform the screenshot to catch any possible exception and keep going in that
        # case
        try:
            # We perform the screenshot
            self.__driver.get_screenshot_as_file(intial_path)
        except WebDriverException as e:
            # We catch this exception, this can be a common exception as the developer can forbid getting a screenshot
            # of a view if the flag detailed below is set in a particular value
            # We will just tell the user and go on
            print("{0}: We can't take a screenshot of this view, the developer set the following flag"
                  " 'LayoutParams.FLAG_SECURE'".format(e))
            print("We caught this and go on with the execution")
