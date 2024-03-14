import datetime
import json
import requests
import time

from Configuration.constants import Credentials, URLs


class ElaiAPI:
    def __init__(self):
        self.url = URLs.ELAI_API_BASE_URL
        self.video_id = ''
        self.video_url = ''

    def generate_video_from_text(self, text_for_video):
        current_utc_time = datetime.datetime.utcnow().replace(microsecond=0)
        payload = {
            "name": f"Video generated at {str(current_utc_time)} UTC time",
            "tags": ["test"],
            "public": True,
            "data": {
                "skipEmails": False,
                "subtitlesEnabled": "false",
                "format": "16_9",
                "musicUrl": "https://elai-media.s3.eu-west-2.amazonaws.com/music/mixkit-driving-ambition-32.mp3",
                "musicVolume": 0.17,
                "resolution": "FullHD"
            }, "slides": [
                {
                    "id": 1,
                    "canvas": {
                        "background": "#ffffff",
                        "version": "4.4.0",
                        "objects": [
                            {
                                "id": 1,
                                "type": "avatar",
                                "src": "https://elai-media.s3.eu-west-2.amazonaws.com/avatars/jade.png",
                                "top": 20,
                                "left": 150,
                                "scaleX": 0.37,
                                "scaleY": 0.37,
                                "avatarType": "transparent",
                                "version": 2
                            }
                        ]
                    },
                    "avatar": {
                        "id": "jade",
                        "name": "Jade",
                        "gender": "female",
                        "version": 2
                    },
                    "animation": "fade_in",
                    "language": "English",
                    "speech": text_for_video,
                    "voiceType": "text",
                    "voice": "en-US-AriaNeural",
                    "voiceProvider": "azure"
                }
            ]
        }
        headers = {
            "accept": "application/json",
            "content-type": "application/json",
            "Authorization": f"Bearer {Credentials.ELAI_API_KEY}"
        }
        response = requests.post(self.url, json=payload, headers=headers)
        response_text_json = json.loads(response.text)
        self.video_id = response_text_json['_id']

    def render_video(self):
       # @TODO - optimize it - first start rendering of all videos,
       #  and then get the links - so, we do not wait 60+ seconds for each one!
        render_api_url = f"{self.url}/render/{self.video_id}"
        headers = {
            "accept": "application/json",
            "Authorization": f"Bearer {Credentials.ELAI_API_KEY}"
        }
        requests.post(render_api_url, headers=headers)

    def get_url_for_rendered_video(self):
        get_video_api_url = f'{self.url}/{self.video_id}'
        headers = {
            "accept": "application/json",
            "Authorization": f"Bearer {Credentials.ELAI_API_KEY}"
        }
        counter = 1
        video_url = ''
        while video_url == '':
            if counter == 180:
                raise Exception(f'#### VIDEO ID {self.video_id} was not retrieved in 180 seconds!!!')
            try:
                response = requests.get(get_video_api_url, headers=headers)
                response_text_json = json.loads(response.text)
                video_url = response_text_json['url']
            except KeyError:
                print(f'Iteration {str(counter)}')
                time.sleep(1)
                counter += 1
        video_url = video_url.replace('public/video', 'preview').replace('apis', 'app')
        index = video_url.find('.mp4')
        self.video_url = video_url[:index]
        return self.video_url


