# 業務自動化ツール
サーバーログを検索・入力データに整形しExcelファイルに書き込みを行います。
 
# Description
 ・各種サーバーログを、解凍しログ事に検索/整形を行いExcelファイルの該当日付に入力。  
 ・S3へログをアップロード & ファイル作成日付から3か月前のログを削除。  
 ・Python未インストールの方でも使えるよう、pyinstallerにて.exe化を行いbatファイルで起動するだけで書き込みやエラー検索が終わります。  

# Demo
・実行ファイル作成日(2021/04/11)
 ![実行前](https://github.com/Ryota-Suzki/Portfolio/blob/img/before.JPG)
 ![実行後](https://github.com/Ryota-Suzki/Portfolio/blob/img/after.JPG)
 
# Features
 複数のExcelファイルにて、同じログデータを管理していたため手動で行うと年間で膨大な時間を費やす事となっていた上  
 Excelファイルを少なくする事は不可能な事から、複数のExcelファイルに対して同時にログデータを書き込む事で時間を大幅に短縮。  
 エラーを検索する機能では、.pyファイルを触る事なくconfig.iniのリスト内に追加する事で誰でも容易にエラーログの検出可否について設定可能。  
 
# Requirement
 * import codecs  
 * import glob  
 * import pandas as pd  
 * import openpyxl as op  
 * import datetime  
 * import re  
 * import os  
 * import configparser  
 * import pathlib  
 * import sys  
 * from datetime import datetime as dt, date, timezone, timedelta  
 * from boto3 import client  
 * import gzip  
 * import zipfile  
 * from dateutil.relativedelta import relativedelta  
 * from boto3.session import Session  
 * import boto3  

# Usage
DEMO(例)
```bash
python DBCP.py
``` 
# Author
* 作成者 Ryota_Suzuki

