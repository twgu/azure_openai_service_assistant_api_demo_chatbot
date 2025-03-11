import os

from azure_openai_service_client import AzureOpenAIServiceClient

client = AzureOpenAIServiceClient().get_client()


def client_files_list():
    response = client.files.list()
    print('\n[ File 목록 ]')
    for res in response:
        print(f'File ID: {res.id}, File Name: {res.filename}')


def client_files_create():
    while True:
        print('\nLocal File Path 입력')
        local_file_path = input('>>> ').strip()
        if not os.path.exists(local_file_path):
            print('\nFile이 존재하지 않습니다.')
        else:
            break

    with open(local_file_path, 'rb') as file:
        client.files.create(file=file, purpose='assistants')
        print('\nFile 추가 성공')

    client_files_list()


def client_files_delete():
    print('\nFile ID 입력')
    file_id = input('>>> ').strip()
    client.files.delete(file_id)
    print('\nFile 삭제 성공')
    client_files_list()


while True:
    print('\n작업 선택')
    print('0: 종료')
    print('1: File 목록 출력')
    print('2: File 추가')
    print('3: File 삭제')
    user_input = input('>>> ').strip()
    if user_input == '0':
        break
    elif user_input == '1':
        client_files_list()
    elif user_input == '2':
        client_files_create()
    elif user_input == '3':
        client_files_delete()
    else:
        print('\n올바른 번호를 입력하세요')
