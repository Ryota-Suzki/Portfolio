import Unit_process as up
import Format as ft
import Excel_Write as write

import numpy as np
import openpyxl as op
import pandas as pd
import glob
import datetime
import sys
import re
import os
import codecs
from openpyxl import load_workbook
from pathlib import Path

path_join = ""
print("■対象ファイル")

pd.set_option('display.max_rows',20)

one_unit_path = path_join.join(glob.glob("●●●●●●*" + "/*●●●●●●*"))
two_unit_path = path_join.join(glob.glob("●●●●●●*" + "/*●●●●●●*"))

file_year = path_join.join((re.findall("●●●●●●(.*)",one_unit_path.split(os.sep)[0])))[0:4]
file_creation_date = datetime.datetime.strptime(path_join.join((re.findall("●●●●●●(.*)",one_unit_path.split(os.sep)[0]))),'%Y%m%d')

print(one_unit_path + "\n" + two_unit_path)

ft.Formating(one_unit_path)
ft.Formating(two_unit_path) #ログデータ整形

# ##call function##
write.excel_set("DBCP", file_year, file_creation_date)
write.excel_set("検知", file_year, file_creation_date) #Excelファイル指定関数

# DBCP数-Function #
print("■DBCP数 (Limit,Over)")
up.dbcp_check(ft.one_unit_log_data)
up.dbcp_check(ft.two_unit_log_data) #DBCP数が規定の数値を超えてるか判定

print("\n" + "正常に処理しました")
