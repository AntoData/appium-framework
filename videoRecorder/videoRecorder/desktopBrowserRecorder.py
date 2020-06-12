__version__ = "0.2.5"
import time
import threading
from datetime import datetime
import os
import imageio
from selenium.common.exceptions import WebDriverException

"""
Created on 28 feb. 2020

@author: ingov
This module contains the following classes:
    DesktopBrowserRecorder: This is the main class in this module. In order to record your desktop
    or a browser opened during a selenium automatic test, you just have to create an object of this
    class. The constructor can get 3 parameters folder, encoding and optionally driver. Folder is
    the path where you want the folder for the recording session to be created, encoding is the
    extension for the video (so far it is only tested and possible using .mp4) and driver is an
    optional parameter. It is a webdriver object, if you pass it to the constructor you will be
    recording the actions taken in the browser controlled by that object if you don't you will
    just record your desktop.
    In order to start a recording session, just use the method start_recording_session offered by
    the object.
    In order to stop it, just use the method stop_recording_session offered by the object
    
    SessionStartedException: It is a called that inherits from the built-in class Exception.
    We just use it to define a custom made exception in case we want to start a recording
    session in an object that is already running a recording session.
    
    NoSessionStartedException: It is a called that inherits from the built-in class Exception.
    We just use it to define a custom made exception in case we want to stop a recording
    session in an object that is not running a recording session.    
"""


