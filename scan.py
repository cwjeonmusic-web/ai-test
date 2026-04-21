import os
import google.generativeai as genai

# API 키 설정
api_key = os.getenv("GEMINI_API_KEY")
if not api_key:
    print("에러: GEMINI_API_KEY가 설정되지 않았습니다.")
    exit(1)

genai.configure(api_key=api_key)

# 모델 설정 (가장 기본 명칭 사용)
try:
    model = genai.GenerativeModel('gemini-1.5-flash')

    # 분석할 취약한 코드 예시
    target_code = """
    def login(user_id):
        query = "SELECT * FROM users WHERE id = '" + user_id + "'"
        db.execute(query)
    """

    prompt = f"""
    당신은 숙련된 보안 컨설턴트입니다. 
    다음 코드의 보안 취약점을 점검하고 보고서를 작성하세요.
    
    [분석할 코드]
    {target_code}
    """

    response = model.generate_content(prompt)
    print("=== Gemini 보안 분석 결과 ===")
    print(response.text)

except Exception as e:
    print(f"분석 중 에러 발생: {e}")
    exit(1)
