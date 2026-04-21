import os
import sys
from google import genai

api_key = os.getenv("GEMINI_API_KEY")
client = genai.Client(api_key=api_key)

def run_scan():
    # 분석할 대상: 이 리포지토리에 있는 모든 .py 파일을 찾아 읽습니다.
    # (본인이 만든 다른 파일이 있다면 그걸 읽게 됩니다.)
    files_to_scan = [f for f in os.listdir('.') if f.endswith('.py') and f != 'scan.py']
    
    if not files_to_scan:
        # 만약 다른 파일이 없다면, 아쉬운 대로 자기 자신(scan.py)이라도 분석해봅니다.
        files_to_scan = ['scan.py']

    for target_file in files_to_scan:
        with open(target_file, 'r', encoding='utf-8') as f:
            code_content = f.read()

        try:
            print(f"[{target_file}] 분석 시도 중...")
            # 모델 명칭에서 'models/'를 빼고 시도 (새 라이브러리 표준)
            response = client.models.generate_content(
                model="gemini-1.5-flash",
                contents=f"시니어 보안 컨설턴트로서 다음 코드의 취약점을 분석해줘:\n\n{code_content}"
            )
            print(f"\n=== {target_file} 보안 분석 결과 ===")
            print(response.text)
        except Exception as e:
            print(f"에러 발생: {e}")

if __name__ == "__main__":
    run_scan()
