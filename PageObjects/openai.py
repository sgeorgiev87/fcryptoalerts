from openai import OpenAI
from Configuration.constants import Credentials


class OpenAIApi:

    @staticmethod
    def generate_and_return_text(main_topic: str, number_of_words: int = 50):
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
