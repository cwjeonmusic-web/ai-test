import os
from google import genai

# 1. 클라이언트 설정
api_key = os.getenv("GEMINI_API_KEY")
client = genai.Client(api_key=api_key)

try:
    # 2. 분석 요청
    response = client.models.generate_content(
        model="gemini-1.5-flash",
        contents="보안 분석을 시작합니다. 아래 코드의 SQL 인젝션 취약점을 찾아주세요: def login(id): query = f'SELECT * FROM users WHERE id={id}'"
    )

    print("=== Gemini 보안 분석 결과 ===")
    print(response.text)

except Exception as e:
    print(f"분석 실패: {e}")
    exit(1)
