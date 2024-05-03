import requests
from requests_oauthlib import OAuth1Session
import os
import json


class TwitterAPI:
    def __init__(self):
        self.consumer_key = os.environ.get("CONSUMER_KEY")
        self.consumer_secret = os.environ.get("CONSUMER_SECRET")
        # str2 = ('OAuth oauth_consumer_key="vv4ja2BrPWKWqyRp8ngyP2Jq6",'
        #         'oauth_token="131473528-ziTQfwHTmmVUapw4otGJEthTSWV8VVMCZmnXkOjF",oauth_signature_method="HMAC-SHA1",'
        #         'oauth_timestamp="1713795921",oauth_nonce="JZaOkd4xRUk",oauth_version="1.0",'
        #         'oauth_signature="DUM0BKFgFZZ%2BVhiLv1UeA20Kf9c%3D"')
        #
        # str3 = ('OAuth oauth_consumer_key="vv4ja2BrPWKWqyRp8ngyP2Jq6",'
        #         'oauth_token="131473528-ziTQfwHTmmVUapw4otGJEthTSWV8VVMCZmnXkOjF",oauth_signature_method="HMAC-SHA1",'
        #         'oauth_timestamp="1713796034",oauth_nonce="gVT1g8MhZMZ",oauth_version="1.0",'
        #         'oauth_signature="Z9%2B9TeBQBgiwUNVrG3X1hc94pjw%3D"')
        self.resource_owner_key = ''
        self.resource_owner_secret = ''
        self.verifier = ''
        self.payload = {"text": "Hello world123!"}

    def get_authorization_url(self):
        request_token_url = "https://api.twitter.com/oauth/request_token?oauth_callback=oob&x_auth_access_type=write"
        oauth = OAuth1Session(self.consumer_key, client_secret=self.consumer_secret)

        try:
            fetch_response = oauth.fetch_request_token(request_token_url)
        except ValueError:
            print(
                "There may have been an issue with the consumer_key or consumer_secret you entered."
            )

        self.resource_owner_key = fetch_response.get("oauth_token")
        self.resource_owner_secret = fetch_response.get("oauth_token_secret")
        print("Got OAuth token: %s" % self.resource_owner_key)

        # Get authorization
        base_authorization_url = "https://api.twitter.com/oauth/authorize"
        authorization_url = oauth.authorization_url(base_authorization_url)
        print("Please go here and authorize: %s" % authorization_url)
        return authorization_url

    def set_verifier(self, verifier):
        self.verifier = verifier
    25 години .. а ще отеква във вечността

    def create_tweet(self, tweet_text):
        # Get the access token
        access_token_url = "https://api.twitter.com/oauth/access_token"
        oauth = OAuth1Session(
            self.consumer_key,
            client_secret=self.consumer_secret,
            resource_owner_key=self.resource_owner_key,
            resource_owner_secret=self.resource_owner_secret,
            verifier=self.verifier,
        )
        oauth_tokens = oauth.fetch_access_token(access_token_url)

        access_token = oauth_tokens["oauth_token"]
        access_token_secret = oauth_tokens["oauth_token_secret"]

        # Make the request
        oauth = OAuth1Session(
            self.consumer_key,
            client_secret=self.consumer_secret,
            resource_owner_key=access_token,
            resource_owner_secret=access_token_secret,
        )

        # Making the request
        response = oauth.post(
            "https://api.twitter.com/2/tweets",
            json=tweet_text,
        )

        if response.status_code != 201:
            raise Exception(
                "Request returned an error: {} {}".format(response.status_code, response.text)
            )

        print("Response code: {}".format(response.status_code))

        # Saving the response as JSON
        json_response = response.json()
        print(json.dumps(json_response, indent=4, sort_keys=True))
