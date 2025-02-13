import unittest
from Configuration.drivers_setup import *
from Configuration.base_test import BaseTest
from PageObjects.openai import OpenAIApi
from PageObjects.banter_bubble_page_objects import BanterBubbleAPI
from PageObjects.twitter_page_objects import TwitterPageObjects
from PageObjects.twitter_api import TwitterAPI


class CreateTweetsFromNewsFeed(BaseTest):
    new_twitter_links = []
    new_twitter_posts_texts = []
    new_plain_texts = []
    chat_gpt_texts = []
    skip_twitter_tests = False
    skip_plain_texts_tests = False

    def test_01_get_last_news(self):
        bb_api = BanterBubbleAPI(self.driver)
        bb_api.save_via_api_all_news_posted_less_than_specific_seconds_ago(12020)
        bb_api.differentiate_news_and_twitter_links()
        self.__class__.new_twitter_links = bb_api.get_all_new_links()
        self.__class__.new_plain_texts = bb_api.get_all_new_plain_texts()

    def test_02_open_twitter_and_save_all_post_texts(self):
        if not self.__class__.skip_twitter_tests:
            twitter_page = TwitterPageObjects(self.driver)
            for url in self.__class__.new_twitter_links:
                self.driver.get(url)
                self.__class__.new_twitter_posts_texts.append(twitter_page.get_post_text())
                # the URL to be saved to some database, so we do not get it again on any next code run

    def test_03_get_texts_from_chat_gpt_according_to_twitter_posts(self):
        if not self.__class__.skip_twitter_tests:
            chat_gpt = OpenAIApi()
            for post_text in self.__class__.new_twitter_posts_texts:
                self.__class__.chat_gpt_texts.append(chat_gpt.generate_and_return_text_for_specific_number_of_chars(post_text))

    def test_04_get_texts_from_chat_gpt_according_to_plain_texts(self):
        if not self.__class__.skip_plain_texts_tests:
            chat_gpt = OpenAIApi()
            for post_text in self.__class__.new_plain_texts:
                self.__class__.chat_gpt_texts.append(chat_gpt.generate_and_return_text_for_specific_number_of_chars(post_text))

    def test_05_post_tweet(self):
        for text in self.__class__.chat_gpt_texts:
            try:
                x_api = TwitterAPI()
                url = x_api.get_authorization_url()
                self.driver.get(url)
                x = TwitterPageObjects(self.driver)
                x.login_for_verifier_code()
                # try:
                #     x.login()
                # except:
                #     pass
                verifier = x.get_twitter_code()
                x_api.set_verifier(verifier)
                x_api.create_tweet(text)
            except:
                print(f'-------- \n Chat GPT Text is: {text} \n')
                handle_exception(self.driver, screenshot_name='cannot_post_tweet.png')
