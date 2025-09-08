import streamlit as st
from utils.tools import approach_agent, search_docs
from utils.companies import companies
import nest_asyncio

nest_asyncio.apply()

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

##### 변수 단순 초기화 #####
if "company" not in st.session_state:
    print("company 초기화 완료!")
    st.session_state.company = "Not Any"

if "agent_name" not in st.session_state:
    print("agent_name 초기화 완료!")
    st.session_state.agent_name = "Not Any"

if "agent_message" not in st.session_state:
    print("agent_message 초기화 완료!")
    st.session_state.agent_message = "Not Any"



# set_page_config default 값 설정.
st.set_page_config(
    initial_sidebar_state="collapsed",
    layout="wide",
    page_icon="😀",
    page_title="라우팅 네트워크 시스템"
)

# title
st.write("# 😀Routing Network System")

col1, col2 = st.columns(2)

prompt = st.chat_input("Say Something")

if prompt:
    agent = st.session_state.agent_dictionary[st.session_state.agent_name]

    print("prompt1")
    json_prompt = {
        "role": "user",
        "content": prompt
    }

    st.session_state.agent_messages[st.session_state.agent_message].append(json_prompt)
    print("prompt2")
    print(st.session_state.agent_messages[st.session_state.agent_message])
    output, messages = agent.run(st.session_state.agent_messages[st.session_state.agent_message])
    print("prompt3")
    # 새로운 chat template로 초기화
    st.session_state.agent_messages[st.session_state.agent_message] = messages

    print(output)
    print("###output###")

if st.session_state.agent_name in st.session_state.agent_dictionary:
    print("check1")
    for agent_message in st.session_state.agent_messages[st.session_state.agent_message]:
        print("check2")
        if agent_message["role"] == "assistant":
            with col1:
                st.write(agent_message["content"])
        elif agent_message["role"] == "user":
            with col2:
                st.write(agent_message["content"])

with st.sidebar:
    st.session_state.company = st.selectbox("**회사 선택**", companies)
    button = st.button("선택")
    if button:
        st.session_state.agent_name = f"{st.session_state.company}_agent"
        st.session_state.agent_message = f"{st.session_state.company}_message"

    if st.session_state.agent_name not in st.session_state.agent_dictionary:
        st.write("해당 회사의 Agent가 아직 존재하지 않습니다.😧")