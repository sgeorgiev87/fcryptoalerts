import time

import requests
from requests_oauthlib import OAuth1Session
from requests_oauthlib.oauth1_session import TokenRequestDenied
import os
import json


class TwitterAPI:
    def __init__(self):
        self.consumer_key = os.environ.get("CONSUMER_KEY")
        self.consumer_secret = os.environ.get("CONSUMER_SECRET")
        print(f'Consumer key in Twitter init is: {self.consumer_key}')
        print(f'Consumer Secret in Twitter init is: {self.consumer_secret}')
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

        counter = 1
        while counter < 10:
            try:
                print(f'Counter is: {str(counter)}')
                oauth_tokens = oauth.fetch_access_token(access_token_url)
                break
            except TokenRequestDenied:
                print(f'I am in the exception!!! Counter is: {str(counter)}')
                time.sleep(15)
                counter += 1
        if counter == 10:
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
            json={"text": tweet_text},
        )

        if response.status_code != 201:
            raise Exception(
                "Request returned an error: {} {}".format(response.status_code, response.text)
            )

        print("Response code: {}".format(response.status_code))

        # Saving the response as JSON
        json_response = response.json()
        print(json.dumps(json_response, indent=4, sort_keys=True))
        time.sleep(20)
