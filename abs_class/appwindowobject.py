import os
from abc import ABC
import configparser
import pathlib
from datetime import datetime
from appium import webdriver

from utils.bitbar_file_uploader import upload_file_to_bitbar
from utils.capabilities_utils import get_capabilities_from_file
import utils.webdriver_find_utils as wu
from utils.screenshot_utils import ScreenshotUtils
from videoRecorder.videoRecorder.desktopBrowserRecorder import DesktopBrowserRecorder

"""
To get to know how to use this project: https://github.com/AntoData/appium-framework/wiki
"""


class AppWindowObject(ABC):
    """
    This is an abstract class that would be the parent of every "page object" class
    """

    def __init__(self, driver: webdriver = None):
        """
        This is the constructor for every "page object" class. We have a parameter driver that will establish how
        we create this new object. If that object is None, it will be because it is the first page object that will
        be created in our test. In that we will have to get the file ".json" in the folder profiles that will have
        the same name as our class in lower case which will be a json file with the capabilities needed to start our
        app in our device.
        If we passed a webdriver object in the parameter driver, we will use that one as the webdriver object in our
        class
        However the case is, we will search for a file ".ini" that will be in folder "selectors" that will have the same
        name as our class in lower case and will contain the different ids and xpaths for that page object and we will
        save then in different dictionaries (one for ids, one for xpaths) that so they will be available at any point
        in our tests
        :param driver: Webdriver object that will decide if we generate the connection to our app and device from the
        beginning or we reuse that object to keep with our test
        """
        # We get the configparser object from the file .ini with the same name as our class in folder selectors
        config: configparser.ConfigParser = self.get_selectors_config(type(self).__name__.lower())
        # We get the section ID that contains the selectors of type id from object configparser and
        # assign it to the dictionary id that is a property of our class
        self.id: dict = dict(config["ID"])
        # We get the section ID that contains the selectors of type xpath from object configparser and
        # assign it to the dictionary xpath that is a property of our class
        self.xpath: dict = dict(config["XPATH"])
        # We will also have a property capabilities
        self.capabilities = None
        # We will have a property called driver of type webdriver that we will use as our appium webdriver
        self.driver: webdriver = None
        # If the parameter driver is None, it means we have to get the capabilities from the file .json with the same
        # name as our class in lower case in folder profiles to connect with appium and our app and create a new driver.
        # This will have to be done for the first page object in our app
        if driver is None:
            # We get the capabilities from the json file with the same name as our class in lower case in folder
            # profile or with the json file that has been written in the temporal file "../tmp/current_test_profile.txt"
            # if this was run from the module interactive_test_runner.py which allows us to schedule and program
            # different test in different devices to be run one after the other
            profile_file: str = ""
            file = None
            # We try to open the file where the json file is set
            try:
                if os.path.exists("../tmp/current_test_profile.txt"):
                    file = open("../tmp/current_test_profile.txt", "r")
                else:
                    file = open("./tmp/current_test_profile.txt", "r")
                # If it exists we read it, line by line
                for line in file:
                    # We add the line to the variable profile_line
                    profile_file += line
            except FileNotFoundError as e:
                # In case the file does not exist, we just pass because it means we are running this using the
                # module in test_suites
                print("tmp file not found: {0}".format(e))
            finally:
                # However, we always try to close the file and remove it in case it exists
                if file is not None:
                    file.close()
            # If the variable profile_file is None or "", means that we didn't read which json profile file we have to
            # use, which means we run this probably from the test suite module, so we use the default file
            if profile_file is None or profile_file == "":
                self.capabilities: dict = get_capabilities_from_file(type(self).__name__.lower() + "profile.json")
            else:
                # In other case, we set a specific json profile file, so we use it
                self.capabilities: dict = get_capabilities_from_file(profile_file)
            self.capabilities["bitbar_project"] = type(self).__name__.lower()
            # If it is a remote test, we check if we provided an ID in bitbar_app (ids are decimal)
            if "bitbar_app" in self.capabilities.keys() and not self.capabilities["bitbar_app"].isdecimal():
                # If we did not, we call the method upload_file_to_bitbar to upload the file in folder apk
                # we set in variable bitbar_app, get the ID of that file uploaded to bitbar and set it as the
                # new value of capability bitbar app, so we can execute our remote test
                self.capabilities["bitbar_app"] = upload_file_to_bitbar(self.capabilities["bitbar_app"])
            # We create the webdriver instance using the capabilities we got from the json file
            # If our capabilities have the key "bitbar_key", it means we are running a remote test
            if "bitbar_apiKey" in self.capabilities.keys():
                print("Remote test")
                # So we get the server we set up in the folder profiles in file config_parameters.ini for
                # variable remote in section SERVERS
                server: str = self.get_server("remote")
            else:
                # Otherwise, we are running a local test and we have to give variable server the value of the
                # parameter local in section SERVERS
                print("Local test")
                server: str = self.get_server("local")

            # If we have this capability we have to install the apk in the device
            if "apk_install" in self.capabilities.keys():
                app_path = str(pathlib.Path().absolute()) + "\\..\\apks\\{0}".format(self.capabilities["apk_install"])
                if os.path.exists(app_path):
                    self.capabilities["app"] = app_path
                else:
                    self.capabilities["app"] = str(pathlib.Path().absolute()) + \
                                               "\\apks\\{0}".format(self.capabilities["apk_install"])

            # We create the instance of the webdriver for our app
            self.driver: webdriver = webdriver.Remote(server, self.capabilities)

            # We automatically start a recording session to record all our interactions with appium
            self.video_recorder = DesktopBrowserRecorder(".mp4", self.driver)
            self.video_recorder.start_recording_session()

            # As this is the first activity of the test, we have to create the folder for the screenshots for this
            # test in the folder screenshots
            # In order to do so, we first get the current date and time
            now = datetime.now()
            # We turn that object into str with the following format
            current_timestamp: str = now.strftime("%Y_%m_%d-%H_%M_%S")
            # Now we build the path for this new folder that will contain the screenshots for this test
            # We get the current path, then go to folder screenshots and then we build the name of the new folder
            # as the current time and date we got earlier as string plus the name of the current class in lower case
            platform: str = ""
            if "platformName" in self.driver.capabilities.keys():
                platform = self.driver.capabilities["platformName"]
            device_name: str = ""
            if "deviceName" in self.driver.capabilities.keys():
                device_name = self.driver.capabilities["deviceName"]
            path: str = str(pathlib.Path().absolute()) + "\\..\\" + "\\screenshots\\"
            if os.path.exists(path):
                initial_path: str = str(pathlib.Path().absolute()) + "\\..\\" + "\\screenshots\\" + \
                                    current_timestamp + "_" + type(self).__name__.lower() + \
                                    "_{0}_{1}".format(platform, device_name)
            else:
                initial_path: str = str(pathlib.Path().absolute()) + "\\screenshots\\" + \
                                    current_timestamp + "_" + type(self).__name__.lower() + \
                                    "_{0}_{1}".format(platform, device_name)
            # Now we create that folder
            os.mkdir(initial_path)
            # We save this path as a capability of our driver, so we can get it from our driver in the future
            self.driver.capabilities["screenshots_path"] = initial_path
        else:
            # Otherwise we just assign the parameter driver to our property driver
            self.driver: webdriver = driver
        # We always add a property called screenshot_util that contains the object ScreenshotUtils with the driver
        # with the capability "screenshots_path" so we can use it to get a screenshot whenever we want that is saved
        # in the right folder
        self.screenshot_util = ScreenshotUtils(self.driver)
        # We get an instance of WebDriverUtils and assign it to the property locators. This is a class that provides
        # a list of functions to find elements with implicit wait
        self.locators: wu.WebDriverFindUtils = wu.WebDriverFindUtils(self.driver)

    @staticmethod
    def get_selectors_config(selector: str) -> configparser.ConfigParser:
        """
        This method searches for the file .ini with the same name selector in the folder selectors and creates a
        configparser object with the information for id and xpath selectors
        :param selector: Name of the ini file in folder selector that we want to open and read
        :return: Configparser object that has parsed the information in the file .ini that we selected
        """
        # We create the configparser object
        config: configparser.ConfigParser = configparser.ConfigParser()
        # We build the path to the file .ini in folder selector
        selector_path: str = str(pathlib.Path().absolute()) + "\\.." + "\\selectors\\" + selector + ".ini"
        if not os.path.exists(selector_path):
            selector_path: str = str(pathlib.Path().absolute()) + "\\selectors\\" + selector + ".ini"
        # We read that file
        print(selector_path)
        config.read(selector_path)
        # We return the configparser object
        return config

    @staticmethod
    def get_server(class_name: str) -> str:
        """
        This method reads the file config_parameters.ini in folder profiles using config parser and returns the
        server url in section SERVERS and assigned to parameter class_name
        :param class_name: Parameter we will get from file config_parameters.ini section SERVERS
        :return: Server url for class with name class_name
        """
        # We create an object of type configparser
        config: configparser.ConfigParser = configparser.ConfigParser()
        # We generate the path to the file config_paramters.ini in folder profiles
        if os.path.exists(str(pathlib.Path().absolute()) + "\\.." + "\\profiles\\config_parameters.ini"):
            config_path: str = str(pathlib.Path().absolute()) + "\\.." + "\\profiles\\config_parameters.ini"
        else:
            config_path: str = str(pathlib.Path().absolute()) + "\\profiles\\config_parameters.ini"
        # We read that file and parse its information
        config.read(config_path)
        # We return the url assigned to the parameter with name class_name in section SERVERS
        return config["SERVERS"][class_name]

    def destroy(self):
        """
        This method stops our current recording session and quits our driver, destroys our object
        :return: None
        """
        self.video_recorder.stop_recording_session()
        self.driver.quit()
