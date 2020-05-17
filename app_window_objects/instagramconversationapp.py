import selenium
from selenium.common.exceptions import TimeoutException
from abs_class.appwindowobject import AppWindowObject


class InstagramConversationApp(AppWindowObject):
    """
    This class control the activity/window for a DM conversation in the instagram app for Android
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
    text_area: str = "text_area"
    button_send: str = "button_send"
    message_selector: str = "message"

    def write_message(self, text: str) -> None:
        """
        This method gets the input where to write the message in a DM conversation and writes the text in variable
        text
        :param text: Text of the message we will send
        :return: None
        """
        self.locators.find_element_by_id(self.id[self.text_area]).send_keys(text)

    def click_send(self) -> None:
        """
        This method click in the button Send to send the message in the conversation
        :return:
        """
        self.locators.find_element_by_id(self.id[self.button_send]).click()

    def send_message(self, text: str) -> None:
        """
        This method sends the message in the variable text in a DM Instagram conversation (uses the two previous
        methods)
        :param text: String of the message we want to send
        :return: None
        """
        self.write_message(text)
        self.click_send()

    def get_message(self, n: int) -> str:
        """
        This method gets the message in the position n (usually we only see 8 messages and the top one is 1)
        :param n: Position of the message we want to get the text from
        :return: A string variable with the text of the message
        """
        # We get the xpath that gets the message, which is a regular expression that uses {n} to get the message
        # in position n, so we replace that with the number of the position of the message we want to get
        xpath: str = self.xpath[self.message_selector].replace("{n}", str(n))
        # Now we use that xpath to find the element and get its text
        text: str = self.locators.find_element_by_xpath(xpath).text
        # We return the text of the message
        return text

    def get_all_visible_messages(self) -> list:
        """
        This method gets all visible messages and gets its text as string and adds it to a list
        :return:
        """
        # We create an empty dictionary
        messages: list = []
        # We get a pointer i, pointing to i (first message)
        i: int = 1
        # We run an infinite loop that will only be broken once we don't find the message in position "i"
        while True:
            # In order to do so, we use a try/except block
            try:
                # We get the message in position i
                message: str = self.get_message(i)
                # We add the message to the list
                messages.append(message)
                # We increase the pointer
                i += 1
            except TimeoutException:
                # If we can't find the element, we will get a timeout exception and break the loop
                break
            except selenium.common.exceptions.NoSuchElementException:
                # Same here, if we can't find the element we will get a NoSuchElementException and break the loop
                break
        # We return the list of messages visible
        return messages
