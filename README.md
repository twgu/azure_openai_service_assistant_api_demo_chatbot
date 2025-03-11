# 개요

Azure OpenAI Service Assistant API Demo Chatbot

- streamlit UI 활용

# 개발 환경

SDK

- Python (Version: 3.11.5)

    ```bash
    python --version
    ```

Install Libraries

- python-dotenv (Version: 1.0.1)

    ```bash
    pip install python-dotenv
    ```

    ```bash
    pip show python-dotenv
    ```

- streamlit (Version: 1.42.2)

    ```bash
    pip install streamlit
    ```

    ```bash
    pip show streamlit
    ```

- openai (Version: 1.64.0)

    ```bash
    pip install openai
    ```

    ```bash
    pip show openai
    ```

# streamlit Run Guide

Terminal에서 실행 대상 파일이 있는 경로로 이동 후 아래와 같이 명령어 입력

```bash
streamlit run file_name.py
```

# Test Playground Guide

`test_playground.py`: 기본 테스트 파일, 자유롭게 작성 및 수정

Python Basic

- `print_load_dotenv.py`: 환경 변수 목록 출력

- `json_file_control.py`

    + JSON Data 출력

    + JSON Data 추가

    + JSON Data 삭제

    + DB File = `json_file_control.json`

Azure OpenAI Service

- `azure_openai_service_assistant.py`

    + Assistant 목록 출력

    + Assistant 정보 조회

- `azure_openai_service_thread.py`

    + Thread 대화 기록 출력

    + Thread 정보 조회

- `azure_openai_service_file.py`

    + File 목록 출력

    + File 추가

    + File 삭제

- `azure_openai_service_vector_store.py`

    + Vector Store 목록 출력

    + Vector Store 추가

    + Vector Store 삭제

    + Vector Store File 목록 출력

    + Vector Store File 추가

    + Vector Store File 삭제

- `azure_openai_service_reset.py`: Assistant, File, Vector Store 초기화

streamlit

- `streamlit_run_example.py`: streamlit 실행 예제

- `streamlit_login_example.py`: streamlit 로그인 예제 (페이지 전환 예제)
