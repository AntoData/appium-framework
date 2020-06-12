# appium-framework
 
This framework provides several features to make your appium projects more easy and standarized. We included features to get the JSON needed to test an Android application, the management of xpaths, ids and other selectors, automatic screenshots, automatic videos and also to schedule the execution of different apps in different devices, real or virtual also remote apps in BitBar.

Our project contains the following packages, modules and files:

- <b>abs_class</b>: In this folder we include all abstract classes used in this project
  - <b>appwindowobject.py</b>: This module contains the abstract class AppWindowObject:
     This is an abstract class that should be the parent of every "page object" class, it manages the driver creation and connection to the appium server, the managing of JSON files, driver capabilities... All our classes in folder app_window_objects must extend this one
- apks: This folder should contains the files apk in case we want to install an application in a device
- <b>app_window_objects</b>: In this class we should include the modules that contain the classes that will interact with our app, the ones where we define the methods that interact with our app (clicking in buttons,...)
- <b>profiles</b>: Here is where we should have all the JSON files. We will extract the desired capabilities for our webdrives from these files.
- screenshots: For each test we will generate a folder here and all screenshots taken during that screenshot will be placed there
- <b>selectors</b>: Here is where we should store the ini files that contain the xpaths, ids, ... needed in a page object class. In order for this framework to work, these files must have the same name that the class where they will be used in lowercase
- test_reports: Here we will store the reports generated after the execution of all tests we have scheduled
- <b>test_suites</b>: Here is where we will store all the test suite classes, these classes will extend the class unittest.TestCase:
  - <i>The method setUp should be overwritten and contain the instantiation of the main/first page object that is the one that connects to appium and also where we create the object to record a video and start the recording session. Also we should overwrite the method tearDown to stop the recording session after every test</i>
- tmp: Here is where we will save a tmp file where we will tell the class appwindowobject which JSON file it should extract the capabilities from in this iteration when using the scheduler feature.
- utils: Here we included several modules that contains several interesting and useful modules for this framework. For instance, a script that helps us to get the JSON file to execute test in our current device and app.
- videoRecorder: Here we included the classes that allow us to record videos for each test
- videos: In this folder we will create the folders where we will save our videos for each recording session
- <b>interactive_test_runner.py</b>: If everything is set up fine, when executing this script our tests will start running in the order specified in scheduled-tests.ini
- npm-requirements.txt: Requirements for npm
- requirements.txt: Required Python modules for this project to ber installed using pip install
- <b>scheduled-tests.ini</b>: In this file, we will provide the order in which we want our test suites to be executed. Also, we will set in each test suite which JSON file to use and which device to run our tests in.
