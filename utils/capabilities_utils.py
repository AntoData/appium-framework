import pathlib
import subprocess
import re
import json as js
import sys
import os
"""
To get to know how to use this project: https://github.com/AntoData/appium-framework/wiki
This module provides a collection of methods that automate the process of getting the capabilities needed to
instanciate an appium webdriver. We execute the adb commands provided by the Android SDK. We turn it into a json or
dict and write it in files o get it from files.
The key methods here are get_basic_capabilities_for_driver(), to_file_capabilities(capability_profile: str) and 
get_capabilities_from_file(capability_profile: str):
In order for all these to work you need to connect your phone or get your emulator up and running correctly and open
your app and keep the screen unlocked:
- get_basic_capabilities_for_driver() -> With this method we use different adb commands to return the capabilities
needed to instantiate a webdriver object and get our appium tests running
to_file_capabilities(capability_profile: str) -> This method calls to get_basic_capabilities_for_driver() and saves
the capabilities to a json file with name "capability_profile" in folder profiles
- get_capabilities_from_file(capability_profile: str): This method reads the json file named "capability_profile"
 in folder profiles with the capabilities needed for our appium tests
"""


def get_adb_properties() -> dict:
    """
    This method runs the command to get all adb properties and turns them into a dict
    :return: A dictionary that contains all the properties that adb returns when executed
    """
    # We execute the command 'adb shell getprop' which is a shell command that returns all properties of our device
    properties = subprocess.run("adb shell getprop", stdout=subprocess.PIPE)
    # We create an empty dictionary that will contain the properties of our device
    dict_properties: dict = {}
    # We turn the result of the executed command to string
    st_properties = str(properties.stdout)
    # The format of the result is of type [parameter]: [value] and we apply several transformations to the result
    # to turn the result into an array of strings where each line is a property
    st_properties = st_properties.replace("\\r", "")
    st_properties = st_properties.replace("[", "")
    st_properties = st_properties.replace("]", "")
    st_properties = st_properties.split("\\n")
    # We go through every line in that array of string
    for v_property in st_properties:
        # We split each line to get the key and value of the property and add it to the dictionary
        item: [str] = v_property.split(":", 1)
        if len(item) > 1:
            dict_properties[item[0]] = item[1]
    # We return the dictionary
    return dict_properties


def get_current_app_properties() -> bytes:
    """
    This method return the properties of our current connected device, we have to connect our device to our machine
    or have our emulator running.
    :return: Bytes that are the response of our adb command
    """
    # We execute the following command that returns only the properties of our current device
    properties = subprocess.run('adb shell "dumpsys window windows | grep -E "mCurrentFocus"',
                                stdout=subprocess.PIPE)
    # If because of the device we don't get anything after running that command, we run this other one
    if str(properties.stdout) == "b''":
        properties = subprocess.run('adb shell "dumpsys window windows | grep -E "mObscuringWindow"',
                                    stdout=subprocess.PIPE)
    # We return the response of that command
    return properties.stdout


def get_apppackage_appactivity() -> dict:
    """
    This method returns the properties related to the app that we are executing at the moment So in order for this to
    work, we need to have that app running
    :return: A dictionary that contains the properties needed to run a test for our current app
    """
    # We use the method get_current_app_properties described above to get all the properties for our current app
    st_properties: [str] = str(get_current_app_properties())
    # We perform several transformation in that variable to get the properties in the right format
    st_properties = re.search("[a-zA-Z.0-9]+/[a-zA-Z.0-9]+", st_properties)
    package_activity = st_properties.group(0)
    # We split the different properties that are part of that property we selected previously
    package_activity = package_activity.split("/")
    # We build the dictionary with the right properties for our current app
    activity_app_dict = {"appPackage": package_activity[0], "appActivity": package_activity[1]}
    # We return that dictionary
    return activity_app_dict


def get_device_properties() -> dict:
    """
    This method returns a dictionary with the properties that adb offers related to our device (real connected
    device or an emulator)
    :return: A dictionary that contains the properties related to our device
    """
    # We call to the method get_adb_properties described previously to get all the properties adb offers
    dict_properties: dict = get_adb_properties()
    # We create an empty dictionary
    dict_device_properties: dict = {}
    # We the property "ro.build.software.version" to a variable called v_so
    if "ro.build.software.version" in dict_properties.keys():
        v_so = dict_properties["ro.build.software.version"]
        # We perform a series of transformations to that property's value
        v_so = v_so.replace(" ", "")
        v_so = re.split('(\d+)', v_so)
        # We add to the variable dict_device_properties the properties we will need to perform our tests
        dict_device_properties["platformName"] = v_so[0]
        dict_device_properties["platformVersion"] = v_so[1]
    elif "ro.build.version.release" in dict_properties.keys():
        dict_device_properties["platformName"] = dict_properties["gsm.operator.alpha"].replace(" ", "")
        dict_device_properties["platformVersion"] = dict_properties["ro.build.version.release"].replace(" ", "")
    dict_device_properties["deviceName"] = dict_properties["ro.product.device"]
    # We return that dictionary
    return dict_device_properties


