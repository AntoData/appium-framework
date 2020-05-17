from appium.webdriver import webdriver
from abs_class.appwindowobject import AppWindowObject


class InstagramAddPostApp(AppWindowObject):
    """
    This classes controls the window that after clicking in the lower bar to post an image from your phone
    """
    def __init__(self, driver: webdriver):
        """
        This constructor receives a parameter driver which is an instance of webdriver that will be assigned
        to the property driver. So we will reuse the driver from another class and won't create a new one
        :param driver: Instance of webdriver created in the first/main activity in the app for Instagram
        """
        super().__init__(driver=driver)

    # Here we create several variables that will contain the key to the xpaths, ids and other selectors
    # so we can search for them with these parameters
    button_allow: str = "button_allow"
    button_next: str = "button_next"

    def allow_permissions(self) -> None:
        self.locators.find_element_by_id(self.id[self.button_allow]).click()

    def click_on_button_next(self) -> None:
        self.locators.find_element_by_id(self.id[self.button_next]).click()
