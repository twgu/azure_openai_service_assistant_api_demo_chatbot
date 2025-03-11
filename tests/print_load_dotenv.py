import os
from dotenv import load_dotenv

load_dotenv()

print('\n[ 환경변수 목록 ]')
print(f'ENDPOINT={os.getenv("ENDPOINT")}')
print(f'API_KEY={os.getenv("API_KEY")}')
print(f'API_VERSION={os.getenv("API_VERSION")}')
print(f'DEFAULT_ASSISTANT_ID={os.getenv("DEFAULT_ASSISTANT_ID")}')
