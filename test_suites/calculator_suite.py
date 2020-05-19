import time
import unittest
import selenium
from app_window_objects import calculatormainapp as cmp
from videoRecorder.videoRecorder.desktopBrowserRecorder import DesktopBrowserRecorder


class CalculatorTestSuite(unittest.TestCase):

    video_recorder = None

    def tearDown(self):
        if self.video_recorder is not None:
            self.video_recorder.stopRecordingSession()

    def test_add_two_numbers(self):
        n = input("Select first number\n")
        m = input("Select second number\n")
        self.calculator = cmp.CalculatorMainApp()
        self.video_recorder = DesktopBrowserRecorder("..//videos", ".mp4", self.calculator.driver)
        self.video_recorder.startRecordingSession()
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
        n = input("Select first number\n")
        m = input("Select second number\n")
        self.calculator = cmp.CalculatorMainApp()
        self.video_recorder = DesktopBrowserRecorder("..//videos", ".mp4", self.calculator.driver)
        self.video_recorder.startRecordingSession()
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
        n = input("Select first number\n")
        m = input("Select second number\n")
        self.calculator = cmp.CalculatorMainApp()
        self.video_recorder = DesktopBrowserRecorder("..//videos", ".mp4", self.calculator.driver)
        self.video_recorder.startRecordingSession()
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
        n = input("Select first number\n")
        m = input("Select second number\n")
        self.calculator = cmp.CalculatorMainApp()
        self.video_recorder = DesktopBrowserRecorder("..//videos", ".mp4", self.calculator.driver)
        self.video_recorder.startRecordingSession()
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
        self.calculator = cmp.CalculatorMainApp()
        self.video_recorder = DesktopBrowserRecorder("..//videos", ".mp4", self.calculator.driver)
        self.video_recorder.startRecordingSession()
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
