import os
import requests
import json


# 1. 설정
API_KEY = os.getenv("GEMINI_API_KEY")
# v1beta 대신 v1을 사용하고, 모델 이름 형식을 바꿨습니다.
URL = f"https://generativelanguage.googleapis.com/v1/models/gemini-1.5-flash:generateContent?key={API_KEY}"

def run_scan():
    # 분석할 파일 찾기
    files = [f for f in os.listdir('.') if f.endswith('.py') and f != 'scan.py']
    target_file = files[0] if files else 'scan.py'
    
    print(f"[{target_file}] 보안 분석 시도 중 (v1 API)...")
    
    try:
        with open(target_file, 'r', encoding='utf-8') as f:
            code = f.read()

        payload = {
            "contents": [{
                "parts": [{
                    "text": f"당신은 보안 컨설턴트입니다. 다음 코드의 보안 취약점을 분석하세요:\n\n{code}"
                }]
            }]
        }

        # 2. 요청 전송
        response = requests.post(URL, json=payload)
        
        # 3. 404가 뜨면 v1beta로 한 번 더 자동 시도
        if response.status_code == 404:
            print("v1 실패, v1beta로 재시도 중...")
            alt_url = URL.replace("/v1/", "/v1beta/")
            response = requests.post(alt_url, json=payload)

        result = response.json()

        if response.status_code == 200:
            print(f"\n=== {target_file} 보안 분석 결과 ===")
            print(result['candidates'][0]['content']['parts'][0]['text'])
        else:
            print(f"최종 분석 실패 (에러코드: {response.status_code})")
            print(json.dumps(result, indent=2, ensure_ascii=False))

    except Exception as e:
        print(f"실행 중 오류 발생: {e}")

if __name__ == "__main__":
    run_scan()
