# 부서별 Agent 페르소나 생성해주는 함수.
def create_persona(department: str, description: str) -> str:
    prompt = f"""너는 회사 내부에서 다양한 정보를 바탕으로 부서들끼리 소통시켜주는 Agent이다.
    현재 너가 속한 부서는 {department}이다.
    부서의 설명은 다음과 같다. '{description}' 
    너는 너가 가진 도구를 최대한 이용하여 사용자의 답변에 답한다."""

    system_prompt = {
        "role": "system",
        "content": prompt
    }

    return system_prompt