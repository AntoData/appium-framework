from appium.webdriver import webelement

from abs_class.appwindowobject import AppWindowObject


class InstagramProfileApp(AppWindowObject):
    """
    This method control the activity that displays the profile view in the app for Instagram in Android
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
    profile_title: str = "profile_title"
    profile_image: str = "profile_image"
    button_edit: str = "button_edit"
    photo_posts: str = "photo_posts"

    def get_profile_title(self) -> str:
        """
        This method gets the name of the profile (that is displayed in the title bar) and returns it
        :return: String with the name of the profile
        """
        return self.locators.find_element_by_id(self.id[self.profile_title]).text

    def is_profile_image_visible(self) -> str:
        """
        This method checks if the profile pic in the profile section is visible
        :return: True if it is visible and False otherwise
        """
        return self.locators.find_element_by_id(self.id[self.profile_image]) is not None

    def get_button_edit_profile(self) -> webelement:
        """
        This method gets the webelement for the button Edit
        :return: Webelement which represents the button Edit
        """
        return self.locators.find_element_by_xpath(self.xpath[self.button_edit])

    def click_button_edit(self) -> None:
        """
        This method click on the button Edit
        :return: None
        """
        self.get_button_edit_profile().click()

    def get_photo_n(self, n) -> webelement:
        """
        This method gets the post in the position n and returns the webelement that represents it
        :param n: Position of the photo we want to get
        :return: Webelement that represents that pic
        """
        return self.locators.find_elements_by_xpath(self.xpath[self.photo_posts])[n]

    def click_photo_n(self, n) -> None:
        """
        This method clicks on the pic in the position n
        :param n: Position of the pic where we want to click
        :return: None
        """
        photo: webelement = self.get_photo_n(n)
        photo.click()
