# -*- coding: utf-8 -*-

import Error_Search as Search #作成モジュール
import Excel_Write as Write #作成モジュール
import Count
import Check #作成モジュール

import codecs
import glob
import pandas as pd
import openpyxl as op
from openpyxl import Workbook, load_workbook
from pathlib import Path
import datetime
import re
import os

Check.writeTxt       #●●●●●●/●●●●●●が存在しない場合

# 変数
path_join = ","; path = ""

# PATH取得
one_unit_file_path = path_join.join(glob.glob("●●●●●●*/●●●●●●*")) #パス名伏字
two_unit_file_path = path_join.join(glob.glob("●●●●●●*/●●●●●●*")) #パス名伏字

#ファイル作成日 & 作成年
file_creation_date = datetime.datetime.strptime(path_join.join((re.findall("●●●●●●(.*)",one_unit_file_path.split(os.sep)[0]))).replace("-","/"),'%Y/%m/%d')
file_creating_years = path_join.join((re.findall("●●●●●●(.*)",one_unit_file_path.split(os.sep)[0])))[0:4] #パス名伏字

#Pathからファイル読込
with codecs.open(one_unit_file_path, "r", "utf-8", "ignore") as File:
    data = pd.read_table(one_unit_file_path, encoding="utf-8", header=None, names="1")
    one_unit_data = (data[data["1"].str.match(".*ERROR.*",na=False)]) #"ERROR"を正規表現で検索し、一致したものをDataFrameに格納

with codecs.open(two_unit_file_path, "r", "utf-8", "ignore") as File:
    data = pd.read_table(two_unit_file_path, encoding="utf-8", header=None, names="1")
    two_unit_data = (data[data["1"].str.match(".*ERROR.*",na=False)])　#"ERROR"を正規表現で検索し、一致したものをDataFrameに格納

Count.deadlock_count(one_unit_data,"one_unit")
Count.deadlock_count(two_unit_data,"two_unit") #サーバー毎に検索する為、"one_unit" or "two_unit"を渡す。

one_unit_deadlock_count = Count.one_unit_deadlock_count
two_unit_deadlock_count = Count.two_unit_deadlock_count #各サーバーのデッドロック数

print("※1.件数が大幅に異なる場合、前日のエラーログの件数と合わせて比較してください。\n　2.同時刻に発生したログは1件にまとめられる場合があるため誤差が発生する日があります。\n"+
      "-----------------------------\n■●●●●●●エラー各件数出力(1号機)\n") #伏字

Search.error_search(one_unit_data["1"]) #Error_Search.pyの関数呼び出し ＆ サーバーエラーログの受け渡し

print("-----------------------------\n■●●●●●●エラー各件数出力(2号機)\n") #伏字

Search.error_search(two_unit_data["1"]) #Error_Search.pyの関数呼び出し ＆ サーバーエラーログの受け渡し

print("\n" + "■Excel記入" + "\n")

Write.excel_dbcp_writing(file_creating_years,file_creation_date,one_unit_deadlock_count) #Excel書き込み関数に、"ファイル作成年月日"　と "デッドロック数"　を渡します。
Write.excel_detec_alarm_writing(file_creating_years,file_creation_date,one_unit_deadlock_count,two_unit_deadlock_count)　#Excel書き込み関数に、"ファイル作成年月日"　と 各ログの"デッドロック数"　を渡します。

print("\n---------------------------------終了------------------------------------")
