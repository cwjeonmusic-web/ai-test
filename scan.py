import os
import google.generativeai as genai

# API 키 설정
api_key = os.getenv("GEMINI_API_KEY")
if not api_key:
    print("에러: GEMINI_API_KEY가 설정되지 않았습니다.")
    exit(1)

# API 설정 (버전을 명시적으로 지정하지 않고 기본 설정을 따름)
genai.configure(api_key=api_key)

try:
    # 1. 모델 설정 (가장 표준적인 'gemini-1.5-flash' 사용)
    # 만약 계속 안 된다면 'models/gemini-1.5-flash'로 시도합니다.
    model = genai.GenerativeModel('gemini-1.5-flash')

    # 2. 분석할 코드
    target_code = """
    def get_user_data(user_id):
        # 취약한 SQL 쿼리 예시
        query = f"SELECT * FROM users WHERE id = '{user_id}'"
        return db.execute(query)
    """

    prompt = f"""
    당신은 숙련된 보안 컨설턴트입니다. 
    다음 코드의 보안 취약점을 점검하고 보고서를 작성하세요.
    
    [분석할 코드]
    {target_code}
    """

    # 3. 분석 요청
    response = model.generate_content(prompt)
    
    print("=== Gemini 보안 분석 결과 ===")
    print(response.text)

except Exception as e:
    # 만약 404 에러가 나면 다른 모델명으로 한 번 더 시도
    print(f"기본 모델명 실패, 대안 모델명으로 시도 중... (에러내용: {e})")
    try:
        model = genai.GenerativeModel('models/gemini-1.5-flash')
        response = model.generate_content(prompt)
        print("=== Gemini 보안 분석 결과 (대안 모델) ===")
        print(response.text)
    except Exception as e2:
        print(f"최종 분석 실패: {e2}")
        exit(1)