class DesktopBrowserRecorder:
    """ 
    This is a class that allows you to record your desktop or a webdriver-driven browser for
    automatic testing.
      
    Attributes: 
        driver (wedriver): A webdriver to get screenshots in case we want to record a selenium.
        webdriver-driven automatic test. By default is None and if we don't provide it in __init__
        we will the desktop.
        __folder (str): The __folder where we want the videos to be saved.
        __encoding (str): The __encoding of the video, .mp4 recommended and tested.
        __keeprecording (bool): Flag that indicated the algorithm if it has to keep recording or stop.
        frame (obj): Current frame taken from the desktop or the browser that will be added to the video.
        __thread (theard): As this process will be all performed in another threard, this is where
        we will store that __thread so we can start it or stop it and that way start or stop the recording
        session.
        """

    def __init__(self, encoding, driver=None):
        """
        The constructor for DesktopBrowserRecorder class.
        :param encoding: The encoding of the video, .mp4 recommended and tested.
        :param driver: A webdriver to get screenshots in case we want to record a selenium.
        By default is None, in that case we will record the desktop and not the browser opened
        by this webdriver
        """
        self.driver = driver
        folder = "..//videos"
        if os.path.exists(folder):
            self.__folder = folder
        else:
            self.__folder = ".//videos"
        self.__sessionPath = ""
        self.__encoding = encoding
        # To start __keeprecording will be False for starters
        self.__keeprecording = False
        # To start our frame will be None until we capture an image to use for the video
        self.frame = None
        # Until we start the recording session this will be None
        self.__thread = None
        
    def __threat_take_screenshot(self):
        """
        This function takes the screenshot that will be added to the video in a different __thread
        than the main __thread. The screenshot will be of the webdriver or the desktop depending
        on what we set in the constructor.
        :return: None
        """
        # This parameter contains the path to the file where we will save the frame
        frame_file_name = self.__sessionPath+"/frame.png"
        # We will keep iterating until the recording session is stopped
        while self.__keeprecording:
            # If self.driver is not None, means we are recording a webdriver browser
            if self.driver is not None:
                # We save our browser screenshot in the file for the frame
                try:
                    self.driver.save_screenshot(frame_file_name)
                except WebDriverException as e:
                    print("{0}: We can't take a screenshot of this view, the developer set the following flag"
                          " 'LayoutParams.FLAG_SECURE'".format(e))
                    print("We caught this and go on with the execution")
            else:
                # Otherwise, we are recording the desktop and take the screenshot from
                # the desktop and save it too to the frame file
                # pyautogui.screenshot(frame_file_name)
                pass
            # We use imageio to open that file and assign it to the attribute frame
            # that we will use to add to the video in the main threat
            self.frame = imageio.imread(frame_file_name)
            # As we are using a 20fps configuration, we sleep for 1/25 seconds
            time.sleep(1/25)
    
    def __build_writer(self):
        """
        This function builders the writer for the class imageio that we will use
        to builder the video. We will use this to build the video writer for our
        current video.
        :return: None
        """
        # We get the current date and time
        now = datetime.now()
        # We use the current date and time and the class attribute __encoding to create the
        # video file name
        file_name = now.strftime("%d-%m-%Y_%H-%M-%S") + self.__encoding
        # We use the recording session __folder and file name to builder the imageio video
        # writer that we will use to create our video
        writer = imageio.get_writer(self.__sessionPath+"/"+file_name, fps=20)
        # We return this object
        return writer
    
    def __main_thread_recording_session(self):
        """
        As the recording process should be done in a parallel __thread to the execution of
        the program where we want to start a recording, we have to define this function
        that contains the main parallel __thread to the program that will be started
        when we start the recording session (using the class method start recording
        session).
        :return: None
        """
        # We get the current instant to the second to build the __folder which
        # will contain the videos resulting of our recording session
        now = datetime.now()
        # We build that path to contain the videos resulting from our recording session
        platform: str = ""
        if "platformName" in self.driver.capabilities.keys():
            platform = self.driver.capabilities["platformName"]
        device_name: str = ""
        if "deviceName" in self.driver.capabilities.keys():
            device_name = self.driver.capabilities["deviceName"]
        app_activity: str = ""
        if "appActivity" in self.driver.capabilities.keys():
            app_activity = self.driver.capabilities["appActivity"]
        self.__sessionPath = self.__folder + "\\"+now.strftime("%d-%m-%Y_%H-%M-%S") + \
                             "_{0}_{1}_{2}".format(platform, device_name, app_activity)
        try:
            # We create that __folder
            os.mkdir(self.__sessionPath)
        except Exception as e:
            print(e)
        # We create the secondary thread that will start taking the screenshots that will
        # build our video
        x = threading.Thread(target=self.__threat_take_screenshot, args=())
        # We use the method __build_writer to get the video writer that will create and build
        # our current video
        writer = self.__build_writer()
        # We start the secondary __thread that will start taking the screenshots
        x.start()
        # While the flag __keeprecording is True, we will keep adding frames to our video
        # or create a new video if case something happens to our current video
        while self.__keeprecording:
            try:
                # If the frame is not None, if we already have a frame, we add it to the video
                if self.frame is not None:
                    writer.append_data(self.frame)
            except (BufferError, Exception):
                # In case there is an exception when trying to add the frame to the video
                # we close the writer
                writer.close()
                # We create a new one
                writer = self.__build_writer()
                if self.frame is not None:
                    # Again we try to add the frame to the new video
                    writer.append_data(self.frame)
                # NOTE: This is the best way to prevent problems when the size of a browser changes
                # in that case, an exception occurs because all frame in a video must have the same size
                # so we create a new video in the same __folder so the session continues and no information
                # is lost. It will be just distributed in several videos in case the window changes sizes
                # several times
            # As our video has the property 20fps, we have to sleep our __thread 1/25. It is not 1/20
            # because processing some of these instructions take time so we need this __thread to keep
            # running faster
            time.sleep(1/25)
        # Once the flag __keeprecording is False we stop our recording session, so we close our video writer
        writer.close()
        # And stop the secondary __thread and takes the screenshots
        x.join()
        
    def start_recording_session(self):
        """
        This method starts the recording session. It starts a new __thread that runs the method
        __main_thread_recording_session
        :return: None
        """
        # If __keeprecording is already True is because we already have a recording session running
        if self.__keeprecording:
            # In that case, we have to raise a custom made Exception
            raise SessionStartedException("There is an existing running recording session for this object")
        print("Started our recording session")
        # Otherwise, we don't have a recording session going on, so we change the flag
        # __keeprecording to True
        self.__keeprecording = True
        # We create the main __thread that runs the algorithm and assign it to attribute __thread
        # so we can start and stop it
        self.__thread = threading.Thread(target=self.__main_thread_recording_session, args=())
        # We start that __thread
        self.__thread.start()
        
    def stop_recording_session(self):
        """
        This method stops the recording session. It stops the threads that create the video
        :return: None
        """
        # If the flag __keeprecording is already False is because we don't have a session running
        if not self.__keeprecording:
            # In that case, we raise a custom made Exception
            raise NoSessionStartedException("There is no current recording session")
        # We set the flag keeprecoring to false, to stop the recording process
        self.__keeprecording = False
        # We stop the main __thread
        self.__thread.join()
        # We set the attribute __thread to None, because the __thread is finished and the
        # recording session is done
        self.__thread = None
        try:
            os.remove(self.__sessionPath+"/frame.png")
        except (FileNotFoundError, Exception):
            print("There was an issue when trying to delete the file where we stored our frames")
        print("Our recording session ended")


class SessionStartedException(Exception):
    """ 
    This is a class that inherits from Exception to create a custom made Exception to be raised
    in the case that we try to start a new recording session when there is a current session
    running.
    """
    pass


class NoSessionStartedException(Exception):
    """ 
    This is a class that inherits from Exception to create a custom made Exception to be raised
    in the case that we try to stop a  recording session when we have not started a recording
    session.
    """
    pass
