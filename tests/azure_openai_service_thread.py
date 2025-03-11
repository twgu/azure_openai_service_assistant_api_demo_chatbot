from azure_openai_service_client import AzureOpenAIServiceClient

client = AzureOpenAIServiceClient().get_client()


def client_beta_threads_messages_list():
    print('\nThread ID 입력')
    thread_id = input('>>> ').strip()
    response = client.beta.threads.messages.list(thread_id=thread_id)
    messages = response.data
    messages.sort(key=lambda message: message.created_at)
    print('\n[ Thread 대화 기록 ]')
    for msg in messages:
        print(f'\n\n\n{msg.role}: {msg.content[0].text.value}')


def client_beta_threads_retrieve():
    print('\nThread ID 입력')
    thread_id = input('>>> ').strip()
    response = client.beta.threads.retrieve(thread_id=thread_id)
    print('\nThread 정보')

while True:
    print('\n작업 선택')
    print('0: 종료')
    print('1: Thread 대화 기록 출력')
    print('2: Thread 정보 조회')
    user_input = input('>>> ').strip()
    if user_input == '0':
        break
    elif user_input == '1':
        client_beta_threads_messages_list()
    elif user_input == '2':
        client_beta_threads_retrieve()
    else:
        print('\n올바른 번호를 입력하세요')

# thread_20BqraI0oHR5FRQ2hljCfM2f
