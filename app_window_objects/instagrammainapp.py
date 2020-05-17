from abs_class.appwindowobject import AppWindowObject
from app_window_objects.instagramaddpostapp import InstagramAddPostApp
from app_window_objects.instagramdmsapp import InstagramDMsApp
import time

from app_window_objects.instagramprofileapp import InstagramProfileApp


class InstagramMainApp(AppWindowObject):
    """
    This class controls the main window in the Instagram app for Android (the one with the feed)
    """
    def __init__(self, driver):
        """
        This constructor receives a parameter driver which is an instance of webdriver that will be assigned
        to the property driver. So we will reuse the driver from another class and won't create a new one
        :param driver: Instance of webdriver created in the first/main activity in the app for Instagram
        """
        super().__init__(driver=driver)

    # Here we create several variables that will contain the key to the xpaths, ids and other selectors
    # so we can search for them with these parameters
    button_dm = "button_dm"
    instagram_title = "instagram_title"
    lower_bar_buttons = "lower_bar_buttons"

    def click_on_button_dm(self) -> InstagramDMsApp:
        """
        This method clicks on the button to access the DMs in the top bar
        :return: An object of type InstagramDMsApp (the window where we go after clicking that button)
        """
        self.locators.find_element_by_id(self.id[self.button_dm]).click()
        return InstagramDMsApp(self.driver)

    def is_title_bar_visible(self) -> bool:
        """
        This method returns True in the title bar of the app is visible
        :return: True if the title bar of the app is visible or False is not
        """
        return self.locators.find_element_by_id(self.id[self.instagram_title]).is_displayed()

    def get_lower_bar_buttons(self) -> list:
        """
        This method gets the webelement for the buttons in the lower bar of this screen
        :return: List of the webelements for the 5 buttons in the lower bar of the main screen in the Instagram app
        for Android
        """
        # We use a try/except block
        try:
            # We wait 7 seconds
            time.sleep(3)
            # We use the xpath to get all webelements in the lower bar
            buttons: list = self.locators.find_elements_by_xpath(self.xpath[self.lower_bar_buttons])
            # We return the list of those webelements
            return buttons
        except Exception as e:
            # We catch any possible exceptions
            print(e)

    def click_on_button_feed(self) -> None:
        """
        This method clicks on the button to access our feed in the lower bar
        :return: None
        """
        self.get_lower_bar_buttons()[0].click()

    def click_on_button_search(self) -> None:
        """
        This method clicks on the button to search/explore posts
        :return: None
        """
        self.get_lower_bar_buttons()[1].click()

    def click_on_button_post(self) -> InstagramAddPostApp:
        """
        This method clicks on the button to post a pic from our phone
        :return: A InstagramAddPostApp object that is the class that represent the screen to pick a pic a posts it
        """
        self.get_lower_bar_buttons()[2].click()
        return InstagramAddPostApp(self.driver)

    def click_on_button_notifications(self) -> None:
        """
        This method clicks on the button to see the notifications
        :return: None
        """
        self.get_lower_bar_buttons()[3].click()

    def click_on_button_profile(self) -> InstagramProfileApp:
        """
        This method click on the button profile in the lower bar and return an InstagramProfileApp object
        that represents that screen
        :return:
        """
        try:
            # We wait for 5 seconds
            #time.sleep(5)
            # We get that elements and click
            self.get_lower_bar_buttons()[4].click()
            # We return the element that represents the profile section of the app
            return InstagramProfileApp(self.driver)
        except Exception as e:
            print(e)
