import os, requests

def send_telegram(text, image_url=None):
    token = os.getenv("BOT_TOKEN")
    chat_id = os.getenv("CHAT_ID")
    url = f"https://api.telegram.org/bot{token}"
    if image_url:
        img = requests.get(image_url, stream=True).raw
        requests.post(f"{url}/sendPhoto", data={"chat_id": chat_id, "caption": text}, files={"photo": img})
    else:
        requests.post(f"{url}/sendMessage", data={"chat_id": chat_id, "text": text})

def translate(text):
    try:
        url = "https://translate.googleapis.com/translate_a/single?client=gtx&sl=en&tl=ko&dt=t&q=" + requests.utils.quote(text)
        r = requests.get(url)
        result = r.json()[0][0][0]
        return result
    except:
        return "[번역 실패]"
