from azure_openai_service_client import AzureOpenAIServiceClient

client = AzureOpenAIServiceClient().get_client()


def client_beta_vector_stores_list():
    response = client.beta.vector_stores.list()
    print('\n[ Vector Store 목록 ]')
    for res in response:
        print(f'Vector Store ID: {res.id}, Vector Store Name: {res.name}')


def client_beta_vector_stores_create():
    print('\nVector Store Name 입력')
    vector_store_name = input('>>> ').strip()
    client.beta.vector_stores.create(name=vector_store_name)
    print('\nVector Store 추가 성공')
    client_beta_vector_stores_list()


def client_beta_vector_stores_delete():
    print('\nVector Store ID 입력')
    vector_store_id = input('>>> ').strip()
    client.beta.vector_stores.delete(vector_store_id=vector_store_id)
    print('\nVector Store 삭제 성공')
    client_beta_vector_stores_list()


def client_beta_vector_stores_files_list():
    print('\nVector Store ID 입력')
    vector_store_id = input('>>> ').strip()
    response = client.beta.vector_stores.files.list(vector_store_id=vector_store_id)
    print('\n[ Vector Store File 목록 ]')
    for res_data in response.data:
        print(f'File ID: {res_data.id}')


def client_beta_vector_stores_files_create():
    print('\nVector Store ID 입력')
    vector_store_id = input('>>> ').strip()
    print('\nFile ID 입력')
    file_id = input('>>> ').strip()
    client.beta.vector_stores.files.create(vector_store_id=vector_store_id, file_id=file_id)
    print('\nVector Store File 추가 성공')


def client_beta_vector_stores_files_delete():
    print('\nVector Store ID 입력')
    vector_store_id = input('>>> ').strip()
    print('\nFile ID 입력')
    file_id = input('>>> ').strip()
    client.beta.vector_stores.files.delete(vector_store_id=vector_store_id, file_id=file_id)
    print('\nVector Store File 삭제 성공')


while True:
    print('\n작업 선택')
    print('0: 종료')
    print('1: Vector Store 목록 출력')
    print('2: Vector Store 추가')
    print('3: Vector Store 삭제')
    print('4: Vector Store File 목록 출력')
    print('5: Vector Store File 추가')
    print('6: Vector Store File 삭제')
    user_input = input('>>> ').strip()
    if user_input == '0':
        break
    elif user_input == '1':
        client_beta_vector_stores_list()
    elif user_input == '2':
        client_beta_vector_stores_create()
    elif user_input == '3':
        client_beta_vector_stores_delete()
    elif user_input == '4':
        client_beta_vector_stores_files_list()
    elif user_input == '5':
        client_beta_vector_stores_files_create()
    elif user_input == '6':
        client_beta_vector_stores_files_delete()
    else:
        print('\n올바른 번호를 입력하세요')
