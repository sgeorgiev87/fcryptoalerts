from selenium.webdriver.common.by import By


class HomePageSelectors(object):
    NEWS_ROOM_BUTTON = (By.XPATH, '//button[text()="Newsroom"]')
    NEWS_ELEMENT = (By.CSS_SELECTOR, '.virtual-scroll-item')
    TIME_SINCE_POSTING = (By.CSS_SELECTOR, '.pl-2.text-xs.font-normal.text-gray-400')
    LINK_TO_POST = (By.XPATH, '//div[@class="virtual-scroll-item"]//a[contains(@href,"https://")]')


class TwitterSelectors(object):
    LOGIN_BUTTON = (By.CSS_SELECTOR, 'a[data-testid="loginButton"] span')
    USERNAME_INPUT = (By.CSS_SELECTOR, 'input[name="text"]')
    NEXT_BUTTON = (By.XPATH, '//span[text()="Next"]')
    PASSWORD_INPUT = (By.CSS_SELECTOR, 'input[name="password"]')
    LOGIN_CONFIRM_BUTTON = (By.XPATH, '//span[text()="Log in"]')
    INPUT_TWEET_TEXT = (By.CSS_SELECTOR, 'div[class*="public-DraftStyleDefault"]')
    POST_TWEET_BUTTON = (By.CSS_SELECTOR, 'div[data-testid="tweetButtonInline"] span')
    FIRST_TWEET_TEXT = (By.CSS_SELECTOR, 'div[data-testid="tweetText"]')
    AUTHORIZE_APP_BUTTON = (By.CSS_SELECTOR, '#allow')
    TWITTER_CODE = (By.CSS_SELECTOR, 'kbd code')
    TWITTER_API_USERNAME = (By.CSS_SELECTOR, '#username_or_email')
    TWITTER_API_PASSWORD = (By.CSS_SELECTOR, '#password')
