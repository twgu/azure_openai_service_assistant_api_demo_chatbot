import streamlit as st

if "page" not in st.session_state:
    st.session_state.page = "login"


def login_page():
    st.title("로그인 페이지")
    user_input = st.text_input("사용자 이름", key="user_input")
    if st.button("로그인"):
        if user_input:
            st.session_state.user = user_input
            st.session_state.page = "main"
            st.rerun()


def main_page():
    st.title("메인 페이지")
    st.write(f"환영합니다, **{st.session_state.user}**님!")
    if st.button("로그아웃"):
        st.session_state.user = None
        st.session_state.page = "login"
        st.rerun()


if st.session_state.page == "login":
    login_page()
elif st.session_state.page == "main":
    main_page()
