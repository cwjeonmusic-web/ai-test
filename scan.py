import os
import google.generativeai as genai

api_key = os.getenv("GEMINI_API_KEY")
genai.configure(api_key=api_key)

# 시도해볼 모델 리스트 (가장 성공 확률 높은 순)
models_to_try = ['gemini-1.5-flash', 'gemini-1.5-flash-latest', 'gemini-pro']

target_code = """
def login(user_id):
    query = "SELECT * FROM users WHERE id = '" + user_id + "'"
    db.execute(query)
"""

success = False
for model_name in models_to_try:
    try:
        print(f"{model_name} 모델로 분석 시도 중...")
        model = genai.GenerativeModel(model_name)
        response = model.generate_content(f"보안 컨설턴트로서 다음 코드 분석해줘: {target_code}")
        
        print(f"\n=== {model_name} 분석 결과 ===")
        print(response.text)
        success = True
        break 
    except Exception as e:
        print(f"{model_name} 실패: {e}")

if not success:
    print("\n[최종 에러] 모든 모델 호출에 실패했습니다. API 키의 프로젝트 권한을 확인해주세요.")
    exit(1)
