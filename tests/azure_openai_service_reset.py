from azure_openai_service_client import AzureOpenAIServiceClient

print('\nAzure OpenAI Service에 모든 Assistant, File, Vector Store를 삭제 하시겠습니까?')
user_input = input('>>> ').strip()

if user_input == "Y":
    client = AzureOpenAIServiceClient().get_client()

    # Assistant
    as_list = client.beta.assistants.list()

    for assistant in as_list:
        client.beta.assistants.delete(assistant_id=assistant.id)

    print('\nAssistant 삭제 완료')

    # # File
    fi_list = client.files.list()

    for file in fi_list:
        client.files.delete(file_id=file.id)

    print('\nFile 삭제 완료')

    # Vector Store
    ve_list = client.beta.vector_stores.list()

    for vector_store in ve_list:
        client.beta.vector_stores.delete(vector_store_id=vector_store.id)

    print('\nVector Store 삭제 완료')
