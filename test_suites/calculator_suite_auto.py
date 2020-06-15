import time
import unittest
import selenium
from app_window_objects import calculatormainapp as cmp

"""
To get to know how to use this project: https://github.com/AntoData/appium-framework/wiki
"""


class CalculatorTestSuite(unittest.TestCase):

    def tearDown(self):
        self.calculator.destroy()
        time.sleep(60)

    def setUp(self) -> None:
        self.calculator = cmp.CalculatorMainApp()

    def test_add_two_numbers(self):
        n: str = str(8)
        m: str = str(3)
        try:
            self.calculator.click_on_arrow()
        except selenium.common.exceptions.NoSuchElementException:
            pass
        self.calculator.click_on_number(n)
        self.calculator.click_on_add()
        self.calculator.click_on_number(m)
        self.calculator.click_on_equal()
        time.sleep(5)
        result = self.calculator.get_operation_int_result()
        print("{0}+{1}={2}".format(n, m, result))
        self.assertEqual((int(n) + int(m)), result)

    def test_subtract_two_numbers(self):
        n: str = str(8)
        m: str = str(3)
        try:
            self.calculator.click_on_arrow()
        except selenium.common.exceptions.NoSuchElementException:
            pass
        self.calculator.click_on_number(n)
        self.calculator.click_on_minus()
        self.calculator.click_on_number(m)
        self.calculator.click_on_equal()
        time.sleep(5)
        result = self.calculator.get_operation_int_result()
        print("{0}-{1}={2}".format(n, m, result))
        self.assertEqual((int(n) - int(m)), result)

    def test_multiply_two_numbers(self):
        n: str = str(8)
        m: str = str(5)
        try:
            self.calculator.click_on_arrow()
        except selenium.common.exceptions.NoSuchElementException:
            pass
        self.calculator.click_on_number(n)
        self.calculator.click_on_multiply()
        self.calculator.click_on_number(m)
        self.calculator.click_on_equal()
        time.sleep(5)
        result = self.calculator.get_operation_int_result()
        print("{0}*{1}={2}".format(n, m, result))
        self.assertEqual((int(n) * int(m)), result)

    def test_divide_two_numbers(self):
        n: str = str(9)
        m: str = str(3)
        try:
            self.calculator.click_on_arrow()
        except selenium.common.exceptions.NoSuchElementException:
            pass
        self.calculator.click_on_number(n)
        self.calculator.click_on_divide()
        self.calculator.click_on_number(m)
        self.calculator.click_on_equal()
        time.sleep(5)
        result = self.calculator.get_operation_float_result()
        print("{0}-{1}={2}".format(n, m, result))
        self.assertEqual(int(n) / (int(m)), result)

    def test_delete_number(self):
        try:
            self.calculator.click_on_arrow()
        except selenium.common.exceptions.NoSuchElementException:
            pass
        self.calculator.click_on_number("9")
        self.calculator.click_on_delete()
        time.sleep(5)
        result = self.calculator.get_preview_result()
        self.assertEqual("", result)


if __name__ == '__main__':
    unittest.main()
