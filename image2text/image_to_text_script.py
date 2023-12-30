import base64
import cv2
import openai
import os
import time
from datetime import datetime, timedelta
import numpy as np
from dotenv import load_dotenv

# .envファイルの内容を読み込見込む
load_dotenv()

# 画像フォルダの指定
image_folder = "../VideoCapture/frame"

# 現在時刻から15秒前の時刻を取得
time_threshold = datetime.now() - timedelta(seconds=15)

# base64にエンコードされた画像のリスト
base64Images = []

# 過去15秒間の画像を読み込む
for i in range(15):  # 1〜15の画像をチェック
  image_path = os.path.join(image_folder, f"saved_frame_{i}.jpg")
  print(image_path)
  if os.path.exists(image_path):
    image = cv2.imread(image_path)
    image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)  # BGRからRGBに変換
    is_success, im_buf_arr = cv2.imencode(".png", image)  # 画像をPNG形式に変換
    byte_im = im_buf_arr.tobytes()
    base64Images.append(base64.b64encode(byte_im).decode("utf-8"))

# GPT-4ビジョンモデルへのプロンプト
PROMPT_CONTENT = """
画像の内容を読み取って、何が写っているのか説明してください。256トークンのため途中で切れないように注意してください。
"""

PROMPT_MESSAGES = [
    {
        "role": "user",
        "content": [
            PROMPT_CONTENT,
            *map(lambda x: {"image": x}, base64Images),
        ],
    },
]

params = {
    "model": "gpt-4-vision-preview",
    "messages": PROMPT_MESSAGES,
    "api_key": os.environ['API_KEY'],
    "headers": {"Openai-Version": "2020-11-07"},
    "max_tokens": 256,
}

# OpenAI APIにリクエストを送信
result = openai.ChatCompletion.create(**params)
print(result.choices[0].message.content)