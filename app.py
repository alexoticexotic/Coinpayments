from flask import Flask, request
import hmac
import hashlib
import requests

app = Flask(__name__)

TELEGRAM_BOT_TOKEN = '8129372019:AAFP33Rzl6taohTdpmogME-DZETwK3RV1Nc'
TELEGRAM_CHAT_ID = '226453434'
IPN_SECRET = 'МояЛюбимаяКошечкаК'  # тот самый, что у тебя в CoinPayments

def send_telegram_message(message):
    url = f"https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}/sendMessage"
    payload = {"chat_id": TELEGRAM_CHAT_ID, "text": message}
    requests.post(url, data=payload)

@app.route("/ipn", methods=["POST"])
def ipn():
    raw_data = request.get_data()
    received_hmac = request.headers.get('HMAC')
    calculated_hmac = hmac.new(IPN_SECRET.encode(), raw_data, hashlib.sha512).hexdigest()

    if received_hmac != calculated_hmac:
        return "Invalid HMAC", 403

    data = request.form
    status = int(data.get('status', 0))

    if status >= 100 or status == 2:
        amount = data.get('amount1')
        currency = data.get('currency1')
        buyer_email = data.get('email', 'неизвестно')
        message = f"Поступил платёж: {amount} {currency}\nEmail: {buyer_email}"
        send_telegram_message(message)

    return "OK", 200
import os

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)

