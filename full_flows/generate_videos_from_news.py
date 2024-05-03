from Configuration.base_test import BaseTest
from Configuration.drivers_setup import *
from PageObjects.elai import ElaiAPI
from PageObjects.openai import OpenAIApi
from PageObjects.banter_bubble_page_objects import BanterBubblesHomePage
from PageObjects.twitter_page_objects import TwitterPageObjects


class GenerateVideo(BaseTest):
    new_twitter_links = []
    new_twitter_posts_texts = []
    new_plain_texts = []
    chat_gpt_texts = []
    all_video_urls = []
    skip_twitter_tests = False
    skip_plain_texts_tests = False

    def test_01_get_last_news(self):
        bb_homepage = BanterBubblesHomePage(self.driver)
        bb_homepage.open_homepage()
        bb_homepage.open_news_room()
        bb_homepage.save_via_browser_all_news_posted_less_than_specific_seconds_ago(seconds=660)
        bb_homepage.differentiate_news_and_twitter_links()
        self.__class__.new_twitter_links = bb_homepage.get_all_new_links()
        self.__class__.new_plain_texts = bb_homepage.get_all_new_plain_texts()
        if len(self.__class__.new_twitter_links) == 0:
            print('NO NEW TWITTER LINKS IN THIS ITERATION!')
            self.__class__.skip_twitter_test = True
        if len(self.__class__.new_plain_texts) == 0:
            print('NO NEW PLAIN TEXT NEWS IN THIS ITERATION!')
            self.__class__.skip_plain_texts_tests = True

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
                self.__class__.chat_gpt_texts.append(chat_gpt.generate_and_return_text_for_specific_number_of_words(post_text))

    def test_04_get_texts_from_chat_gpt_according_to_plain_texts(self):
        if not self.__class__.skip_plain_texts_tests:
            chat_gpt = OpenAIApi()
            for post_text in self.__class__.new_plain_texts:
                self.__class__.chat_gpt_texts.append(chat_gpt.generate_and_return_text_for_specific_number_of_words(post_text))

    def test_05_generate_videos(self):
        elai_api = ElaiAPI()
        for text in self.__class__.chat_gpt_texts:
            print(f'CHAT GPT Text is: {text}')
            elai_api.generate_video_from_text(text)
            elai_api.render_video()
            video_url = elai_api.get_url_for_rendered_video()
            self.__class__.all_video_urls.append(video_url)

    def test_06_print_all_video_urls(self):
        for url in self.__class__.all_video_urls:
            print(f'Elai Video URL is: {url}')
