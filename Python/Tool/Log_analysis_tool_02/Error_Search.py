# -*- coding: utf-8 -*-

import pandas as pd
import re
import datetime
import numpy as np
import configparser
import glob
import json
import pathlib

#変数
path_join = "," ; path = ""

path = pathlib.Path().absolute()   # test.pyのあるディレクトリ
path /= '../../../●●●●●●/'     # ディレクトリ移動

config_path = path_join.join(glob.glob(str(path) + "/config.ini"))

config_ini = configparser.ConfigParser()
config_ini.read(config_path)

config_list = json.loads(config_ini.get("セクション名", "キー"))

#エラー件数抽出関数
def Extraction(data, unit_name):
    global severe_one_unit,severe_two_unit,one_unit_severe_cnt,two_unit_severe_cnt,one_unit_exception_count,two_unit_exception_count
    if unit_name == "one_unit":
        one_unit_severe_cnt = len((data[data["c00"].str.contains("SEVERE", na=False)]))
        one_unit_exception_count = len((data[data["c00"].str.contains("exception",na=False,case=False)]))
         # + len((data[data["c01"].str.contains("exception",na=False,case=False)]))

        severe_one_unit = (data[data["c00"].str.contains("SEVERE", na=False)])

    elif unit_name == "two_unit":
        two_unit_severe_cnt = len((data[data["c00"].str.contains("SEVERE", na=False)]))

        word = (data.iat[0,0])
        if "This File wasn't found" in word:
            two_unit_exception_count = 0
        else:
            two_unit_exception_count = len((data[data["c00"].str.contains("exception",na=False,case=False)]))

        severe_two_unit = (data[data["c00"].str.contains("SEVERE", na=False)])

# リスト内index抽出関数
def func1(lst, value):
    return [i for i, x in enumerate(lst) if x == value]

#既知エラー or 新規エラー検索関数
def Error_Search(error_log_data, unit_name, overtime_service_log, service_time_log):
    match = [] #既知エラーログ件数
    notmatch = [] #新規エラーログ件数
    all = [] #エラーログ全件数
    
    for error_list in error_log_data:
        for num in range(len(config_list)):
            if re.match(config_list[num], error_list):
                match.append(num)
                all.append(1)
            else:
                continue
            break

        else:
            notmatch.append(1)
            all.append(0)
    if "one_unit" in unit_name:
        print("・全件数：" + str(len(all)) + "件(「SEVERE」で検索) ★\n" +
              "・全件数：" + str(one_unit_exception_count) + "件(「Exception」で検索) ★\n\n" +
              "・時間外ログ件数：" + str(len(overtime_service_log)) + "件\n" +
              "・時間内ログ件数：" + str(len(service_time_log)) + "件 ★\n")

    elif "two_unit" in unit_name:
        print("・全件数：" + str(len(all)) + "件(「SEVERE」で検索) ★\n" +
              "・全件数：" + str(two_unit_exception_count) + "件(「Exception」で検索) ★\n\n" +
              "・時間外ログ件数：" + str(len(overtime_service_log)) + "件\n" +
              "・時間内ログ件数：" + str(len(service_time_log)) + "件 ★\n")

    # print("※日次報告の件数と比較してください。大幅に異なる場合「2.全件数」と比較してください。\n")

    if unit_name not in "SEVERE":
        if len(match) > 0:
            print("　(1)一致:" + str(len(match)) + "件" + "\n")

        elif len(match) == 0:
            print("　(1)既知エラーログ無し\n")

# 一致したエラー(番号)があった場合、件数と影響度をPrint
    for num in range(len(config_list)):
        if num in match:
            print("　　・" + str(match.count(num)) + "件(" + (config_list[num].replace(".*","") + "：サービス影響無し)"))

# 不一致の件数が0じゃない場合、件数とGrepした際の行数をPrint
    if len(notmatch) > 0:
        print("\n　(2)不一致:" + str(len(notmatch)) + "件")
        idx = func1(all,0) #all(List)内で0と一致するIndex抽出
        idx = map(lambda x: x+1, idx) #抽出したIndexに+1
        print("\n　　・" + path_join.join(map(str,idx)) + "行目にエラーが発生しています。ログを確認してください。\n")

    elif len(notmatch) == 0:
        print("\n　(2)新規エラーログ無し\n")
