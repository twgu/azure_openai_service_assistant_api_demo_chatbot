import time
import os
import openai

import json_db_control
import streamlit as st
from azure_openai_service_client import AzureOpenAIServiceClient
from datetime import datetime

# ##############################################################
# streamlit 세션 변수 관리
# ##############################################################
if 'page' not in st.session_state:
    st.session_state.page = 'home'

if 'client' not in st.session_state:
    st.session_state.client = AzureOpenAIServiceClient().get_client()

if 'client_thread_info' not in st.session_state:
    st.session_state.client_thread_info = None

if 'client_assistant_ids' not in st.session_state:
    st.session_state.client_assistant_ids = []

if 'client_assistant_names' not in st.session_state:
    st.session_state.client_assistant_names = []

if 'client_file_ids' not in st.session_state:
    st.session_state.client_file_ids = []

if 'client_file_names' not in st.session_state:
    st.session_state.client_file_names = []

if 'db_thread_ids' not in st.session_state:
    st.session_state.db_thread_ids = []

if 'db_thread_names' not in st.session_state:
    st.session_state.db_thread_names = []

if 'db_assistant_ids' not in st.session_state:
    st.session_state.db_assistant_ids = []

if 'selected_assistant_id' not in st.session_state:
    st.session_state.selected_assistant_id = ''

if 'selected_thread_id' not in st.session_state:
    st.session_state.selected_thread_id = ''


def refresh_client_assistants():
    print(f'[{datetime.now()}] def refresh_client_assistants():')

    response = st.session_state.client.beta.assistants.list()

    new_ids = []
    new_names = []

    for assistant in response:
        new_ids.append(assistant.id)
        new_names.append(assistant.name)

    st.session_state.client_assistant_ids = new_ids
    st.session_state.client_assistant_names = new_names


def refresh_client_files():
    print(f'[{datetime.now()}] def refresh_client_files():')

    response = st.session_state.client.files.list()

    new_ids = []
    new_names = []

    for file in response:
        new_ids.append(file.id)
        new_names.append(file.filename)

    st.session_state.client_file_ids = new_ids
    st.session_state.client_file_names = new_names


def refresh_db():
    print(f'[{datetime.now()}] def refresh_db():')

    db = json_db_control.load_json('db_v2.json')

    st.session_state.db_thread_ids = db.get('db_thread_ids', [])
    st.session_state.db_thread_names = db.get('db_thread_names', [])
    st.session_state.db_assistant_ids = db.get('db_assistant_ids', [])


# ##############################################################
# streamlit 페이지
# ##############################################################
def page_home():
    print(f'[{datetime.now()}] 페이지 렌더링: home')

    st.title('🏠 Home')
    st.button('💬 대화방으로 이동', on_click=move_page_chat)
    st.button('➕ 신규 대화 생성', on_click=move_page_new_chat)
    st.button('⚙️ 설정', on_click=move_page_settings)


