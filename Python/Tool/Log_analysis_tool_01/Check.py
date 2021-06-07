#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import os
import glob
import re
import datetime

now = datetime.datetime.now()
now = now.strftime("%y%m%d")

def writeTxt(file_name, myCheck):
    if not myCheck:
        with open(file_path, "w") as f:
            f.write(file_name + " This File wasn't found" + '\n')
            f.write(file_name + " Dummy File was created" + '\n')
            print("●●●●●●フォルダにダミーファイルを作成しました。")
    else: 
        print("■ファイルは存在しています。\n")

def main():
    myCheck = os.path.isfile(file_path)
    writeTxt(file_name, myCheck)

set_path_01 = glob.glob("●●●●●●*/●●●●●●*") # パス取得（rc5x-auth.log）
set_path_01 = " ".join(set_path_01) #PATH変換
file_name = os.path.basename(set_path_01)       # 末尾(rc5x-auth.log)検索ファイル名に設定

set_path_02 = glob.glob("●●●●●●*/")  #ダミーファイル作成パスを設定
set_path_02 = " ".join(set_path_02)

file_path = os.path.join(set_path_02,file_name)  # パスとファイル名を結合

main()
