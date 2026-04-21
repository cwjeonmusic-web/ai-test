import os
import sys
from google import genai

api_key = os.getenv("GEMINI_API_KEY")
client = genai.Client(api_key=api_key)

def run_scan():
    # 분석할 파일 찾기
    files_to_scan = [f for f in os.listdir('.') if f.endswith('.py') and f != 'scan.py']
    if not files_to_scan:
        files_to_scan = ['scan.py']

    # 시도해볼 모델 명칭 후보군 (404 에러 방지용)
    model_variants = [
        "gemini-1.5-flash",          # 기본
        "models/gemini-1.5-flash",   # 전체 경로
        "gemini-1.5-flash-latest",   # 최신 태그
        "gemini-pro"                 # 하위 호환용
    ]

    for target_file in files_to_scan:
        print(f"\n--- [{target_file}] 분석 시작 ---")
        try:
            with open(target_file, 'r', encoding='utf-8') as f:
                code_content = f.read()

            success = False
            for model_name in model_variants:
                try:
                    print(f"[{model_name}] 모델로 시도 중...")
                    response = client.models.generate_content(
                        model=model_name,
                        contents=f"시니어 보안 컨설턴트로서 다음 코드의 취약점을 분석해줘:\n\n{code_content}"
                    )
                    print(f"=== {target_file} 분석 성공 ({model_name}) ===")
                    print(response.text)
                    success = True
                    break # 성공하면 다음 파일로
                except Exception as e:
                    if "404" in str(e):
                        continue # 404면 다음 모델명 시도
                    else:
                        print(f"오류 발생: {e}")
                        break
            
            if not success:
                print(f"[{target_file}] 모든 모델 명칭 시도 실패 (404 등)")

        except Exception as e:
            print(f"파일 읽기 오류: {e}")

if __name__ == "__main__":
    run_scan()
