import os
import requests
import json

# 1. 설정
API_KEY = os.getenv("GEMINI_API_KEY")
# 모델 주소를 v1으로 고정하여 404 에러 방지
URL = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-1.5-flash:generateContent?key={API_KEY}"

def run_scan():
    # 분석할 파일 찾기
    files = [f for f in os.listdir('.') if f.endswith('.py') and f != 'scan.py']
    target_file = files[0] if files else 'scan.py'
    
    print(f"[{target_file}] 보안 분석 중...")
    
    with open(target_file, 'r', encoding='utf-8') as f:
        code = f.read()

    # 2. 제미나이에게 보낼 데이터
    payload = {
        "contents": [{
            "parts": [{
                "text": f"당신은 시니어 보안 컨설턴트입니다. 다음 코드의 취약점을 분석하고 수정 코드를 제안하세요:\n\n{code}"
            }]
        }]
    }

    # 3. 직접 요청 보내기
    response = requests.post(URL, json=payload)
    result = response.json()

    if response.status_code == 200:
        print(f"\n=== {target_file} 보안 분석 결과 ===")
        print(result['candidates'][0]['content']['parts'][0]['text'])
    else:
        print(f"분석 실패 (에러코드: {response.status_code})")
        print(json.dumps(result, indent=2, ensure_ascii=False))

if __name__ == "__main__":
    run_scan()
