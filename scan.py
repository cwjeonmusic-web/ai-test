import os
import google.generativeai as genai

# 1. API 키 설정
api_key = os.getenv("GEMINI_API_KEY")
genai.configure(api_key=api_key)

# 2. 모델 설정 (Gemini 1.5 Flash가 빠르고 무료 효율이 좋습니다)
model = genai.GenerativeModel('gemini-1.5-flash')

# 3. 분석할 코드 (나중에는 실제 PR 코드를 가져오게 바꿀 겁니다)
target_code = """
def delete_user(user_id):
    query = f"DELETE FROM users WHERE id = '{user_id}'"
    db.execute(query)
"""

# 4. 분석 요청
prompt = f"""
너는 시니어 보안 컨설턴트야. 
아래 코드의 취약점을 분석하고, 취약점 명칭, 위험도, 공격 시나리오, 그리고 보안 가이드가 반영된 안전한 코드를 작성해줘.

분석할 코드:
{target_code}
"""

response = model.generate_content(prompt)

print("=== Gemini 보안 분석 결과 ===")
print(response.text)
