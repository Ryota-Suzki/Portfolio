# HTTP通信を行うための標準ライブラリ
import urllib.request
import requests
import base64
import configparser
import pathlib
import glob
import json
from datetime import datetime, date, timedelta
import os

path_join = ""

path = pathlib.Path().absolute()   # test.pyのあるディレクトリ
path /= 'conf/'     # ディレクトリ移動

#設定ファイル関連
config_path = path_join.join(glob.glob(str(path) + "/config.ini"))
config_ini = configparser.ConfigParser()
config_ini.read(config_path)

user = config_ini["xxxxxxx"]["xxxxx"] # WebDAVユーザー名
password = config_ini["xxxxxxx"]["xxxxx"] # WebDAVパスワード
conf_get_url = (config_ini.get("xxxx","xxx",raw=True)) #%を読み込むため「raw=True」
file_list = json.loads(config_ini.get("xxxxx","xxxx")) #ファイル名のリスト取得

# 日付変数
d_today = datetime.today() #今日の日付
d_yesterday = d_today - timedelta(days=1) #前日
webdav_folder = datetime.strftime(d_today,"%Y%m%d") #WebDAVフォルダ名
local_folder = (datetime.strftime(d_yesterday,"%Y%m%d")) #ローカルフォルダ名

try:
    os.makedirs(local_folder)
except:
    pass

# 送信先のURL
for num in range(len(file_list)):

    if "xxxxx" in file_list[num]:
        file_path = file_list[num] + datetime.strftime(d_yesterday,"%Y-%m-%d") + ".zip"

    elif  "xxxxx" in file_list[num]:
        file_path = file_list[num] + datetime.strftime(d_yesterday,"%Y%m%d") + ".gz"

    print("ダウンロード済:" + file_path)

    url = conf_get_url.format(datetime.strftime(d_yesterday,"%Y"),datetime.strftime(d_yesterday,"%Y-%m"),webdav_folder,file_path)

    # Basic認証用の文字列を作成.
    basic = base64.b64encode('{}:{}'.format(user, password).encode('utf-8'))

    # Basic認証付きの、GETリクエストを作成する.
    request = urllib.request.Request(url,headers={"Authorization": "Basic " + basic.decode('utf-8')})

    save_name = local_folder +"/" + file_path

    # 送信して、レスポンスを受け取る.
    try:
        with urllib.request.urlopen(request) as web_file:
            data = web_file.read()
            with open(save_name, mode='wb') as local_file:
                local_file.write(data)
    except urllib.error.URLError as e:
            print(e)
