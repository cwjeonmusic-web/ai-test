import os
from google import genai

# 1. 클라이언트 설정
api_key = os.getenv("GEMINI_API_KEY")
client = genai.Client(api_key=api_key)

# 2. 분석할 코드
target_code = """
def login(user_id):
    # 취약한 코드 예시: SQL Injection
    query = "SELECT * FROM users WHERE id = '" + user_id + "'"
    db.execute(query)
"""

try:
    print("Gemini 1.5 Flash 모델로 보안 분석을 시작합니다...")
    
    # 3. 분석 요청 (최신 문법)
    response = client.models.generate_content(
        model="gemini-1.5-flash",
        contents=f"당신은 시니어 보안 컨설턴트입니다. 다음 코드의 취약점을 분석하고 보안 가이드를 작성하세요: {target_code}"
    )

    print("\n=== Gemini 보안 분석 결과 ===")
    print(response.text)

except Exception as e:
    print(f"분석 실패: {e}")
    exit(1)
