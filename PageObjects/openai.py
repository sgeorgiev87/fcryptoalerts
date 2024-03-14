from openai import OpenAI
from Configuration.credentials import Credentials


class OpenAIApi:

    @staticmethod
    def generate_and_return_text(ground_point):
        text = ''
        conversation = [
            {"role": "system", "content": "You are a helpful assistant."},
            {"role": "user", "content": f"Please generate me a logic text up to 150 words for the crypto industry based on the following text: {ground_point}"}
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
