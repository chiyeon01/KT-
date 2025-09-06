import streamlit as st
from utils.tools import approach_agent, search_docs
from utils.departments import departments

# 부서의 agent를 저장하는 session_state
if "agent_dictionary" not in st.session_state:
    print("agent_dictionary 초기화 완료!")
    st.session_state.agent_dictionary = {}

# 부서 agent마다의 message를 저장하는 session_state
if "agent_messages" not in st.session_state:
    print("agent_messages 초기화 완료!")
    st.session_state.agent_messages = {}

# 부서별 documentary를 저장하는 session_state
if "docs_dictionary" not in st.session_state:
    print("docs_dictionary 초기화 완료!")
    st.session_state.docs_dictionary = {}

# agent가 사용할 tools
if "tools" not in st.session_state:
    print("tools 초기화 완료!")
    st.session_state.tools = [approach_agent, search_docs]

# tools 종류
if "tool_repository" not in st.session_state:
    print("tool_repository 초기화 완료!")
    st.session_state.tool_repository = {
        "approach_agent": approach_agent,
        "search_docs": search_docs,
    }



st.set_page_config(
    initial_sidebar_state="collapsed",
    layout="wide",
    page_icon="😀",
    page_title="라우팅 네트워크 시스템"
)

st.write("# 😀Routing Network System")

with st.sidebar:
    department = st.selectbox("**부서 선택**", departments)
    agent_name = f"{department}_agent"
    agent_message = f"{department}_agent"

    if agent_name not in st.session_state.agent_dictionary:
        st.write("해당 부서의 Agent가 아직 존재하지 않습니다.😧")
    else:
        agent = st.session_state.agent_dictionary[agent_name]
        prompt = st.chat_input("Say Something")
        if prompt:
            json_prompt = {
                "role": "user",
                "content": prompt
            }

            st.session_state.agent_messages[agent_message].append(json_prompt)

            output, messages = agent.run(st.session_state.agent_messages)

            st.write(output)