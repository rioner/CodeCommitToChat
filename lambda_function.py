# coding:utf-8
from json import dumps, loads
from botocore.vendored import requests

def lambda_handler(event, context):
    # チャット部屋のURL
    URL = "url"
    # 元データ
    message = ''
    # 加工データ
    body = ''

    # 更新内容の取得
    message = event['Records'][0]['Sns']['Message']
    before_rep = message.find('repository/')+11
    after_rep = message.find('/pull-request')
    before_link = message.find('https://ap')
    after_link = len(message)-1
    if 'created' in message:
        body = message[before_rep:after_rep] + ' リポジトリにプルリクエストを作成しました。\n'
        body = body + message[before_link:after_link]
    elif 'comment' in message:
        body = message[before_rep:after_rep] + ' リポジトリのプルリクエストにコメントしました。\n'
        body = body + message[before_link:after_link]
    elif 'merge' in message:
        body = message[before_rep:after_rep] + ' リポジトリのプルリクエストをマージしました。\n'
        body = body + message[before_link:after_link]
    elif 'closed' in message:
        body = message[before_rep:after_rep] + ' リポジトリのプルリクエストをクローズしました。\n'
        body = body + message[before_link:after_link]
    # 内容があればチャットする
    if body:
        message_headers = {'Content-Type': 'application/json; charset=UTF-8'}
        bot_message = {'text' : body}
        requests.post(
            URL,
            headers=message_headers,
            data=dumps(bot_message),
        )