import os
import subprocess
import unittest
import configparser
import pathlib
import threading
import time
import sys
from appium.webdriver.appium_service import AppiumService
sys.path.append(str(pathlib.Path().absolute())+"/../videoRecorder/videoRecorder")
sys.path.append(str(pathlib.Path().absolute())+"/../videoRecorder")

"""
This module is the one we use when we want to run several test suites in different devices. We only have to run this
module completely and set the file "scheduled-tests.ini" in the main folder. We set the test in that file as follows:
[Test 1]
profile_file = <Profile JSON file in folder profiles we want to use for this test, ex: "instagramloginappprofile.json">
test_suite_file = <Test suite module in folder test_suites, for ex: "instagram_suite">
device = <real (USB connected mobile device) or installed virtual device for ex: Pixel_2_API_28>

[Test 2]
profile_file = <...>
test_suite_file = <...>
device = <...>
"""
# This is a global variable that we will use to start and stop the appium server
appium_service = AppiumService()


def start_appium_server_cmd_line() -> None:
    """
    This method just starts the appium server using the global variable
    :return: None
    """
    os.system("appium")


def start_appium_service_cmd_line() -> None:
    """
    This method just starts the appium service using the global variable
    :return: None
    """
    appium_service.start()


def stop_appium_service_cmd_line() -> None:
    """
    This method just stops the appium service using the global variable
    :return: None
    """
    appium_service.stop()


def adb_start_server() -> None:
    """
    This method starts the adb server using the command line
    :return: None
    """
    try:
        stdout = subprocess.run("adb start-server", stdout=subprocess.PIPE)
        print(stdout.stdout)
    except subprocess.SubprocessError:
        print("adb start-server didn't work, sorry")


def adb_stop_server() -> None:
    """
    This method kills all processes related to appium server in Windows (if it does not work, we catch the exception)
    :return: None
    """
    try:
        stdout = subprocess.run("taskkill /F /IM node.exe", stdout=subprocess.PIPE)
        print(stdout.stdout)
    except subprocess.SubprocessError:
        print("This works only in Windows, sorry")


def start_virtual_device(device: str) -> None:
    """
    This method starts the virtual device in the parameter device using the command for it in command line
    :param device: This is a string where we set the name of the virtual device to start
    :return: None
    """
    try:
        stdout = subprocess.run("emulator -avd {0}".format(device), stdout=subprocess.PIPE)
        print(stdout.stdout)
    except subprocess.SubprocessError:
        print("We could not start the device, sorry")


def stop_virtual_device() -> None:
    """
    This method kills the current virtual device running
    :return: None
    """
    stdout = subprocess.run("adb -s emulator-5554 emu kill", stdout=subprocess.PIPE)
    print(stdout.stdout)


def scheduler():
    """
    This is the main method in this module that will be run when we run this module. Here we basically start
    the appium server, we read the file "scheduled-tests.ini" and go one group of variables by one getting the
    different variables to set our environment to run our tests one after the other
    :return: None
    """
    appium_server = threading.Thread(target=start_appium_server_cmd_line, args=())
    appium_server.start()
    # We start the appium server
    start_appium_service_cmd_line()
    # We start adb server in a new thread
    adb_server = threading.Thread(target=adb_start_server, args=())
    adb_server.start()
    # We create the configparser object
    config: configparser.ConfigParser = configparser.ConfigParser()
    # We build the path to the file .ini in folder selector
    scheduler_path: str = str(pathlib.Path().absolute()) + "\\..\\" + "scheduled-tests.ini"
    # We read the file scheduled-tests.ini that contains the variables to run our tests, one by one
    config.read(scheduler_path)
    # We go through every key in that file that represents each test we want to run
    for key in config.keys():
        # This will contain a key DEFAULT which we have to skip
        if key != "DEFAULT":
            # We get the variables for our current test
            current_test_parameters = config[key]
            # If the parameter "device" is not "real", it means we have to start a virtual device
            if current_test_parameters["device"] != "real":
                # We start the process to start a virtual device in a new thread
                virtual_device = threading.Thread(target=start_virtual_device,
                                                  args=(current_test_parameters["device"],))
                virtual_device.start()
                # We wait for 180 seconds to wait for the virtual device to be completely started
                time.sleep(120)
            # We created a unittest test suite object
            suite = unittest.TestSuite()
            # We create a variable to None
            file = None
            try:
                # We create a file "../tmp/current_test_profile.txt" which will contain the name of the json profile
                # file we want to use for our current test and that the abstract class in module appwindowobject.py
                # will read to run the test in the right device with the right settings
                file = open("../tmp/current_test_profile.txt", "+w")
                # We write the name of the profile_file we set in scheduled-tests.ini in this temp file
                file.write(current_test_parameters["profile_file"])
            except FileNotFoundError as e:
                # We catch exceptions
                print("We can't create the file current_test_profile.txt: {0}".format(e))
            finally:
                # We always close this file if it was created and opened, which means in case it is not None
                # This is extremely important as the file will be opened in class in the module appwindowobject.py
                if file is not None:
                    file.close()
            try:
                # If the module defines a suite() function, call it to get the suite.
                mod = __import__("test_suites."+current_test_parameters["test_suite_file"], globals(), locals(),
                                 ['suite'])
                suitefn = getattr(mod, 'suite')
                suite.addTest(suitefn())
            except (ImportError, AttributeError):
                # else, just load all the test cases from the module.
                suite.addTest(unittest.defaultTestLoader.loadTestsFromName("test_suites." +
                                                                           current_test_parameters["test_suite_file"]))
            unittest.TextTestRunner().run(suite)
            # Once we run that suite, if this was run in a virtual device we stop that virtual device as it will be no
            # longer needed and will be wasting memory and affecting our performance
            if current_test_parameters["device"] != "real":
                stop_virtual_device()

if __name__ == '__main__':
    try:
        scheduler()
    finally:
        # Once we run all suites we stop the appium server
        stop_appium_service_cmd_line()
        # We stop all processes of adb server
        adb_stop_server()
