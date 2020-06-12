import selenium
from abs_class.appwindowobject import AppWindowObject


class CalculatorMainApp(AppWindowObject):
    """
    This class control the main and only window of the calculator app that comes with Android phones by default
    """
    def __init__(self):
        """
        As this is the first/main activity of the app, we don't pass a webdriver parameter so it has to search
        for the json file with the same name as this class in lower case in folder profiles to create the property
        driver that will perform this test
        """
        super().__init__()

    # Here we create several variables that will contain the key to the xpaths, ids and other selectors
    # so we can search for them with these parameters
    button_arrow: str = "arrow"
    number_button: str = "number"
    button_add: str = "add"
    button_minus: str = "minus"
    button_equal: str = "equal"
    button_result: str = "result"
    button_multiply: str = "multiply"
    button_division: str = "division"
    button_delete: str = "delete"
    result_preview: str = "result_preview"
    result: str = "result"

    def click_on_arrow(self) -> None:
        """
        This method clicks in the arrow to display the numbers and basic operations screen
        :return: None
        """
        self.locators.find_element_by_id(self.id["arrow"]).click()

    def click_on_number(self, number: str) -> None:
        """
        This method clicks in the button with the number in parameter number
        :param number: Parameter that defines the number of the button we will press
        :return: None
        """
        # We will get the id we saved that is a regular expression where {n} represents the number, we replace
        # that for the number in parameter number
        id_number: str = self.id[self.number_button].replace("{n}", number)
        self.locators.find_element_by_id(id_number).click()
        self.locators.take_screenshot()

    def click_on_add(self) -> None:
        """
        This method clicks in the button + (the addition)
        :return: None
        """
        self.locators.find_element_by_id(self.id[self.button_add]).click()

    def click_on_minus(self) -> None:
        """
        This method clicks in the button - (the subtraction)
        :return: None
        """
        self.locators.find_element_by_id(self.id[self.button_minus]).click()

    def click_on_equal(self) -> None:
        """
        This method clicks in the button = (equals)
        :return: None
        """
        self.locators.find_element_by_id(self.id[self.button_equal]).click()

    def get_operation_int_result(self) -> int:
        """
        This method gets the result of the operation and parses it to int
        :return: None
        """
        try:
            result = int(self.locators.find_element_by_id(self.id[self.result]).text)
        except selenium.common.exceptions.NoSuchElementException:
            result = int(self.locators.find_element_by_id(self.id[self.result_preview]).text)
        return result

    def get_operation_float_result(self) -> float:
        """
        This method gets the result of the operation and parses it to float
        :return: None
        """
        try:
            result = float(self.locators.find_element_by_id(self.id[self.result]).text.replace(",", "."))
        except selenium.common.exceptions.NoSuchElementException:
            result = float(self.locators.find_element_by_id(self.id[self.result_preview]).text.replace(",", "."))
        return result

    def click_on_multiply(self) -> None:
        """
        This method clicks in the button x (multiplication)
        :return: None
        """
        self.locators.find_element_by_id(self.id[self.button_multiply]).click()

    def click_on_divide(self) -> None:
        """
        This method clicks in the button / (division)
        :return: None
        """
        self.locators.find_element_by_xpath(self.xpath[self.button_division]).click()

    def click_on_delete(self) -> None:
        """
        This method clicks in the button to delete a number from the screen
        :return: None
        """
        self.locators.find_element_by_xpath(self.xpath[self.button_delete]).click()

    def get_preview_result(self) -> str:
        """
        This method gets the preview result in string format
        :return: None
        """
        try:
            result = self.locators.find_element_by_id(self.id[self.result_preview]).text
        except selenium.common.exceptions.NoSuchElementException:
            result = self.locators.find_element_by_id(self.id[self.result]).text
        return result
