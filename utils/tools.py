import streamlit as st
from PyPDF2 import PdfReader

def approach_agent(company: str, request: str) -> str:
    """
    회사 이름을 가지고 해당 회사의 Agent에게 연락을 취하여 답을 얻어주는 함수.

    Args:
        company: 타 회사 이름
        request: 타 회사 Agent에게 요청하고 싶은 정보
    """

    print(f"start {company} approach_agent")
    print(f"request is {request}.")

    agent_name = f"{company}_agent"
    agent_message = f"{company}_message"

    if agent_name not in st.session_state.agent_dictionary:
        return "해당 회사가 존재하지 않음"
    
    agent = st.session_state.agent_dictionary[agent_name]

    message = {
        "role": "user",
        "content": request
    }

    st.session_state.agent_messages[agent_message].append(message)

    result, output_messages = agent.run(st.session_state.agent_messages[agent_message])
    st.session_state.agent_messages[agent_message] = output_messages

    return result

def search_docs(company: str) -> str:
    """
    원하는 회사의 문서에 접근해서 정보를 가져오는 함수.(사실상 자기 자신의 회사)

    Args:
        company: 문서를 찾길 원하는 회사. 종류는 "A회사", "B회사", "C회사", "D회사", "E회사", "F회사", "G회사", "H회사"이 있다.
    """

    print(f"{company} search_docs")

    docs_name = f"{company}_docs"

    if docs_name not in st.session_state.docs_dictionary:
        return "해당 문서는 존재하지 않음."
    
    uploaded_docs = st.session_state.docs_dictionary[docs_name]

    pdf = PdfReader(uploaded_docs)

    company_docs = ""
    for page in pdf.pages:
        company_docs += company_docs.extract_text()

    return company_docs