def get_basic_capabilities_for_driver() -> dict:
    """
    This method collects the capabilities from our app and our device using the methods described previously
    and combines them into a dictionary that contains all the capabilities needed to instantiate the webdriver
    to perform our test. In order for this to work, we need to have our device connected and our app running
    :return: The dictionary result of combining the capabilities described above
    """
    # We get properties of our device and save it to a dictionary
    dict_device_properties: dict = get_device_properties()
    # We get the properties of the main activity of our app
    activity_app_dict: dict = get_apppackage_appactivity()
    # We create an empty dictionary
    basic_capabilities: dict = {}
    # We add the capabilities of our device to the dictionary we created
    basic_capabilities.update(dict_device_properties)
    # We add the automationName capability (which is needed)
    basic_capabilities["automationName"] = "UiAutomator1"
    # We add also the dictionary with the capabilities for our app and activity
    basic_capabilities.update(activity_app_dict)
    # We also add the property for the timeout to start the test
    basic_capabilities["adbExecTimeout"] = "200000"
    # We return the dictionary with all the basic capabilities that we need to instantiate a webdriver
    return basic_capabilities


def to_file_capabilities(capability_profile: str) -> None:
    """
    This method call to method get_basic_capabilities_for_driver described above to get all the basic capabilities
    needed to instantiate a webdrive instance and perform a test and saves them to a json file in folder selectors
    with name capabilitiy_profile (for this to work with this framework this file should have the same name in lower
    case than the class for the page object of the activity where the test for our app starts
    :param capability_profile: This will be the name of the json file we will generate in folder profiles. In order
    for this to work in our framework, it should be the name of the class for the first page object where our app starts
    in lower case
    :return: None
    """
    # We call to get_basic_capabilities_for_driver to get the basic capabilities to perform our test for our app and
    # device
    capabilities: dict = get_basic_capabilities_for_driver()
    # We turn this into a json object
    json = js.dumps(capabilities)
    # We create a None variable that will contain the file where we will save this json object
    f = None
    # We write our file inside a try/except block to catch possible exceptions
    try:
        # We generate the path for our file in folder profiles
        profile_path: str = str(pathlib.Path().absolute()) + "\\..\\" + "\\profiles\\" + capability_profile
        # We create that file (using mode w+)
        f = open("{0}.json".format(profile_path), "w+")
        # We write our object json into our file
        f.write(json)
    # We catch any possible exception
    except Exception as e:
        print("There was an exception when getting the capabilities to file: {0}".format(e))
        exc_type, exc_obj, exc_tb = sys.exc_info()
        fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
        print(exc_type, fname, exc_tb.tb_lineno)
    finally:
        # We always check if f is not None, so we have opened/created our file
        if f is not None:
            # And in that case we close it
            f.close()


def get_capabilities_from_file(capability_profile: str) -> dict:
    """
    This method reads a json file named capabilitiy_profile in folder profiles and return a dict with the capabilities
    that were included in that file
    :param capability_profile: Name of the file in folder profiles
    :return: Dictionary with all the capabilities included in that json file
    """
    # We create a variable that will contain the dictionary with value None (so if we can't read the file we return
    # None)
    capabilities_dict = None
    try:
        # Inside a try/except block we read the file that turn it into a dictionary in the variable created to None
        # previously
        if os.path.exists(str(pathlib.Path().absolute()) + "\\..\\" + "\\profiles\\" + capability_profile):
            with open(str(pathlib.Path().absolute()) + "\\..\\" + "\\profiles\\" + capability_profile, 'r') as f:
                capabilities_dict = js.load(f)
        else:
            with open(str(pathlib.Path().absolute()) + "\\profiles\\" + capability_profile, 'r') as f:
                capabilities_dict = js.load(f)
    # We catch any exception that might happen
    except Exception as e:
        print("There was an error while getting capabilities from file {0}: {1}".format(capability_profile, e))
        exc_type, exc_obj, exc_tb = sys.exc_info()
        fname: str = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
        print(exc_type, fname, exc_tb.tb_lineno)
    finally:
        # In case variable f is not None, it means we got to open that file, so we clase it
        if f is not None:
            f.close()
    # We return the dictionary with the capabilities
    return capabilities_dict
