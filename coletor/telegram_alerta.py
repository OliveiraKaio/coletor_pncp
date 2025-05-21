import requests
import os

def notificar_telegram(mensagem):
    token = os.getenv("TELEGRAM_BOT_TOKEN")
    chat_id = os.getenv("TELEGRAM_CHAT_ID")
    if not token or not chat_id:
        print("[telegram] Token ou Chat ID ausente.")
        return

    url = f"https://api.telegram.org/bot{token}/sendMessage"
    data = {"chat_id": chat_id, "text": mensagem}
    
    try:
        requests.post(url, data=data, timeout=10)
    except Exception as e:
        print(f"[telegram] Falha ao notificar: {e}")
