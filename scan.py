import os
import requests
import json

# 1. 설정
API_KEY = os.getenv("GEMINI_API_KEY")
# 새 프로젝트 키에 가장 적합한 v1beta 경로입니다.
URL = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-1.5-flash:generateContent?key={API_KEY}"

def run_scan():
    # 분석할 파일 찾기 (vulnerable_test.py가 있다면 그걸 우선적으로 분석)
    files = [f for f in os.listdir('.') if f.endswith('.py') and f != 'scan.py']
    target_file = files[0] if files else 'scan.py'
    
    print(f"[{target_file}] 보안 분석 시작 (새 API 키 사용)...")
    
    try:
        with open(target_file, 'r', encoding='utf-8') as f:
            code = f.read()

        payload = {
            "contents": [{
                "parts": [{
                    "text": f"당신은 시니어 보안 컨설턴트입니다. 다음 파이썬 코드의 보안 취약점을 분석하고 개선안을 제시하세요:\n\n{code}"
                }]
            }]
        }

        # 2. 제미나이 서버에 요청
        response = requests.post(URL, json=payload)
        result = response.json()

        if response.status_code == 200:
            print(f"\n✅ 분석 성공! (대상: {target_file})")
            print("-" * 50)
            print(result['candidates'][0]['content']['parts'][0]['text'])
            print("-" * 50)
        else:
            print(f"❌ 분석 실패 (에러코드: {response.status_code})")
            print(json.dumps(result, indent=2, ensure_ascii=False))

    except Exception as e:
        print(f"⚠️ 실행 중 오류 발생: {e}")

if __name__ == "__main__":
    run_scan()
