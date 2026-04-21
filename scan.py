import os
import requests
import json

# 설정
API_KEY = os.getenv("GEMINI_API_KEY")
GITHUB_TOKEN = os.getenv("GITHUB_TOKEN")
PR_NUMBER = os.getenv("PR_NUMBER")
REPO = os.getenv("REPO")

GEMINI_URL = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-3-flash-preview:generateContent?key={API_KEY}"

def post_github_comment(content):
    if not PR_NUMBER:
        print("PR 환경이 아니므로 댓글을 남기지 않습니다.")
        return

    url = f"https://api.github.com/repos/{REPO}/issues/{PR_NUMBER}/comments"
    headers = {
        "Authorization": f"token {GITHUB_TOKEN}",
        "Accept": "application/vnd.github.v3+json"
    }
    data = {"body": f"### 🤖 Gemini AI 보안 분석 리포트\n\n{content}"}
    
    response = requests.post(url, headers=headers, json=data)
    if response.status_code == 201:
        print("✅ GitHub PR에 성공적으로 댓글을 남겼습니다.")
    else:
        print(f"❌ 댓글 작성 실패: {response.status_code}")
        print(response.text)

def run_scan():
    # 분석할 파일 찾기
    files = [f for f in os.listdir('.') if f.endswith('.py') and f != 'scan.py']
    target_file = files[0] if files else 'scan.py'
    
    print(f"[{target_file}] 보안 분석 시작...")
    
    try:
        with open(target_file, 'r', encoding='utf-8') as f:
            code = f.read()

        payload = {
            "contents": [{
                "parts": [{"text": f"당신은 전문 보안 컨설턴트입니다. 다음 코드의 보안 취약점을 분석하고 수정안을 마크다운 형식으로 제시하세요:\n\n{code}"}]
            }]
        }

        response = requests.post(GEMINI_URL, json=payload)
        result = response.json()

        if response.status_code == 200:
            analysis_text = result['candidates'][0]['content']['parts'][0]['text']
            print("\n--- 분석 완료 ---")
            print(analysis_text)
            
            # 분석 결과를 댓글로 남기기
            post_github_comment(analysis_text)
        else:
            print(f"❌ 분석 실패: {response.status_code}")

    except Exception as e:
        print(f"⚠️ 오류 발생: {e}")

if __name__ == "__main__":
    run_scan()
