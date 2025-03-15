from flask import Flask, request, jsonify
import requests

app = Flask(__name__)

# LibreTranslate API 설정
LIBRETRANSLATE_URL = "https://libretranslate.com/translate"  # 공개 서버 URL

# LINE Webhook 처리
@app.route("/callback", methods=["POST"])
def callback():
    data = request.json

    # LINE에서 메시지가 왔을 때 처리
    for event in data["events"]:
        if event["type"] == "message":
            user_message = event["message"]["text"]
            reply_token = event["replyToken"]

            # LibreTranslate로 번역
            translated_text = translate_text(user_message, "ko", "es")

            # LINE에 번역된 메시지 보내기
            send_line_reply(reply_token, translated_text)

    return "OK", 200

# 번역 함수
def translate_text(text, source_lang, target_lang):
    payload = {
        "q": text,
        "source": source_lang,
        "target": target_lang,
        "format": "text"
    }
    response = requests.post(LIBRETRANSLATE_URL, json=payload)
    return response.json().get("translatedText", "번역 실패!")

# LINE 메시지 보내기
def send_line_reply(reply_token, text):
    LINE_API_URL = "https://api.line.me/v2/bot/message/reply"
    LINE_ACCESS_TOKEN = "XbpI6t1buzzH0DKRlBegb5+qSmgFo5rURJGj0wAbIgrWVEJkkfoAc6dRstpPZL3y074mT4QRlPvXEZuY7C68HiotsoXKD2IHblpq4IYRA+6KoGEWOFppHnPeB01LLyupiT7rP9MZPToffl47lCl9mQdB04t89/1O/w1cDnyilFU="  # 여기에 네가 받은 LINE 토큰 넣기

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
