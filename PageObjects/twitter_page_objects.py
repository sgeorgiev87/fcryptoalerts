import os

from Configuration.base_page import BasePage
from PageObjects.selectors import TwitterSelectors
from Configuration.constants import Credentials


class TwitterPageObjects(BasePage):
    def __init__(self, driver, timeout=5):
        BasePage.__init__(self, driver=driver, timeout=timeout)
        self.username = os.environ['TWITTER_USERNAME']
        self.password = os.environ['TWITTER_PASSWORD']

    def open_url_and_click_login(self):
        self.driver.get('https://twitter.com')
        self.visibility_of_element(TwitterSelectors.LOGIN_BUTTON).click()

    def login(self):
        self.visibility_of_element(TwitterSelectors.USERNAME_INPUT).send_keys(Credentials.TWITTER_USERNAME)
        self.visibility_of_element(TwitterSelectors.NEXT_BUTTON).click()
        self.visibility_of_element(TwitterSelectors.PASSWORD_INPUT).send_keys(Credentials.TWITTER_PASSWORD)
        self.visibility_of_element(TwitterSelectors.LOGIN_CONFIRM_BUTTON).click()

    def post_tweet(self, text):
        self.visibility_of_element(TwitterSelectors.INPUT_TWEET_TEXT).send_keys(text)
        self.visibility_of_element(TwitterSelectors.POST_TWEET_BUTTON).click()

    def get_post_text(self):
        return self.visibility_of_element(TwitterSelectors.FIRST_TWEET_TEXT).text.replace('\n', ' ')

    def get_twitter_code(self):
        self.click_authorize_app_button()
        return self.visibility_of_element(TwitterSelectors.TWITTER_CODE).text

    def login_for_verifier_code(self):
        self.click_authorize_app_button()
        try:
            self.login()
        except:
            try:
                self.visibility_of_element(TwitterSelectors.TWITTER_API_USERNAME).send_keys(self.username)
                self.visibility_of_element(TwitterSelectors.TWITTER_API_PASSWORD).send_keys(self.password)
            except:
                pass
        try:
            self.click_authorize_app_button()
        except:
            pass

    def click_authorize_app_button(self):
        try:
            self.visibility_of_element(TwitterSelectors.AUTHORIZE_APP_BUTTON).click()
        except:
            pass