def page_chat():
    print(f'[{datetime.now()}] 페이지 렌더링: chat')

    refresh_client_assistants()
    refresh_client_files()
    refresh_db()

    st.markdown(
        """
        <style>
        .st-emotion-cache-fis6aj.e1blfcsg5 {
            display: none;
        }
        </style>
        """,
        unsafe_allow_html=True
    )

    if len(st.session_state.db_thread_names) == 0:
        st.subheader('🚫 선택 가능한 대화방이 없습니다.')
        st.button('➕ 신규 대화 생성', on_click=move_page_new_chat)
        st.button('🏠 Home', on_click=move_page_home)
        st.stop()

    st.sidebar.title('💬 대화방')

    st.sidebar.button('🏠 Home', on_click=move_page_home)

    st.sidebar.button('➕ 신규 대화 생성', on_click=move_page_new_chat)

    st.sidebar.selectbox(
        label='대화방 선택',
        options=st.session_state.db_thread_names,
        key='page_chat_selectbox_value'
    )

    # 선택한 Thread 이름으로 Thread ID, Assistant ID 찾기
    thred_name_idx = st.session_state.db_thread_names.index(st.session_state.page_chat_selectbox_value)
    st.session_state.selected_thread_id = st.session_state.db_thread_ids[thred_name_idx]
    st.session_state.selected_assistant_id = st.session_state.db_assistant_ids[thred_name_idx]

    # Assistant ID로 Assistant 이름 찾기
    if st.session_state.selected_assistant_id in st.session_state.client_assistant_ids:
        assistant_id_idx = st.session_state.client_assistant_ids.index(st.session_state.selected_assistant_id)
        assistant_name = st.session_state.client_assistant_names[assistant_id_idx]
    else:
        assistant_name = st.session_state.selected_assistant_id

    st.sidebar.subheader(f'🤖 대화 모델: {assistant_name}')

    # 대화 기록 불러오기
    messages = st.session_state.client.beta.threads.messages.list(
        thread_id=st.session_state.selected_thread_id,
        limit=100
    ).data

    messages.sort(key=lambda msg: msg.created_at)

    for message in messages:
        with st.chat_message(message.role):
            st.write(message.content[0].text.value)

    if st.session_state.selected_assistant_id in st.session_state.client_assistant_ids:
        st.chat_input('메세지를 입력하세요...', key='page_chat_chat_input_value', on_submit=new_message)
    else:
        st.chat_input('🚫 현재 지원되지 않는 대화 모델 입니다.', disabled=True)

    try:
        # Assistant 정보 조회
        assistant_info = st.session_state.client.beta.assistants.retrieve(
            assistant_id=st.session_state.selected_assistant_id
        )

        assistant_tools = assistant_info.tools

        # Thread 정보 조회
        st.session_state.client_thread_info = st.session_state.client.beta.threads.retrieve(
            thread_id=st.session_state.selected_thread_id
        )

        for tool in assistant_tools:
            st.sidebar.markdown("---")

            if tool.type == 'file_search':
                st.sidebar.file_uploader(
                    label='📁 파일 검색',
                    key='page_chat_file_uploader1_value',
                    on_change=new_file_search
                )

                for fsvsid in st.session_state.client_thread_info.tool_resources.file_search.vector_store_ids:
                    thread_vector_store_files = st.session_state.client.beta.vector_stores.files.list(
                        vector_store_id=fsvsid
                    )

                    for tvsf in thread_vector_store_files.data:
                        file_id_idx1 = st.session_state.client_file_ids.index(tvsf.id)
                        file_name1 = st.session_state.client_file_names[file_id_idx1]
                        st.sidebar.write(file_name1)
            elif tool.type == 'code_interpreter':
                st.sidebar.file_uploader(
                    label='🧑‍💻 코드 인터프리터',
                    key='page_chat_file_uploader2_value',
                    on_change=new_code_interpreter
                )

                for cifid in st.session_state.client_thread_info.tool_resources.code_interpreter.file_ids:
                    file_id_idx2 = st.session_state.client_file_ids.index(cifid)
                    file_name2 = st.session_state.client_file_names[file_id_idx2]
                    st.sidebar.write(file_name2)

    except openai.NotFoundError as ex:
        print(ex)


def page_new_chat():
    print(f'[{datetime.now()}] 페이지 렌더링: new_chat')

    refresh_client_assistants()

    if len(st.session_state.client_assistant_names) == 0:
        st.subheader('🚫 선택 가능한 대화 모델이 없습니다.')
        st.button('🏠 Home', on_click=move_page_home)
        st.stop()

    st.title('➕ 신규 대화 생성')

    st.selectbox(
        label='1️⃣ 모델 선택',
        options=st.session_state.client_assistant_names,
        key='page_new_chat_selectbox_value'
    )

    st.text_input(label="2️⃣ 대화방 이름", key='page_new_chat_text_input_value')

    st.button('✅ 생성', on_click=create_thread)

    st.button('🏠 Home', on_click=move_page_home)


def page_settings():
    print(f'[{datetime.now()}] 페이지 렌더링: settings')

    st.title('⚙️ 설정')
    st.button('🏠 Home', on_click=move_page_home)


