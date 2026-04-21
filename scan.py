import os
import google.generativeai as genai

# 1. API 키 설정
api_key = os.getenv("GEMINI_API_KEY")
genai.configure(api_key=api_key)

# 2. 모델 설정 (에러 방지를 위해 확실한 명칭인 'gemini-1.5-flash-latest' 사용)
model = genai.GenerativeModel('gemini-1.5-flash-latest')

# 3. 분석할 코드
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
