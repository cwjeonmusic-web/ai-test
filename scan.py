import os
import sys

# 1. 라이브러리 설치 확인 및 불러오기
try:
    from google import genai
except ImportError:
    print("에러: google-genai 라이브러리가 설치되지 않았습니다.")
    sys.exit(1)

# 2. API 키 확인 (디버깅용)
api_key = os.getenv("GEMINI_API_KEY")
if not api_key:
    print("에러: GEMINI_API_KEY 환경 변수를 찾을 수 없습니다. Secrets 설정을 확인하세요.")
    sys.exit(1)
else:
    print(f"API 키 확인 완료 (앞글자 4자리): {api_key[:4]}****")

# 3. 클라이언트 실행 및 분석
try:
    client = genai.Client(api_key=api_key)
    
    response = client.models.generate_content(
        model="gemini-1.5-flash",
        contents="보안 컨설턴트로서 다음 코드의 취약점을 한 문장으로 분석해줘: query = 'SELECT * FROM users WHERE id=' + user_id"
    )

    print("\n=== Gemini 보안 분석 결과 ===")
    print(response.text)

except Exception as e:
    print(f"\n[분석 중 상세 에러 발생]: {str(e)}")
    sys.exit(1)
