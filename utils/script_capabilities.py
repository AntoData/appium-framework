from utils.capabilities_utils import to_file_capabilities

"""
To get to know how to use this project: https://github.com/AntoData/appium-framework/wiki
This is a script that automates the process of getting the right capabilities to instantiate our webdriver instance
to perform our tests. We should have our app running and the screen unlocked and then provide a name for the file. In
order for this to work completely with our framework the name of the file should be the same name as the main activity
page object class (classes in folder app_window_objects) in lower case.
"""


def main():
    try:
        print("Unlock the phone")
        print("Open the app you want to automate")
        profile = input("Please provide a name for this profile to be saved:\n")
        to_file_capabilities(profile)
        print("By default the property 'automationName' will be set to 'UiAutomator1'")
        print("If you see in Appium logs that the test does not run the app, try changing to 'UiAutomator2'")
    except (FileNotFoundError, Exception):
        print("An error was caught, maybe your app needs other commands to get the activity and package, try with:")
        print("adb shell \"dumpsys window windows | grep -E \'Window\'\"")
        print("adb shell \"dumpsys package | grep <your app>\"")


if __name__ == '__main__':
    main()
