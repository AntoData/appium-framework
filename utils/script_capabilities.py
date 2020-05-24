from utils.capabilities_utils import to_file_capabilities

"""
This is a script that automates the process of getting the right capabilities to instantiate our webdriver instance
to perform our tests. We should have our app running and the screen unlocked and then provide a name for the file. In
order for this to work completely with our framework the name of the file should be the same name as the main activity
page object class (classes in folder app_window_objects) in lower case.
"""


def main():
    print("Unlock the phone")
    print("Open the app you want to automate")
    profile = input("Please provide a name for this profile to be saved:\n")
    to_file_capabilities(profile)
    print("By default the property 'automationName' will be set to 'UiAutomator1'")
    print("If you see in Appium logs that the test does not run the app, try changing to 'UiAutomator2'")


if __name__ == '__main__':
    main()
