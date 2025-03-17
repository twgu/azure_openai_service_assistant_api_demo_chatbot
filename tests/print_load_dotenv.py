import os
from dotenv import load_dotenv

load_dotenv()

print('\n[ 환경변수 목록 ]')
print(f'AZURE_OPENAI_ENDPOINT={os.getenv("AZURE_OPENAI_ENDPOINT")}')
print(f'AZURE_OPENAI_API_KEY={os.getenv("AZURE_OPENAI_API_KEY")}')
print(f'API_VERSION={os.getenv("API_VERSION")}')
