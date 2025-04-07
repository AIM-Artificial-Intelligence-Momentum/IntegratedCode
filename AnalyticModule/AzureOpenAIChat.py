import requests
import os
from dotenv import load_dotenv

class AzureOpenAIChat:
    def __init__(self):
        load_dotenv()

        # 환경 변수에서 Azure OpenAI API 정보 로드
        self.endpoint = os.getenv("AZURE_OPENAI_ENDPOINT")
        self.api_key = os.getenv("AZURE_OPENAI_API_KEY")
        self.deployment_name = os.getenv("DEPLOYMENT_NAME")
        self.headers = {
            'Content-Type': 'application/json',
            'api-key': self.api_key
        }

    def chatgpt_response(self, prompt, history):
        # print(prompt, history)
        headers = {
            'Content-Type': 'application/json',
            'api-key': self.api_key 
        }
        messages = []
        messages.append(
            {
                    "role": "system",
                    "content": [
                        {
                            "type": "text",
                            "text": "You are an AI assistant that helps find information!"
                        }
                    ]
            },
        )
        if len(history)>0:
            for text in history[0]:
                messages.append({
                    "role":"assistant",
                    "content":[{
                        "type":"text",
                        "text":text
                    }]
                })
        messages.append({
            "role":"user",
            "content":[
                {
                    "type":"text",
                    "text":prompt
                }
            ]
        })
        payload = {
            "messages": messages,
            "temperature": 0.7,
            "top_p": 0.95,
            "max_tokens": 4096
        }

        response = requests.post(
            self.endpoint,
            headers=headers,
            json=payload
        )

        result = response.json()
        bot_response = result['choices'][0]['message']['content'].strip()
        history.append({"role": "user", "content": prompt})
        history.append({"role": "assistant", "content": bot_response})
        return '', history
