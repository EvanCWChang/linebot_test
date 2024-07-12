from flask import Flask, request, abort

from linebot import (
    LineBotApi, WebhookHandler
)
from linebot.exceptions import (
    InvalidSignatureError
)
from linebot.models import *

#======python的函數庫==========
import tempfile, os
import datetime
import openai
import time
import traceback
#======python的函數庫==========

app = Flask(__name__)
static_tmp_path = os.path.join(os.path.dirname(__file__), 'static', 'tmp')
# Channel Access Token
line_bot_api = LineBotApi(os.getenv('CHANNEL_ACCESS_TOKEN'))
# Channel Secret
handler = WebhookHandler(os.getenv('CHANNEL_SECRET'))
# OPENAI API Key初始化設定
openai.api_key = os.getenv('OPENAI_API_KEY')

# 首先，安裝必要的模組
!pip install requests

# 匯入需要的模組
import datetime
import requests

# 星座與日期對應
zodiac_signs = {
    "摩羯座": {"start_date": (12, 22), "end_date": (1, 19), "traits": "負責任、紀律嚴明、有自制力、善於管理"},
    "水瓶座": {"start_date": (1, 20), "end_date": (2, 18), "traits": "進步、獨創、獨立、人道主義"},
    "雙魚座": {"start_date": (2, 19), "end_date": (3, 20), "traits": "有同情心、藝術性、直覺性、溫柔、智慧、音樂天賦"},
    "牡羊座": {"start_date": (3, 21), "end_date": (4, 19), "traits": "勇敢、堅定、自信、熱情、樂觀、誠實、熱情"},
    "金牛座": {"start_date": (4, 20), "end_date": (5, 20), "traits": "可靠、有耐心、實際、奉獻、負責任、穩定"},
    "雙子座": {"start_date": (5, 21), "end_date": (6, 20), "traits": "溫柔、親切、好奇、適應力強、學習迅速、善於交流"},
    "巨蟹座": {"start_date": (6, 21), "end_date": (7, 22), "traits": "堅韌、想像力豐富、忠誠、情感豐富、同情心、說服力"},
    "獅子座": {"start_date": (7, 23), "end_date": (8, 22), "traits": "創造力、熱情、大方、善良、幽默"},
    "處女座": {"start_date": (8, 23), "end_date": (9, 22), "traits": "忠誠、分析能力強、仁慈、勤勉、實際"},
    "天秤座": {"start_date": (9, 23), "end_date": (10, 22), "traits": "合作、公正、和善、優雅、公平、社交能力強"},
    "天蠍座": {"start_date": (10, 23), "end_date": (11, 21), "traits": "機智、勇敢、充滿激情、頑強、真誠"},
    "射手座": {"start_date": (11, 22), "end_date": (12, 21), "traits": "慷慨、理想主義、幽默感強"}
}

def get_zodiac_sign(month, day):
    for sign, data in zodiac_signs.items():
        start_date = datetime.date(2020, data["start_date"][0], data["start_date"][1])
        end_date = datetime.date(2020, data["end_date"][0], data["end_date"][1])
        date = datetime.date(2020, month, day)

        # Handle Capricorn separately due to year change
        if sign == "摩羯座":
            if (date >= start_date and date <= datetime.date(2020, 12, 31)) or (date >= datetime.date(2020, 1, 1) and date <= end_date):
                return sign, data["traits"]
        else:
            if start_date <= date <= end_date:
                return sign, data["traits"]
    return None, None

def get_daily_horoscope(sign):
    try:
        url = f"https://ohmanda.com/api/horoscope/{sign.lower()}/"
        response = requests.get(url)
        if response.status_code == 200:
            horoscope = response.json().get("horoscope")
            return horoscope
        else:
            return "無法獲取今日運勢"
    except:
        return "無法獲取今日運勢"

# 獲取用戶輸入的日期
user_input = input("請輸入生日（MM/DD）：")
month, day = map(int, user_input.split('/'))

# 獲取星座及個性
zodiac_sign, traits = get_zodiac_sign(month, day)

# 獲取今日星座運勢
if zodiac_sign:
    horoscope = get_daily_horoscope(zodiac_sign)
    print(f"你的星座是：{zodiac_sign}")
    print(f"個性特徵：{traits}")
    print(f"今日運勢：{horoscope}")
else:
    print("無法辨識您的星座，請確認輸入格式是否正確。")
