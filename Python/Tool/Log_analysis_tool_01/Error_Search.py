# -*- coding: utf-8 -*-

import re
import pandas as pd
import configparser
import glob
import pathlib
import json

# 変数
Path_join = ","; path = "";

path = pathlib.Path().absolute()   # test.pyのあるディレクトリ
path /= '../../../●●●●●●/'     # ディレクトリ移動

config_path = (glob.glob(str(path) + "/config.ini"))

config_ini = configparser.ConfigParser()
config_ini.read(config_path)

config_list = json.loads(config_ini.get("セクション名", "キー")) #エラーログ検索のため、キーには正規表現を含んだリストを指定(例:.*エラーログ.*)

# リスト内index抽出関数
def func1(lst, value): #新規エラーログがどの行数に記載されているか判定用
    return [i for i, x in enumerate(lst) if x == value]

# エラー件数抽出関数

def error_search(File):　#File:サーバーエラーログ
    deadlock = []      #デッドロック
    match = []         #既知エラーログ
    notmatch = []      #新規エラーログ
    all = []           #全エラーログ

    for error_list in File:
        for num in range(len(config_list)):
            if re.match(config_list[num], error_list):

                if "デッドロック" in config_list[num]:
                    deadlock.append(num)
                    all.append(1) #全件数に"1"を格納

                elif "デッドロック" not in config_list[num]:
                    match.append(num)
                    all.append(1) #全件数に"1"を格納
            else:
                continue
            break

        else:
            notmatch.append(1) #不一致件数に"1"を格納
            all.append(0) # #全件数に"0"を格納

    print("1.全件数：" + str(len(all) - len(deadlock)) + "件(日次報告件数と比較してください)\n")

    if len(match) > 0:
        print("　(1)一致：" + str(len(match)) + "件")

    elif len(match) == 0:
        print("　(1)既知エラーログ無")

    else:
        print("")

    for num in range(len(config_list)):
        if num in match:
            print("　　・" + str(match.count(num)) + "件(" + (config_list[num].replace(".*","") + "：サービス影響無し)")) #config.iniのリストの文字列:サービス影響無し

    if len(notmatch) > 0:
        idx = func1(all,0) #エラーログ全件数内の"0"を検索しindexを抽出
        idx = map(lambda x: x+1, idx) #抽出したIndexに +1
        print("　(2)不一致：" + str(len(notmatch)) + "件")
        print("　　・" + Path_join.join(map(str,idx)) + "行目に新規エラーが発生しています。ログを確認してください。\n")

    else:
        print("　(2)新規エラーログ無\n")

    if len(deadlock) > 0:
        print("　(3)デッドロック:" + str(len(deadlock)) + "件")

    else:
        print("　(3)デッドロック発生無")