# ##############################################################
# 함수
# ##############################################################
def create_thread():
    print(f'[{datetime.now()}] def create_thread():')

    refresh_db()

    # Thread 이름 중복 불가
    thread_name = st.session_state.page_new_chat_text_input_value

    subheader_text = ''
    if thread_name in st.session_state.db_thread_names:
        subheader_text = '🚫 대화방 이름이 이미 존재합니다.'
    elif thread_name == '':
        subheader_text = '🚫 대화방 이름은 비어있을 수 없습니다.'

    if thread_name in st.session_state.db_thread_names or thread_name == '':
        st.subheader(subheader_text)
        st.button('🔙 뒤로가기', on_click=move_page_new_chat)
        st.button('💬 대화방으로 이동', on_click=move_page_chat)
        st.button('🏠 Home', on_click=move_page_home)
        st.stop()

    # Vector Store 생성
    vector_store_id = st.session_state.client.beta.vector_stores.create().id

    # Thread 생성
    thread_id = st.session_state.client.beta.threads.create(
        tool_resources={
            "file_search": {
                "vector_store_ids": [vector_store_id]
            },
            "code_interpreter": {
                "file_ids": []
            }
        }
    ).id

    # 선택한 Assistant 이름으로 Assistant ID 찾기
    assistant_name = st.session_state.page_new_chat_selectbox_value
    assistant_name_idx = st.session_state.client_assistant_names.index(assistant_name)
    assistant_id = st.session_state.client_assistant_ids[assistant_name_idx]

    # DB 저장
    thread_ids = st.session_state.db_thread_ids
    thread_names = st.session_state.db_thread_names
    assistant_ids = st.session_state.db_assistant_ids

    thread_ids.insert(0, thread_id)
    thread_names.insert(0, thread_name)
    assistant_ids.insert(0, assistant_id)

    data = {
        "db_thread_ids": thread_ids,
        "db_thread_names": thread_names,
        "db_assistant_ids": assistant_ids
    }

    json_db_control.save_json('db_v2.json', data)

    # 페이지 이동
    move_page_chat()


def new_message():
    print(f'[{datetime.now()}] def new_message():')

    st.session_state.client.beta.threads.messages.create(
        thread_id=st.session_state.selected_thread_id,
        role='user',
        content=st.session_state.page_chat_chat_input_value
    )

    run_id = st.session_state.client.beta.threads.runs.create(
        thread_id=st.session_state.selected_thread_id,
        assistant_id=st.session_state.selected_assistant_id
    ).id

    while True:
        run_status = st.session_state.client.beta.threads.runs.retrieve(
            run_id=run_id,
            thread_id=st.session_state.selected_thread_id
        ).status

        if run_status == 'completed':
            break

        time.sleep(1)


def new_file_search():
    print(f'[{datetime.now()}] def new_file_search():')

    uploaded_file = st.session_state.page_chat_file_uploader1_value

    upload_dir = 'temp_file_store'
    os.makedirs(upload_dir, exist_ok=True)

    file_path = os.path.join(upload_dir, uploaded_file.name)

    with open(file_path, 'wb') as f:
        f.write(uploaded_file.getbuffer())

    with open(file_path, 'rb') as f2:
        file_id = st.session_state.client.files.create(file=f2, purpose='assistants').id

    # 현재 버전에서는 Thread 생성 시 Vector Store를 생성하고 1:1로 묶어줌..
    vector_store_id = st.session_state.client_thread_info.tool_resources.file_search.vector_store_ids[0]

    st.session_state.client.beta.vector_stores.files.create(
        vector_store_id=vector_store_id,
        file_id=file_id
    )

    if file_path and os.path.exists(file_path):
        os.remove(file_path)


def new_code_interpreter():
    print(f'[{datetime.now()}] def new_code_interpreter():')

    uploaded_file = st.session_state.page_chat_file_uploader2_value

    upload_dir = 'temp_file_store'
    os.makedirs(upload_dir, exist_ok=True)

    file_path = os.path.join(upload_dir, uploaded_file.name)

    with open(file_path, "wb") as f:
        f.write(uploaded_file.getbuffer())

    with open(file_path, 'rb') as f2:
        file_id = st.session_state.client.files.create(file=f2, purpose='assistants').id

    file_ids = st.session_state.client_thread_info.tool_resources.code_interpreter.file_ids

    file_ids.append(file_id)

    st.session_state.client.beta.threads.update(
        thread_id=st.session_state.selected_thread_id,
        tool_resources={
            "code_interpreter": {
                "file_ids": file_ids
            }
        }
    )

    if file_path and os.path.exists(file_path):
        os.remove(file_path)


# ##############################################################
# streamlit 페이지 이동
# ##############################################################
def move_page_home():
    st.session_state.page = 'home'


def move_page_chat():
    st.session_state.page = 'chat'


def move_page_new_chat():
    st.session_state.page = 'new_chat'


def move_page_settings():
    st.session_state.page = 'settings'


if st.session_state.page == 'home':
    page_home()
elif st.session_state.page == 'chat':
    page_chat()
elif st.session_state.page == 'new_chat':
    page_new_chat()
elif st.session_state.page == 'settings':
    page_settings()
