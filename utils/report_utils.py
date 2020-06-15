from datetime import datetime

"""
To get to know how to use this project: https://github.com/AntoData/appium-framework/wiki
"""


class ReportUtils:
    """
    This class provides features to create, write and close a text file for every execution of interactive_test_runner.
    We create a report for every execution of interactive_test_runner, no matter how many test suites in every
    execution we will generate just one report file with the information for each test suite
    """

    def __init__(self):
        """
        This is the constructor of the class, it creates the file and the object file
        """
        # We get the current time
        now = datetime.now()
        # We build the file name using the current instant
        self.file_name = "report_" + now.strftime("%d-%m-%Y_%H-%M-%S")
        try:
            # We create the file inside a try/except block
            self.file = open(".\\test_reports\\"+self.file_name+".txt", "+w")
        except (FileNotFoundError, Exception) as e:
            # If we get an exception, we display this message
            print("We got the following exception when trying to create the report file: {0}".format(e))

    def write_line_in_file(self, line):
        """
        This method writes in the object attribute file the line passed as parameter
        :param line: String that contains the line to write
        :return: None
        """
        try:
            # We use the object attribute file and write the line in parameter line in a try/except block
            self.file.write(line)
        except (FileNotFoundError, Exception) as e:
            # We display this message if we get any exception
            print("We got the following exception when trying to write a line in the report file: {0}".format(e))

    def close_file(self):
        """
        This method closes the file in attribute file
        :return: None
        """
        try:
            # We close the file in object attribute file inside a try/except block
            self.file.close()
        except (FileNotFoundError, Exception) as e:
            # In case we get any exception, we display this message
            print("We got the following exception when trying to close the report file: {0}".format(e))

    @staticmethod
    def get_tests_from_suite(suite) -> str:
        """
        This static method (which means we can use it without creating a new object, just using the classname)
        handles how to get the tests inside a test suite object
        :param suite: Object with the test suite whose test cases we want to get
        :return: A string object with the names of the test cases in the test suite
        """
        # We create the parameter that will contain the name of the test cases
        tests: str = ""
        # We go through all test cases in the object test suite
        for test in suite._tests[0]._tests[0]._tests:
            # We add each test to the parameter tests
            tests += str(test) + "\n"
        # We return the parameter tests which will contain all the test cases in test suite
        return tests
