import streamlit as st
from utils.companies import companies
from utils.create_agent import Agent, load_agent
from utils.create_persona import create_persona

st.set_page_config(
    layout="wide",
    page_icon="😀",
    page_title="회사 정보 입력"
)

st.write("# 😀Create Your Company!")
uploaded_file = st.file_uploader("**문서 업로드**")

col1, col2 = st.columns([1, 3])

with col1:
    company = st.selectbox("**회사 선택**", companies)
    description = st.text_input("**회사 설명란**")
    is_save = st.button("**저장**")

    if is_save:
        if not uploaded_file:
            st.write("파일 업로드는 필수입니다😅")
        if not company:
            st.write("회사가 정해지지 않았습니다😅")
        if not description:
            st.write("회사에 대한 설명을 해주세요😅")
        else:
            progress_bar = st.progress(0)
            status_text = st.empty()

            status_text.text("시작...")
            progress_bar.progress(10)

            agent_name = f"{company}_agent"
            agent_message = f"{company}_message"
            docs_name = f"{company}_docs"

            status_text.text("에이전트 생성 중...")
            progress_bar.progress(30)

            st.session_state.agent_dictionary[agent_name] = load_agent(_tools=st.session_state.tools, _tool_repository=st.session_state.tool_repository)

            status_text.text("프롬프트 생성 중...")
            progress_bar.progress(70)
            
            st.session_state.agent_messages[agent_message] = create_persona(company, description)

            status_text.text("파일 업로드 중...")
            progress_bar.progress(90)
            st.session_state.docs_dictionary[docs_name] = uploaded_file

            progress_bar.progress(100)
            status_text.text("완료!")
            
            st.write("축하드립니다😊 당신만의 Agent가 등록되었어요!")