import torch
import re
import json
import streamlit as st
from transformers import AutoTokenizer, AutoModelForCausalLM


@st.cache_resource
def load_agent(checkpoint="K-intelligence/Midm-2.0-Mini-Instruct", _tools=[], _tool_repository={}):
    return Agent(checkpoint=checkpoint, tools=_tools, tool_repository=_tool_repository)

# 각 회사마다 Agent를 손쉽게 생성하기 위해 class 선언.
class Agent:
    def __init__(self, checkpoint="K-intelligence/Midm-2.0-Mini-Instruct", tools=[], tool_repository={}):
        self.checkpoint = checkpoint
        self.tool_repository = tool_repository

        print("tokenizer 생성중...")
        self.tokenizer = AutoTokenizer.from_pretrained(
            self.checkpoint, 
            )
        print("tokenizer 생성 완료✔")
        
        print("model 생성중...")
        self.model = AutoModelForCausalLM.from_pretrained(
            self.checkpoint, 
            dtype=torch.float16, 
            device_map="auto",
            low_cpu_mem_usage=True
            )
        print("model 생성 완료✔")

        if tools:
            self.tools = tools
        else:
            self.tools = []
        print("Agent 생성 완료!")

    # messages는 chat_template 형식으로 들어와야 함.
    def run(self, messages):
        print("답변 생성중...")
        inputs = self.tokenizer.apply_chat_template(messages, tools=self.tools, add_generation_prompt=True, return_dict=True, return_tensors="pt")
        model_outputs = self.model.generate(input_ids=inputs["input_ids"], attention_mask=inputs["attention_mask"], max_new_tokens=128)
        model_output = self.tokenizer.decode(model_outputs[0][len(inputs["input_ids"][0]):-1])
        print(model_output)
        # tool을 사용하기로 결정했는지 확인.
        tool_matches = re.findall(r"<tool_call>\s*(\{.*?\})\s*</tool_call>", model_output, re.DOTALL)

        return_values = []
        print(tool_matches)

        # tool을 사용했다면 그에 따른 로직.
        for tool_match in tool_matches:
            # tool 호출.
            tool_call_data = json.loads(tool_match)
            tool_name = tool_call_data.get("name")
            tool_arguments = tool_call_data.get("arguments")

            # tool이 repository에 존재한다면 도구 실행.
            if tool_name in self.tool_repository:
                try:
                    tool_result = self.tool_repository[tool_name](**tool_arguments)
                except Exception as e:
                    tool_result = f"Tool 실행 중 오류 발생: {e}"

                return_values.append(
                            {
                                "role": "tool",
                                "tool_name": tool_name,
                                "content": tool_result if tool_result else "값을 반환하지 않음"
                            }
                        )
            else: # 없으면 잘못된 tool을 호출했다고 판단.
                return_values.append(
                    {
                        "role": "tool",
                        "tool_name": tool_name,
                        "content": f"알 수 없는 tool: {tool_name}"
                    }
                )

        messages.extend(return_values)

        inputs = self.tokenizer.apply_chat_template(messages, add_generation_prompt=True, return_dict=True, return_tensors="pt")
        model_outputs = self.model.generate(input_ids=inputs["input_ids"], attention_mask=inputs["attention_mask"], max_new_tokens=128)

        model_output = self.tokenizer.decode(model_outputs[0][len(inputs["input_ids"][0]):-1])

        messages.append(
            {
                "role": "assistant",
                "content": model_output
            }
        )

        return model_output, messages