from azure_openai_service_client import AzureOpenAIServiceClient

client = AzureOpenAIServiceClient().get_client()


def client_beta_assistants_list():
    response = client.beta.assistants.list()
    print('\n[ Assistant 목록 ]')
    for res in response:
        print(f'Assistant ID: {res.id}, Assistant Name: {res.name}')


def client_beta_assistants_retrieve():
    print('\nAssistant ID 입력')
    assistant_id = input('>>> ').strip()
    response = client.beta.assistants.retrieve(assistant_id=assistant_id)
    print('\nAssistant 정보')


while True:
    print('\n작업 선택')
    print('0: 종료')
    print('1: Assistant 목록 출력')
    print('2: Assistant 정보 조회')
    user_input = input('>>> ').strip()
    if user_input == '0':
        break
    elif user_input == '1':
        client_beta_assistants_list()
    elif user_input == '2':
        client_beta_assistants_retrieve()
    else:
        print('\n올바른 번호를 입력하세요')
