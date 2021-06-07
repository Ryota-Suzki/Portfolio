import codecs
import glob
import pandas as pd
import openpyxl as op
from openpyxl import Workbook, load_workbook
from pathlib import Path
import datetime
import re
import os
import gzip
import zipfile

#日付変数
year = datetime.datetime.now().strftime("%Y")

#パス関連
path_join = ","; current_path = os.getcwd()

#zipファイルリスト
multi_zip_list = (glob.glob(current_path + "任意のパス"+ year + "*.zip"))
single_zip_list = (glob.glob(current_path + "任意のパス"+ year + "*.zip"))

# column定義
column_name = ["IP","DATE","TIME","STATUS","NUM-01","NUM-02","CODE"]
drop_column = ["IP","DATE","STATUS","NUM-01","NUM-02","CODE"]

def access_counts(path, name):
    with codecs.open(path, "r", encoding="utf-8") as file:
        data_lines = file.read()
        try:
            data_lines = data_lines.replace("-","")
            data_lines = re.sub("[ ]+"," ",data_lines)
        except:
            pass
    with codecs.open(path, "w", encoding="utf-8") as file:
        file.write(data_lines)
        data = pd.read_table(path, encoding="utf-8", header=None, names=column_name,sep=" ")
        data["TIME"] = (data["DATE"].astype(str)).str.cat(data["TIME"],sep=" ")
        data = data.drop(drop_column,axis=1)
        data["TIME"]=pd.to_datetime(data["TIME"])
        data["count"] = 1
        result = (data.groupby(pd.Grouper(key="TIME", freq="1h")).sum())
        result.to_csv("任意のパス" + name + "任意のファイル名.csv")

def Decompression(name): #解凍
        try:
            os.makedirs("解凍先フォルダ名")
            os.makedirs("結果先フォルダ名")
        except:
            pass

        for decompression in name: #zipリストを順に読み込み
            with zipfile.ZipFile(decompression) as file_zip:
                file_zip.extractall("./解凍先フォルダ名") #カレントディレクトリに解凍フォルダ作成

try:
    open(path_join.join(single_zip_list))
    print("単数ファイル検知")
    Decompression(single_zip_list)

except:
    print("複数ファイル検知")
    Decompression(multi_zip_list)

file_path = glob.glob("任意のパス")
for list in file_path:
    file_date = (re.split('\.',list)[1])
    access_counts(list, file_date)
print("終了")