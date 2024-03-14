import requests
import unittest
from Configuration.drivers_setup import *
from PageObjects.openai import OpenAIApi
from PageObjects.web_page_objects import BanterBubblesHomePage, TwitterPageObjects


class GenerateVideo(unittest.TestCase):
    driver = None
    new_twitter_links = []
    new_twitter_posts_texts = []
    new_plain_texts = []
    chat_gpt_texts = []
    skip_twitter_test = False

    @classmethod
    def setUpClass(cls):
        cls.driver = driver_init()
        cls.driver.maximize_window()

    def test_01_get_last_news(self):
        bb_homepage = BanterBubblesHomePage(self.driver)
        bb_homepage.open_homepage()
        bb_homepage.open_news_room()
        bb_homepage.check_and_save_news_posted_less_than_specific_seconds_ago(seconds=300)
        bb_homepage.check_new_posts_for_twitter_links()
        self.__class__.new_twitter_links = bb_homepage.get_all_new_links()
        self.__class__.new_plain_texts = bb_homepage.get_all_new_plain_texts()
        if len(self.__class__.new_twitter_links) == 0:
            print('NO NEW NEWS IN THIS ITERATION!')
            self.__class__.skip_twitter_test = True

    def test_02_open_twitter_and_save_all_post_texts(self):
        if not self.__class__.skip_twitter_test:
            twitter_page = TwitterPageObjects(self.driver)
            for url in self.__class__.new_twitter_links:
                self.driver.get(url)
                self.__class__.new_twitter_posts_texts.append(twitter_page.get_post_text())
                # the URL to be saved to some database, so we do not get it again on any next code run

    def test_03_get_texts_from_chat_gpt_according_to_twitter_posts(self):
        chat_gpt = OpenAIApi()
        for post_text in self.__class__.new_twitter_posts_texts:
            self.__class__.chat_gpt_texts.append(chat_gpt.generate_and_return_text(post_text))
        for text in self.__class__.chat_gpt_texts:
            print(text)

    def test_04_generate_video(self):
        pass
