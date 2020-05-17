from abs_class.appwindowobject import AppWindowObject
from app_window_objects.instagrammainapp import InstagramMainApp


class InstagramLoginApp(AppWindowObject):
    """
    This class controls the first activity in the Instagram app for Android
    """
    def __init__(self):
        # We don't use a pre-existing webdriver parameters as this is the first activity when we run our tests,
        # so we have to create it from scratch using the json file in the folder properties
        super().__init__()

    # Here we create several variables that will contain the key to the xpaths, ids and other selectors
    # so we can search for them with these parameters
    button_login = "button_login"
    field_username = "field_username"
    field_password = "field_password"
    button_to_login = "button_to_login"

    def click_on_login(self) -> None:
        """
        This method clicks in the button Login
        :return: None
        """
        self.locators.find_element_by_id(self.id[self.button_login]).click()

    def set_username(self, username: str) -> None:
        """
        This method writes the string in "username" in the field for the username in the login page
        :param username: String with the username we want to send to that input
        :return: None
        """
        self.locators.find_element_by_id(self.id[self.field_username]).send_keys(username)

    def set_password(self, password: str) -> None:
        """
        This method sends the string in the variable password to the field in password
        :param password: String variable with the password
        :return: None
        """
        self.locators.find_element_by_id(self.id[self.field_password]).send_keys(password)

    def click_on_button_to_login(self) -> InstagramMainApp:
        """
        This method clicks in the button to finally login after setting the username and password
        :return: None
        """
        self.locators.find_element_by_id(self.id[self.button_to_login]).click()
        return InstagramMainApp(self.driver)
