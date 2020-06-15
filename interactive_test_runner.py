import os
import subprocess
import unittest
import configparser
import pathlib
import threading
import time
import sys
from datetime import datetime

from psutil import process_iter
from signal import SIGTERM  # or SIGKILL
from appium.webdriver.appium_service import AppiumService

from utils.report_utils import ReportUtils

sys.path.append(str(pathlib.Path().absolute())+"/../videoRecorder/videoRecorder")
sys.path.append(str(pathlib.Path().absolute())+"/../videoRecorder")

"""
To get to know how to use this project: https://github.com/AntoData/appium-framework/wiki

This module is the one we use when we want to run several test suites in different devices. We only have to run this
module completely and set the file "scheduled-tests.ini" in the main folder. We set the test in that file as follows:
[Test 1]
profile_file = <Profile JSON file in folder profiles we want to use for our test, ex: "instagramloginappprofile-g.json">
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
    # We kill any process that is listening in port 4723
    for proc in process_iter():
        for conns in proc.connections(kind='inet'):
            if conns.laddr.port == 4723:
                proc.send_signal(SIGTERM)
    # We execute the command appium to start the server
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
    # We create the file to store the report for the results of the test suites we are going to execute
    report_file = ReportUtils()
    # We create this variables to control threads for starting and stopping appium and adb servers
    appium_server = None
    adb_server = None
    # We create the configparser object
    config: configparser.ConfigParser = configparser.ConfigParser()
    # We build the path to the file .ini in folder selector
    scheduler_path: str = str(pathlib.Path().absolute()) + "\\" + "scheduled-tests.ini"
    # We read the file scheduled-tests.ini that contains the variables to run our tests, one by one
    config.read(scheduler_path)
    # We go through every key in that file that represents each test we want to run
    for key in config.keys():
        # This will contain a key DEFAULT which we have to skip
        if key != "DEFAULT":
            # We get the variables for our current test
            current_test_parameters = config[key]
            # If the parameter "device" is not "remote", it means we have to start the adb service, appium server...
            if current_test_parameters["device"] != "remote":
                appium_server = threading.Thread(target=start_appium_server_cmd_line, args=())
                appium_server.start()
                # We start the appium server
                start_appium_service_cmd_line()
                # We start adb server in a new thread
                adb_server = threading.Thread(target=adb_start_server, args=())
                adb_server.start()
            # If the parameter "device" is not "real", it means we have to start a virtual device
            if current_test_parameters["device"] != "real" and current_test_parameters["device"] != "remote":
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
                file = open("./tmp/current_test_profile.txt", "+w")
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
            # We get the current instant to know when we started executing our suite
            now = datetime.now()
            # We build the first line for this suite stating when we started running it
            first_line: str = "We started executing this test suite at {0}:\n".format(now.strftime("%d-%m-%Y_%H-%M-%S"))
            second_line: str = "Tests to perform: \n"
            # We write in the report file the information about the test suite before running
            report_file.write_line_in_file(first_line)
            report_file.write_line_in_file(second_line)
            report_file.write_line_in_file(report_file.get_tests_from_suite(suite))
            # We run the test suite
            results = unittest.TextTestRunner().run(suite)
            # We get the number of tests run
            runs = results.testsRun
            # We get the errors during the execution of the test suite
            errors = results.errors
            # We get the time when our test suite stopped
            now_end = datetime.now()
            end_time_str = now_end.strftime("%d-%m-%Y_%H-%M-%S")
            # We build the lines for and write them to the report
            report_test_numbers: str = "We run {0} tests\n".format(runs)
            report_file.write_line_in_file(report_test_numbers)
            report_finished: str = "The execution finished at {0}\n".format(end_time_str)
            report_file.write_line_in_file(report_finished)
            report_failed: str = "The following failed {0}\n".format(errors)
            report_file.write_line_in_file(report_failed)
            # Once we run that suite, if this was run in a virtual device we stop that virtual device as it will be no
            # longer needed and will be wasting memory and affecting our performance
            if current_test_parameters["device"] != "real" and current_test_parameters["device"] != "remote":
                stop_virtual_device()
            # After running our test suite, if our device was not remote we have to stop appium and adb
            if current_test_parameters["device"] != "remote":
                # If appium_server was created
                if appium_server is not None:
                    # We stop the thread
                    # appium_server.join()
                    pass
                # We stop the appium server
                stop_appium_service_cmd_line()
                # We stop adb server if it was created, stopping its thread
                if adb_server is not None:
                    adb_server.join()
    report_file.close_file()


if __name__ == '__main__':
    try:
        scheduler()
    finally:
        # Once we run all suites we stop the appium server
        stop_appium_service_cmd_line()
        # We stop all processes of adb server
        adb_stop_server()
