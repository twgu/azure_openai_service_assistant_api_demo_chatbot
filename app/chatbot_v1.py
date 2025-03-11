import time
import json

import streamlit as st

from azure_openai_service_client import AzureOpenAIServiceClient

if "client" not in st.session_state:
    st.session_state.client = AzureOpenAIServiceClient().get_client()
if "page" not in st.session_state:
    st.session_state.page = "streamlit_page_home"

if "client_assistant_id_list" not in st.session_state:
    st.session_state.client_assistant_id_list = []
if "client_assistant_name_list" not in st.session_state:
    st.session_state.client_assistant_name_list = []

if "selected_assistant_id" not in st.session_state:
    st.session_state.selected_assistant_id = ""
if "selected_thread_id" not in st.session_state:
    st.session_state.selected_thread_id = ""

if "db_thread_id_list" not in st.session_state:
    st.session_state.db_thread_id_list = []
if "db_thread_name_list" not in st.session_state:
    st.session_state.db_thread_name_list = []
if "db_assistant_id_list" not in st.session_state:
    st.session_state.db_assistant_id_list = []


def load_json():
    try:
        with open('db_v1.json', "r", encoding="utf-8") as file:
            content = file.read().strip()
            return json.loads(content) if content else {}
    except (FileNotFoundError, json.JSONDecodeError):
        return {}


def save_json(data):
    with open('db_v1.json', "w", encoding="utf-8") as file:
        json.dump(data, file, indent=4, ensure_ascii=False)


def refresh_db():
    db = load_json()

    st.session_state.db_thread_id_list = db.get("db_thread_id_list", [])
    st.session_state.db_thread_name_list = db.get("db_thread_name_list", [])
    st.session_state.db_assistant_id_list = db.get("db_assistant_id_list", [])

    return db


def refresh_client():
    st.session_state.client_assistant_id_list = []
    st.session_state.client_assistant_name_list = []

    response_client_beta_assistants_list = st.session_state.client.beta.assistants.list()

    for client_assistant in response_client_beta_assistants_list:
        st.session_state.client_assistant_id_list.append(client_assistant.id)
        st.session_state.client_assistant_name_list.append(client_assistant.name)


def streamlit_page_home():
    refresh_client()

    if len(st.session_state.client_assistant_id_list) == 0:
        st.subheader("Azure OpenAI Service에 Assistant가 없어 진행할 수 없습니다.")
        st.stop()

    st.title("메뉴 목록")

    if st.button("신규 Thread 생성"):
        st.session_state.page = "streamlit_page_new_thread"
        st.rerun()

    if st.button("Thread 목록"):
        st.session_state.page = "streamlit_page_thread"
        st.rerun()


def streamlit_page_new_thread():
    st.selectbox(
        label="Assistant 선택",
        options=st.session_state.client_assistant_name_list,
        key='selected_assistant_name'
    )

    st.text_input(label="Thread명", key='new_thread_name')

    if st.button('생성'):
        db = refresh_db()

        if st.session_state.new_thread_name in st.session_state.db_thread_name_list:
            st.write("이미 존재하는 Thread명 입니다.")
        else:
            response_client_beta_threads_create = st.session_state.client.beta.threads.create()

            idx = st.session_state.client_assistant_name_list.index(st.session_state.selected_assistant_name)

            st.session_state.db_thread_id_list.insert(0, response_client_beta_threads_create.id)
            st.session_state.db_thread_name_list.insert(0, st.session_state.new_thread_name)
            st.session_state.db_assistant_id_list.insert(0, st.session_state.client_assistant_id_list[idx])

            db["db_thread_id_list"] = st.session_state.db_thread_id_list
            db["db_thread_name_list"] = st.session_state.db_thread_name_list
            db["db_assistant_id_list"] = st.session_state.db_assistant_id_list

            save_json(db)

            st.session_state.page = "streamlit_page_thread"
            st.rerun()

    if st.button("뒤로가기"):
        st.session_state.page = "streamlit_page_home"
        st.rerun()


def streamlit_page_thread():
    refresh_db()

    if len(st.session_state.db_thread_id_list) == 0:
        st.subheader("저장된 Thread가 없습니다.")
        if st.button("뒤로가기"):
            st.session_state.page = "streamlit_page_home"
            st.rerun()
        st.stop()

    st.sidebar.title("옵션")

    st.sidebar.selectbox(
        label="Thread 선택",
        options=st.session_state.db_thread_name_list,
        key='selected_thread_name'
    )

    if st.sidebar.button("뒤로가기"):
        st.session_state.page = "streamlit_page_home"
        st.rerun()

    idx1 = st.session_state.db_thread_name_list.index(st.session_state.selected_thread_name)
    st.session_state.selected_thread_id = st.session_state.db_thread_id_list[idx1]
    st.session_state.selected_assistant_id = st.session_state.db_assistant_id_list[idx1]

    if st.session_state.selected_assistant_id in st.session_state.client_assistant_id_list:
        idx2 = st.session_state.client_assistant_id_list.index(st.session_state.selected_assistant_id)

        st.subheader(f'선택된 Assistant: {st.session_state.client_assistant_name_list[idx2]}')

        if st.chat_input("메시지를 입력하세요...", key='user_new_message'):
            st.session_state.client.beta.threads.messages.create(
                thread_id=st.session_state.selected_thread_id,
                role='user',
                content=st.session_state.user_new_message
            )

            response_client_beta_threads_runs_create = st.session_state.client.beta.threads.runs.create(
                thread_id=st.session_state.selected_thread_id,
                assistant_id=st.session_state.selected_assistant_id
            )

            while True:
                response_client_beta_threads_runs_retrieve = st.session_state.client.beta.threads.runs.retrieve(
                    thread_id=st.session_state.selected_thread_id,
                    run_id=response_client_beta_threads_runs_create.id
                )

                if response_client_beta_threads_runs_retrieve.status == "completed":
                    break

                time.sleep(1)

            st.rerun()
    else:
        st.subheader(f'선택된 Assistant: {st.session_state.selected_assistant_id}')

        st.chat_input("현재 지원되지 않는 Assistant 입니다.", disabled=True)

    response_client_beta_threads_messages_list = st.session_state.client.beta.threads.messages.list(
        thread_id=st.session_state.selected_thread_id,
        limit=100
    )

    thread_messages = response_client_beta_threads_messages_list.data
    thread_messages.sort(key=lambda row: row.created_at)

    for msg in thread_messages:
        with st.chat_message(msg.role):
            st.write(msg.content[0].text.value)


if st.session_state.page == "streamlit_page_home":
    streamlit_page_home()
elif st.session_state.page == "streamlit_page_new_thread":
    streamlit_page_new_thread()
elif st.session_state.page == "streamlit_page_thread":
    streamlit_page_thread()
