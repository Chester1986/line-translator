from flask import Flask, request, jsonify
import requests

app = Flask(__name__)

# LibreTranslate API 설정 (무료 공개 서버)
LIBRETRANSLATE_URL = "https://libretranslate.com/translate"

# LINE Webhook 처리
@app.route("/callback", methods=["POST"])
def callback():
    data = request.json

    for event in data["events"]:
        if event["type"] == "message":
            user_message = event["message"]["text"]
            reply_token = event["replyToken"]

            # 한국어면 스페인(유럽) 스페인어로, 스페인어면 한국어로 번역
            if detect_language(user_message) == "ko":
                translated_text = translate_text(user_message, "ko", "es")
            else:
                translated_text = translate_text(user_message, "es", "ko")

            # 번역된 메시지를 LINE으로 보내기
            send_line_reply(reply_token, translated_text)

    return "OK", 200

# 번역 함수 (LibreTranslate API 호출)
def translate_text(text, source_lang, target_lang):
    payload = {
        "q": text,
        "source": source_lang,
        "target": target_lang,
        "format": "text"
    }
    response = requests.post(LIBRETRANSLATE_URL, json=payload)
    
    # 응답이 올바르게 왔는지 확인 후 번역 결과 반환
    if response.status_code == 200:
        return response.json().get("translatedText", "번역 실패!")
    else:
        return "번역 오류 발생!"

# 언어 감지 함수 (LibreTranslate 사용)
def detect_language(text):
    detect_url = "https://libretranslate.com/detect"
    response = requests.post(detect_url, json={"q": text})

    if response.status_code == 200 and response.json():
        return response.json()[0].get("language", "unknown")
    return "unknown"

# LINE 메시지 보내기 함수
def send_line_reply(reply_token, text):
    LINE_API_URL = "https://api.line.me/v2/bot/message/reply"
    LINE_ACCESS_TOKEN = "XbpI6t1buzzH0DKRlBegb5+qSmgFo5rURJGj0wAbIgrWVEJkkfoAc6dRstpPZL3y074mT4QRlPvXEZuY7C68HiotsoXKD2IHblpq4IYRA+6KoGEWOFppHnPeB01LLyupiT7rP9MZPToffl47lCl9mQdB04t89/1O/w1cDnyilFU="  # 네 LINE Access Token 입력!

    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {LINE_ACCESS_TOKEN}"
    }
    payload = {
        "replyToken": reply_token,
        "messages": [{"type": "text", "text": text}]
    }
    requests.post(LINE_API_URL, json=payload, headers=headers)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
