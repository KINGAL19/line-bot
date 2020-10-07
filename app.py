# SDK-software development kit
# flask 架設網站套件，Django用來做網頁套件

from flask import Flask, request, abort

from linebot import (
    LineBotApi, WebhookHandler
)
from linebot.exceptions import (
    InvalidSignatureError
)
from linebot.models import (
    MessageEvent, TextMessage, TextSendMessage,
)

app = Flask(__name__)

line_bot_api = LineBotApi('j1ZvY0U/x0vit5Q2P3P15MY8GANOKZ3nre5kZ7o1rMU0jGJoUWRztEddjlQfErUT02+Dgx9+QIUeU6dZ7wMUrAVzGpl/K2D+yCyKzunbf8Q7neC8LNzOABRq6bJAxqoDNNrjvRNaheM3S1iv/3kjXQdB04t89/1O/w1cDnyilFU=')
handler = WebhookHandler('c15858635eadb1d6587a8e8c0c79ad5b')


@app.route("/callback", methods=['POST'])
def callback():
    # get X-Line-Signature header value
    signature = request.headers['X-Line-Signature']

    # get request body as text
    body = request.get_data(as_text=True)
    app.logger.info("Request body: " + body)

    # handle webhook body
    try:
        handler.handle(body, signature)
    except InvalidSignatureError:
        print("Invalid signature. Please check your channel access token/channel secret.")
        abort(400)

    return 'OK'


@handler.add(MessageEvent, message=TextMessage)
def handle_message(event):
    line_bot_api.reply_message(
        event.reply_token,
        TextSendMessage(text=event.message.text))

# 如果地個程式是直接被執行，而不是被載入，才執行。
if __name__ == "__main__":
    app.run()