import time
import unittest
from app_window_objects import instagramloginapp as ins
from app_window_objects.instagramaddpostapp import InstagramAddPostApp
from app_window_objects.instagramconversationapp import InstagramConversationApp
from app_window_objects.instagramdmsapp import InstagramDMsApp
from app_window_objects.instagrammainapp import InstagramMainApp
from app_window_objects.instagramprofileapp import InstagramProfileApp
from appium.webdriver import webelement


class InstagramTestSuite(unittest.TestCase):

    def tearDown(self):
        self.instagram.destroy()
        time.sleep(60)

    def setUp(self) -> None:
        self.instagram = ins.InstagramLoginApp()

    def test_login(self, username: str = None) -> InstagramMainApp:
        if username is None:
            self.username = input("Give us your username: ")
        password = input("Give us your password: ")
        self.instagram.click_on_login()
        self.instagram.set_username(self.username)
        self.instagram.set_password(password)
        time.sleep(5)
        instagram_main: InstagramMainApp = self.instagram.click_on_button_to_login()
        self.assertTrue(instagram_main.is_title_bar_visible(), "We were not logged in")
        time.sleep(5)
        return instagram_main

    def test_dms(self) -> None:
        instagram_main: InstagramMainApp = self.test_login()
        instagram_dm: InstagramDMsApp = instagram_main.click_on_button_dm()
        name = input("Who do you want to send a DM to? ")
        # noinspection PyTypeChecker
        instagram_conversation: InstagramConversationApp = instagram_dm.scroll_bottom_page(
            instagram_dm.wrapper_search_conversation, name)
        message: str = input("What text do you want to send? ")
        instagram_conversation.send_message(message)
        messages = instagram_conversation.get_all_visible_messages()
        print(messages)
        self.assertTrue(messages[len(messages)-1] == message, "Message was not sent")

    def test_profile(self) -> None:
        username = input("Give us your username: ")
        instagram_main: InstagramMainApp = self.test_login(username)
        time.sleep(3)
        instagram_profile: InstagramProfileApp = instagram_main.click_on_button_profile()
        time.sleep(3)
        self.assertTrue(instagram_profile.is_profile_image_visible(), "Profile image is not displayed")
        self.assertTrue(instagram_profile.get_profile_title() == username, "Profile name is not correct")
        self.assertTrue(instagram_profile.get_button_edit_profile() is not None, "Button Edit was not loaded")

    def test_post_image(self) -> None:
        username = input("Give us your username: ")
        instagram_main: InstagramMainApp = self.test_login(username)
        time.sleep(5)
        instagram_post: InstagramAddPostApp = instagram_main.click_on_button_post()
        time.sleep(3)
        instagram_post.allow_permissions()
        instagram_post.click_on_button_next()
        instagram_post.click_on_button_next()
        instagram_post.click_on_button_next()
        instagram_profile = instagram_main.click_on_button_profile()
        instagram_photo_post: webelement = instagram_profile.get_photo_n(0)
        self.assertTrue(instagram_photo_post is not None, "Photo was not uploaded")
        instagram_profile.click_photo_n(0)


if __name__ == '__main__':
    unittest.main()
