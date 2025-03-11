import os
from dotenv import load_dotenv

from openai import AzureOpenAI


class AzureOpenAIServiceClient:
    _instance = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(AzureOpenAIServiceClient, cls).__new__(cls)
            cls._instance._initialize_client()
        return cls._instance

    def _initialize_client(self):
        load_dotenv()

        self.client = AzureOpenAI(
            azure_endpoint=os.getenv('ENDPOINT'),
            api_key=os.getenv('API_KEY'),
            api_version=os.getenv('API_VERSION')
        )

    def get_client(self):
        return self.client
