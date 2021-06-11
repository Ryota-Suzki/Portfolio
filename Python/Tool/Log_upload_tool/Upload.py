# -*- coding: utf-8 -*-
import Download
import svn
import os
import pathlib
import glob
import re
import datetime
from dateutil.relativedelta import relativedelta
import configparser
from boto3.session import Session

# Download　実行
Download.download_file()

# svn 実行
svn.svn_commit()

path_join = ""

path = pathlib.Path().absolute()   # test.pyのあるディレクトリ
path /= '●●●●●●/'     # ディレクトリ移動

config_path = path_join.join(glob.glob(str(path) + "/config.ini"))

config_ini = configparser.ConfigParser()
config_ini.read(config_path)

id = config_ini["セクション名"]["キー"]　#aws id
secret_key = config_ini["セクション名"]["キー"] # aws secret key

session = Session(aws_access_key_id = id,aws_secret_access_key = secret_key)

zip_list = (glob.glob(Download.save_path + "/*.zip")) #zipファイルのリスト作成
gz_list = (glob.glob(Download.save_path + "*.gz")) #gzファイルのリスト作成

file_creating_date = path_join.join((re.findall("●●●●●●(.*).zip",path_join.join(zip_list[0])))) #ファイル作成年月日

creating_years = datetime.datetime.strptime(file_creating_date,"%Y-%m-%d").year #ファイル作成年
creating_month = str(datetime.datetime.strptime(file_creating_date,"%Y-%m-%d").year) + "0" + str(datetime.datetime.strptime(file_creating_date,"%Y-%m-%d").month) #ファイル作成月
creation_date = path_join.join((re.findall("●●●●●●(.*).zip",path_join.join(zip_list[0])))).replace("-","") #ファイル作成日

today = str(datetime.datetime.today() - relativedelta(months=3)).partition(".")[0] #今日の日付
select_date = datetime.datetime.strptime(today,'%Y-%m-%d %H:%M:%S').strftime('%Y%m') #フォルダ指定用の日付に置換
select_year = datetime.datetime.strptime(select_date,'%Y%m').strftime('%Y')


s3_resource = session.resource('●●●●●●') #接続先
bucket = s3_resource.Bucket("●●●●●●") #接続先バケット名

s3client = session.client('s3') #接続先(ログ削除用)
client_bucket = "●●●●●●" #接続先バケット名
prefix = '●●●●●●/●●●●●●/{0}/{1}/'.format(select_year,select_date) #削除先フォルダパス(今日の日付から3か月前のログフォルダ)

def delete_all_keys(client_bucket,prefix,dryrun=False): #S3フォルダ削除
    contents_count = 0
    next_token = ''

    while True:
        if next_token == '':
            response = s3client.list_objects_v2(Bucket = client_bucket,Prefix=prefix)
        else:
            response = s3client.list_objects_v2(Bucket = client_bucket,Prefix=prefix, ContinuationToken=next_token)

        if 'Contents' in response:
            contents = response['Contents']
            contents_count = contents_count + len(contents)
            for content in contents:
                # if not dryrun:
                if dryrun:
                    print("Deleting: s3://" + client_bucket + "/" + content['Key'])
                    s3client.delete_object(Bucket=client_bucket, Key=content['Key'])
                else:
                    print("DryRun: s3://" + client_bucket + "/" + content['Key'])

        if 'NextContinuationToken' in response:
            next_token = response['NextContinuationToken']
            print(next_token)
        else:
            break
    if contents_count == 0:
        print("削除対象件数：" + str(contents_count)) #削除したファイル数
    elif contents_count > 0:
        print("削除件数："+ str(contents_count))

def UploadFile(name): #S3アップロード
    for Writeing in name:
        path = (path_join.join(Writeing))
        print(str(path) + "アップロード完了")
        bucket.upload_file("{}".format(Writeing),"●●●●●●/●●●●●●/{0}/{1}/{2}/{3}".format(creating_years,creating_month,creation_date,os.path.basename(Writeing)))

def Decompression(name): #ローカルでファイル解凍
    if name == gz_list:
        for decompression in name:
            file = path_join.join(decompression)
            os.makedirs(decompression.replace(".gz",""),exist_ok=True) #ディレクトリ作成 例(●●●●●●_2021-01-08.gz → ●●●●●●_2021-01-08
            file_name = re.sub("sv-rc.*[0-2]_","",decompression).replace(".gz","") #ファイル名変数 例(xxxx_●●●●●●_20210124 → ●●●●●●_20210124
            decompression_file = open(decompression.replace(".gz","") + "/" + file_name,'wb') #書込み先ファイル先変数
            #例(●●●●●●.gz/●●●●●●_20210124 →　●●●●●●_20210124/●●●●●●_20210124
            with gzip.open(file, 'rb') as f_in: #gzファイルをByte型で読込
                for line in f_in:
                    decompression_file.write(line) #Byte型を順に書込み先ファイルに書き込み
    elif name == zip_list:
        for decompression in name: #zipリストを順に読み込み
            with zipfile.ZipFile(decompression) as file_zip:
                file_zip.extractall("./") #カレントディレクトリに解凍フォルダ作成

delete_all_keys(client_bucket, prefix, True) #ログ削除関数

UploadFile(zip_list) #フォルダアップロード関数
UploadFile(gz_list)

