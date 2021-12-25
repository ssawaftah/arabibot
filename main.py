# Copyright 2021 TerminalWarlord under the terms of the MIT
# license found at https://github.com/TerminalWarlord/TikTok-Downloader-Bot/blob/master/LICENSE
# Encoding = 'utf-8'
# Fork and Deploy, do not modify this repo and claim it yours
# For collaboration mail me at dev.jaybee@gmail.com
from pyrogram import Client, filters
from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton, InlineQueryResultArticle, InputTextMessageContent
import shutil
import requests
import json
import os
import re
from bs4 import BeautifulSoup as bs
import time
from datetime import timedelta
import math
import base64
from progress_bar import progress, TimeFormatter, humanbytes
from dotenv import load_dotenv

load_dotenv()
bot_token = os.environ.get('BOT_TOKEN')
workers = int(os.environ.get('WORKERS'))
api = int(os.environ.get('API_KEY'))
hash = os.environ.get('API_HASH')
chnnl = os.environ.get('CHANNEL_URL')
BOT_URL = os.environ.get('BOT_URL')
app = Client("JayBee", bot_token=bot_token, api_id=api, api_hash=hash, workers=workers)



@app.on_message(filters.command('start'))
def start(client, message):
    kb = [[InlineKeyboardButton('موقع عربي بلس', url=chnnl),InlineKeyboardButton('اتصل بنا', url="https://t.me/s_awaftah")]]
    reply_markup = InlineKeyboardMarkup(kb)
    app.send_message(chat_id=message.from_user.id, text=f"مرحبا بكم في بوت تحميل مقاطع تيك توك ، يمكنكم تحميل مقاطع تيك توك عبر ارسال رابط الفيديو فقط وسيقوم البوت بجلب الفيديو لك\n\n "       
                           "تابع المطور على انستغرام :https://instagram.com/s_awaftah",
                     parse_mode='md',
                     reply_markup=reply_markup)




@app.on_message(filters.command('help'))
def help(client, message):
    kb = [[InlineKeyboardButton('Channel 🛡', url=chnnl),InlineKeyboardButton('Repo 🔰', url="https://www.arabi-plus.com")]]
    reply_markup = InlineKeyboardMarkup(kb)
    app.send_message(chat_id=message.from_user.id, text=f"مرحبا بكم في بوت تحميل مقاطع تيك توك ، يمكنكم تحميل مقاطع تيك توك عبر ارسال رابط الفيديو فقط وسيقوم البوت بجلب الفيديو لك\n\n"
                                            "__ارسل لي رابط مقطع التيك توك لاقوم بتحميلة__",
                     parse_mode='md',
                     reply_markup=reply_markup)


@app.on_message((filters.regex("http://")|filters.regex("https://")) & (filters.regex('tiktok')|filters.regex('douyin')))
def tiktok_dl(client, message):
    a = app.send_message(chat_id=message.chat.id,
                         text='__Downloading File to the Server__',
                         parse_mode='md')
    link = re.findall(r'\bhttps?://.*[(tiktok|douyin)]\S+', message.text)[0]
    link = link.split("?")[0]



    
    params = {
      "link": link
    }
    headers = {
      'x-rapidapi-host': "tiktok-info.p.rapidapi.com",
      'x-rapidapi-key': "f9d65af755msh3c8cac23b52a5eep108a33jsnbf7de971bb72"
    }
    
    ### Get your Free TikTok API from https://rapidapi.com/TerminalWarlord/api/tiktok-info/
    #Using the default one can stop working any moment 
    
    api = f"https://tiktok-info.p.rapidapi.com/dl/"
    r = requests.get(api, params=params, headers=headers).json()['videoLinks']['download']
    directory = str(round(time.time()))
    filename = str(int(time.time()))+'.mp4'
    size = int(requests.head(r).headers['Content-length'])
    total_size = "{:.2f}".format(int(size) / 1048576)
    try:
        os.mkdir(directory)
    except:
        pass
    with requests.get(r, timeout=(50, 10000), stream=True) as r:
        r.raise_for_status()
        with open(f'./{directory}/{filename}', 'wb') as f:
            chunk_size = 1048576
            dl = 0
            show = 1
            for chunk in r.iter_content(chunk_size=chunk_size):
                f.write(chunk)
                dl = dl + chunk_size
                percent = round(dl * 100 / size)
                if percent > 100:
                    percent = 100
                if show == 1:
                    
        app.send_document(chat_id=message.chat.id,
                          document=f"./{directory}/{filename}",
                          caption=f"\n\n"
                          f"تابع المطور على انستغرام : https://instagram.com/s_awaftah",
                          file_name=f"{directory}",
                          parse_mode='md',
                          progress=progress,
                          progress_args=(a, start, title))
        a.delete()
        try:
            shutil.rmtree(directory)
        except:
            pass


app.run()
