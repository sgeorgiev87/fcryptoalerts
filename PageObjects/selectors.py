from selenium.webdriver.common.by import By


class HomePageSelectors(object):
    NEWS_ROOM_BUTTON = (By.XPATH, '//button[text()="Newsroom"]')
    NEWS_ELEMENT = (By.CSS_SELECTOR, '.virtual-scroll-item')
    TIME_SINCE_POSTING = (By.CSS_SELECTOR, '.pl-2.text-xs.font-normal.text-gray-400')
    LINK_TO_POST = (By.XPATH, '//div[@class="virtual-scroll-item"]//a[contains(@href,"https://")]')


class TwitterSelectors(object):
    FIRST_TWEET_TEXT = (By.CSS_SELECTOR, 'div[data-testid="tweetText"]')
