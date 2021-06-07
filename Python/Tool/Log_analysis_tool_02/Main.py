
import Error_Search as Search
import Check
import Format as Ft
import pandas as pd
import openpyxl as op
import glob
import codecs
import datetime as dt
import re
import os
import pathlib

from datetime import time
from openpyxl.styles import Font
from openpyxl.styles.alignment import Alignment

### call tion ###
Check.writeTxt #SV-RCWW-02にcatalina.*logが存在しない場合のFunction

#　変数
Path_join = ","; word = "●●●●●●エラーログ件数"

# ファイルのパス取得
one_unit_catalina_path = Path_join.join(glob.glob("●●●●●●*/●●●●●●.*"))
two_unit_catalina_path = Path_join.join(glob.glob("●●●●●●*/●●●●●●.*"))

# 時間変数
file_creatiing_date = Path_join.join((re.findall("●●●●●●(.*)",one_unit_catalina_path.split(os.sep)[0])))
creation_date =  dt.datetime.strptime(file_creatiing_date,'%Y-%m-%d').strftime('%Y/%m/%d/')

col_names = ['c{0:02d}'.format(i) for i in range(200)]

### call function ###
Ft.Formating(one_unit_catalina_path)
Ft.Formating(two_unit_catalina_path) #Format.pyにファイルパスを受け渡し

with codecs.open(one_unit_catalina_path, "r", "utf-8", "ignore") as file:
    one_unit_data = pd.read_table(file, encoding="utf-8", header=None, names=col_names)

    one_unit_total_time = pd.read_table(one_unit_catalina_path, header=None, names=col_names, sep=' ', engine = 'python',
    converters={'c28':str, 'c29':str, 'c30':str, 'c31':str, 'c32':str, 'c33':str, 'c34':str, 'c35':str, 'c36':str,'c37':str, 'c38':str, 'c39':str, 'c40':str, 'c41':str}).dropna(subset=["c00","c01"])
    # print(one_unit_total_time)
    one_unit_total_time = one_unit_total_time[one_unit_total_time["c00"].str.contains(one_unit_total_time.iat[0,0])]

with codecs.open(two_unit_catalina_path, "r", "utf-8", "ignore") as file:
    two_unit_data = pd.read_table(file, encoding="utf-8", header=None, names=col_names)

    two_unit_total_time = pd.read_table(two_unit_catalina_path, header=None, names=col_names,sep=' ',
    converters={'c28':str, 'c29':str, 'c30':str, 'c31':str, 'c32':str, 'c33':str, 'c34':str, 'c35':str, 'c36':str,'c37':str, 'c38':str, 'c39':str, 'c40':str, 'c41':str}).dropna(subset=["c00","c01"])
    # print(two_unit_total_time)
    two_unit_total_time = two_unit_total_time[two_unit_total_time["c00"].str.contains(two_unit_total_time.iat[0,0])]

### call function ###

Ft.Date_range_specified(one_unit_total_time, "one_unit")
Ft.Date_range_specified(two_unit_total_time, "two_unit") #サービス時間内と時間外に分割関数(サービス全時間のログ,サーバー毎に処理するため"one_unit" or "two_unit")

Search.Extraction(one_unit_data,"one_unit")
Search.Extraction(two_unit_data,"two_unit") #エラーログ検索関数(サーバー毎のログ、サーバー毎に処理するため"one_unit" or "two_unit")

severe_one_unit = Search.severe_one_unit
severe_two_unit = Search.severe_two_unit #"SEVERE"検索結果

print("※1.全件数(SEVERE/Exception)もしくは時間内ログ件数と一致している場合OKとします。\n　2.同時刻に発生したログは1件にまとめられる場合があるため数件の誤差が発生する日があります。\n")
print("-----------------------------\n■DSPRS_log_0204エラー各件数出力(1号機)\n")

### call function ###
Search.Error_Search(severe_one_unit["c00"], "one_unit", Ft.one_unit_out_time, Ft.one_unit_in_time)

print("-----------------------------\n■DSPRS_log_0204エラー各件数出力(2号機)\n")

### call function ###
Search.Error_Search(severe_two_unit["c00"],"two_unit", Ft.two_unit_out_time, Ft.two_unit_in_time)

#------------------------------------------------------------------------#
print("■テキストファイル書き込み中")

path = pathlib.Path().absolute()
path /='../../../●●●●●●/'

File_Path = str(path)

Text_path = glob.glob(File_Path + "/●●●●●●エラーログ件数.*txt")
Text_path = Path_join.join(Text_path)

print("・" + str(Text_path[9:]))

with open(Text_path, mode='r') as File:
    lines = File.readlines()
    lines = Path_join.join(lines)

with open(Text_path, mode='a') as File:
    if re.match(word,lines): #変数Wordに一致している場合
        File.write(creation_date + " " + str(len(severe_one_unit)) + "件" + "\n")
    else: #変数Wordに一致していない場合
        File.write("●●●●●●エラーログ件数" + "\n" + creation_date + " " + str(len(severe_one_unit)) + "件" + "\n")

print("\n---------------------------------終了--------------------------------------")
