from openai import OpenAI
from Configuration.constants import Credentials


class OpenAIApi:

    @staticmethod
    def generate_and_return_text_for_specific_number_of_words(main_topic: str, number_of_words: int = 50):
        text = ''
        conversation = [
            {"role": "system", "content": "You are a helpful assistant."},
            {"role": "user", "content": f"Please generate me a logic text up to {str(number_of_words)} words "
                                        f"for the crypto industry, based on the following text: {main_topic}"}
        ]
        client = OpenAI(api_key=Credentials.OPEN_AI_KEY)
        stream = client.chat.completions.create(
            model="gpt-4",
            messages=conversation,
            stream=True,
        )

        for chunk in stream:
            if chunk.choices[0].delta.content is not None:
                text = text + chunk.choices[0].delta.content
        return text

    @staticmethod
    def generate_and_return_text_for_specific_number_of_chars(main_topic: str, number_of_chars: int = 280):
        text = ''
        conversation = [
            {"role": "system", "content": "You are a helpful assistant."},
            {"role": "user", "content": f"Please generate me a logic text up to {str(number_of_chars)} letters,"
                                        f"and it is really important the text to be no more than {str(number_of_chars)} symbols,"
                                        f"so, please, do not make it any longer, "
                                        f"for the crypto industry, based on the following text: {main_topic}"
                                        f" and add 1 or 2 emoticons at the end of the text! "
                                        f"But, please, it is really important to have the text no more than 280 letters"
                                        f"including the emoticons"}
        ]
        client = OpenAI(api_key=Credentials.OPEN_AI_KEY)
        stream = client.chat.completions.create(
            model="gpt-4",
            messages=conversation,
            stream=True,
        )

        for chunk in stream:
            if chunk.choices[0].delta.content is not None:
                text = text + chunk.choices[0].delta.content

        # if len(text) < 280:
        return text

    # def get_text(self, main_topic, chars: int = 280):
    #     generated_text = self.generate_and_return_text_for_specific_number_of_chars(main_topic, chars)
    #     counter


