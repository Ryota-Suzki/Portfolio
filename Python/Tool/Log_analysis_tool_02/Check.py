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
        print("■ファイルは存在しています。")

def main():
    myCheck = os.path.isfile(file_path)

    writeTxt(file_name, myCheck)

set_path_01 = glob.glob("●●●●●●*/●●●●●●.*")
set_path_01 = " ".join(set_path_01)
file_name = os.path.basename(set_path_01)

set_path_02 = glob.glob("●●●●●●*/")
set_path_02 = " ".join(set_path_02)

file_path = os.path.join(set_path_02,file_name)

main()
