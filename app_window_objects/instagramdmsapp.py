import selenium
from appium.webdriver import webelement
from abs_class.appwindowobject import AppWindowObject
from app_window_objects.instagramconversationapp import InstagramConversationApp
from typing import Callable, Optional


class InstagramDMsApp(AppWindowObject):
    """
    This class controls the window/activity of the list of DM conversations in the app for Instagram in Android
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
    name_conversation: str = "name_conversation"

    def get_n_conversation_name(self, n: int) -> str:
        """
        This method gets the name of the person of the conversation in position "n"
        :param n: Place of the conversation, 0 is the top conversation
        :return: String with the name of the person we had the conversation with at the position n
        """
        # We get the xpath for each name of the conversations, it is a regular expresion where {n} is the position
        # of the conversation, we replace it with the position of the conversation
        xpath: str = self.xpath[self.name_conversation].replace("{n}", str(n+3))
        # We get the text of the message
        result: str = self.locators.find_element_by_xpath(xpath).text
        # We return the text of that message
        return result

    def get_conversation_n(self, n: int) -> webelement:
        """
        We get the webelement corresponding to the conversation in position "n" (0 is the conversation at the top)
        :param n: Position of the conversation
        :return: Webelement of the conversation
        """
        # We get the xpath for each name of the conversations, it is a regular expresion where {n} is the position
        # of the conversation, we replace it with the position of the conversation
        xpath: str = self.xpath[self.name_conversation].replace("{n}", str(n + 3))
        # We return that webelement
        return self.locators.find_element_by_xpath(xpath)

    def click_on_conversation_n(self, n: int) -> None:
        """
        This method gets the webelement in the position "n" and clicks on it to open it
        :param n: Position of the conversation we want to click in (0 is the conversation at the top)
        :return: None
        """
        return self.get_conversation_n(n).click()

    def scroll_bottom_page(self, func: Callable, *args) -> object:
        """
        This method keeps getting every conversation and scrolls until the method in variable func returns something
        different than None (using the variables in *args)
        :param func: Method that will be called and assigned to the variable that will break this algorithm
        :param args: Parameters that will be used in the previous method
        :return: And object that will be the result of the method in func
        """
        # First we create a variasble go_on that will be the flag to keep going through our conversations and scrolling
        # or to stop once it is not None
        go_on = None
        # These two variables will allow us to see if we got to the bottom of the list, if both are equal is because
        # we got the same conversation twice
        v_name1: str = "Name1"
        v_name2: str = ""
        # So while those two variables are not equals, we will keep looking and scrolling
        while v_name1 != v_name2:
            # Now, v_name2 is the new v_name1 (we update the variable)
            v_name1 = v_name2
            print(self.driver.get_window_size())
            # We use a try/except block
            try:
                # The variable go_on will be equals to the result of the function func with variables args
                go_on = func(args)
                # If go_on is not None, it means we have fulfilled the goal of this algorithm so we stop the loop
                # and return the variable go_on which is the result of the method
                if go_on is not None:
                    # We return go_on
                    return go_on
                # We get the coordinates of the conversation at the top
                coordinates_1: dict = self.get_conversation_n(0).location
                # We get the coordinates of the fourth conversation
                coordinates_2: dict = self.get_conversation_n(3).location
                # Now, v_name2 will contain the name of the conversation in the fourth place
                v_name2 = self.get_n_conversation_name(3)
                # We scroll now 4 positions
                self.driver.swipe(0, coordinates_2["y"], 0, coordinates_1["y"])
            except Exception as e:
                # We catch any exception that is thronw
                print(e)
                go_on = None
        # We return the result of the function func, go_on
        return go_on

    def click_on_conversation_with_name(self, name: str) -> Optional[InstagramConversationApp]:
        """
        This method return the page/activity/window object of the conversation with name in the variable name.
        We click in that conversation and return an object of type InstagramConversationApp
        :param name: Name of the account we had the conversation with we want to get
        :return: An object of type InstagramConversationApp
        """
        print("name: {0}".format(name))
        # We check every visible conversation (we usually see 8 conversations)
        for i in range(0, 7):
            # We use a try/except block
            try:
                # We get the name of the person we are having a conversation with in the conversation in the position
                # i
                v_name: str = self.get_n_conversation_name(i)
                v_name = v_name.replace("\n", "")
                print("Checking conversation: {0}".format(v_name))
                # If it is the same as the name we passed as parameter
                if v_name == name:
                    print("Found our conversation")
                    # We click in that conversation
                    self.click_on_conversation_n(i)
                    # We return an object of type InstagramConversationApp, instantiated using our current property
                    # driver
                    return InstagramConversationApp(self.driver)
            # If we can't find one of these 8 conversations, we return None
            except TimeoutError:
                return None
            except selenium.common.exceptions.NoSuchElementException:
                return None
        # If we went through all of those 8 conversations and did not find the one we were searching for, we return
        # None
        return None

    def search_conversation_by_name(self, name: str) -> bool:
        """
        This method searches for a conversation with user with name in the parameter "name" and return True if
        we find it
        :param name: Name of the account of the conversation we are searching
        :return: True if we don't find it, False if do
        """
        # We create the flag, not_found to True
        not_found: bool = True
        # We go through every visible conversation in our screen
        for i in range(0, 7):
            # We get the name in the conversation in the position i
            v_name: str = self.get_n_conversation_name(i)
            # If we got one and is the same as the one we are looking for
            if v_name is not None and name == v_name:
                # We click on that conversation
                self.click_on_conversation_n(i)
                # We set our flag to False
                not_found = False
                # We break this loop
                break
        # We return the value of our flag
        return not_found

    def wrapper_search_conversation(self, *args) -> InstagramConversationApp:
        """
        This method is a wrapper of our previous method to be used in the method scroll_bottom_page as the parameter
        func
        :param args: Parameters that we will pass to our function
        :return: The result of the method click_on_conversation_with_name
        """
        name: str = args[0][0]
        res: InstagramConversationApp = self.click_on_conversation_with_name(name)
        return res
