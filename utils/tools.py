import streamlit as st

def approach_agent(department: str, request: str) -> str:
    """
    부서 이름을 가지고 해당 부서의 Agent에게 연락을 취하여 답을 얻어주는 함수.

    Args:
        department: 부서 이름
        request: 부서 Agent에게 요청하고 싶은 정보
    """

    agent_name = f"{department}_agent"
    agent_message = f"{department}_message"

    if agent_name not in st.session_state.agent_dictionary:
        return "해당 부서가 존재하지 않음"
    
    agent = st.session_state.agent_dictionary[agent_name]

    message = {
        "role": "user",
        "content": request
    }

    st.session_state.agent_messages[agent_message].append(message)

    result, output_messages = agent.run(st.session_state.agent_messages[agent_message])
    st.session_state.agent_messages[agent_message] = output_messages

    return result

def search_docs(department: str) -> str:
    """
    원하는 부서의 문서에 접근해서 정보를 가져오는 함수.

    Args:
        department: 문서를 찾길 원하는 부서. 종류는 "기획1팀", "기획2팀", "영업1팀", "영업2팀", "영업3팀", "경영1팀", "경영2팀", "경영3팀"이 있다.
    """

    docs_name = f"{department}_docs"

    if docs_name not in st.session_state.docs_dictionary:
        return "해당 문서는 존재하지 않음."
    
    output_docs = st.session_state.docs_dictionary[docs_name]

    return output_docs