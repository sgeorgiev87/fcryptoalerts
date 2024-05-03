from Configuration.base_page import BasePage
from PageObjects.selectors import TwitterSelectors
from Configuration.constants import Credentials


class TwitterPageObjects(BasePage):
    def __init__(self, driver, timeout=10):
        BasePage.__init__(self, driver=driver, timeout=timeout)

    def login(self):
        self.driver.get('https://twitter.com')
        self.visibility_of_element(TwitterSelectors.LOGIN_BUTTON).click()
        self.visibility_of_element(TwitterSelectors.USERNAME_INPUT).send_keys(Credentials.TWITTER_USERNAME)
        self.visibility_of_element(TwitterSelectors.NEXT_BUTTON).click()
        self.visibility_of_element(TwitterSelectors.PASSWORD_INPUT).send_keys(Credentials.TWITTER_PASSWORD)
        self.visibility_of_element(TwitterSelectors.LOGIN_CONFIRM_BUTTON).click()

    def post_tweet(self):
        self.visibility_of_element(TwitterSelectors.INPUT_TWEET_TEXT).send_keys('FIRST TWEET!')
        self.visibility_of_element(TwitterSelectors.POST_TWEET_BUTTON).click()

    def get_post_text(self):
        return self.visibility_of_element(TwitterSelectors.FIRST_TWEET_TEXT).text.replace('\n', ' ')

    def get_twitter_code(self):
        return self.visibility_of_element(TwitterSelectors.TWITTER_CODE).text

    def login_for_verifier_code(self):
        self.visibility_of_element(TwitterSelectors.TWITTER_API_USERNAME).send_keys('sgeorgiev87@gmail.com')
        self.visibility_of_element(TwitterSelectors.TWITTER_API_PASSWORD).send_keys('Metallica87')
        self.visibility_of_element(TwitterSelectors.AUTHORIZE_APP_BUTTON).click()
