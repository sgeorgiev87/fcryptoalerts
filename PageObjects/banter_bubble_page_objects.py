import datetime
import os

import requests
from PageObjects.selectors import *
from Configuration.base_page import *


class BanterBubbleAPI(BasePage):
    def __init__(self, driver, timeout=10):
        BasePage.__init__(self, driver=driver, timeout=timeout)
        self.new_news = []
        self.all_twitter_links = []
        self.plain_texts = []
        self.news_api_url = os.environ['BANTER_BUBBLES_NEWS_API_URL']
        self.web_url = os.environ['BANTER_BUBBLES_WEB_URL']

    def save_via_api_all_news_posted_less_than_specific_seconds_ago(self, seconds: int = 120):
        all_news = requests.get(self.news_api_url).json()
        for news in all_news:
            post_date_str = news['created_at']
            post_date_time = datetime.datetime.strptime(post_date_str, "%Y-%m-%dT%H:%M:%S.%fZ")
            curr_date_time = datetime.datetime.utcnow()
            duration_in_s = (curr_date_time - post_date_time).total_seconds()
            if duration_in_s < seconds:
                self.new_news.append(news['text'])
            else:
                break

    def differentiate_news_and_twitter_links(self):
        for news in self.new_news:
            if 'https://x.com' in news or 'https://twitter.com' in news:
                # separate by space the whole news string in different strings
                # so we can easily get the Twitter link
                all_strings = news.replace('\n', ' ').split(sep=" ")
                for string in all_strings:
                    if 'https://x.com' in string or 'https://twitter.com' in string:
                        self.all_twitter_links.append(string)
                        break
            else:
                plain_text = news.replace('\n', ' ')
                # this is to avoid generating text and videos for some twitter replies - i.e. "Wow. What a story"
                if len(plain_text) > 60:
                    self.plain_texts.append(plain_text)

    def get_all_new_links(self):
        return self.all_twitter_links

    def get_all_new_plain_texts(self):
        return self.plain_texts


class BanterBubblesHomePage(BanterBubbleAPI):
    def __init__(self, driver, timeout=10):
        BanterBubbleAPI.__init__(self, driver=driver, timeout=timeout)

    def open_homepage(self):
        try:
            self.driver.set_page_load_timeout(5)
            self.driver.get('https://banterbubbles.com/')
        except:
            print('time out')
            # self.driver.send_keys(Keys.CONTROL + 'Escape')
            self.driver.execute_script("window.stop();")

    def open_news_room(self):
        self.visibility_of_element(HomePageSelectors.NEWS_ROOM_BUTTON).click()

    def get_all_news_from_feed(self):
        return self.visibility_of_elements(HomePageSelectors.NEWS_ELEMENT)

    def save_via_browser_all_news_posted_less_than_specific_seconds_ago(self, seconds: int = 60):
        all_news = self.get_all_news_from_feed()
        for news in all_news:
            posted_time = news.find_element(*HomePageSelectors.TIME_SINCE_POSTING).text
            if 'hours' in posted_time:
                hours_since_post = int(posted_time.split(" ", 1)[0])
                seconds_since_post = hours_since_post * 60 * 60
                if seconds_since_post < seconds:
                    self.new_news.append(news)
            elif 'minutes' in posted_time:
                minutes_since_post = int(posted_time.split(" ", 1)[0])
                seconds_since_post = minutes_since_post * 60
                if seconds_since_post < seconds:
                    self.new_news.append(news)
