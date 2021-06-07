import glob
import codecs
import pandas as pd
import datetime as dt

dt_now = dt.datetime.now()

start_time = pd.to_datetime((str(dt_now.year) + "-" + str(dt_now.month)+ "-" + str(dt_now.day) + " " + "09:00:00")) #サービス開始時間をdatetimeに変換
end_time = pd.to_datetime((str(dt_now.year) + "-" + str(dt_now.month)+ "-" + str(dt_now.day) + " "  + "22:00:00")) #サービス終了時間をdatetimeに変換

def Formating(path): #ログファイルの整形(ファイルパス)
    global file
    try: #日によって文字コードが異なるため例外処理
        with codecs.open(path, "r", encoding="shift-jis") as file:
            data_lines = file.read()
            data_lines = data_lines.replace("\t"," ")　#タブを空白に変換
        with codecs.open(path, "w", encoding="utf-8") as file:
            file.write(data_lines) #変換した全行を書き込み

    except:
        with codecs.open(path, "r", encoding="utf-8") as file:
            data_lines = file.read()
            data_lines = data_lines.replace("\t"," ")
        with codecs.open(path, "w", encoding="utf-8") as file:
            file.write(data_lines)

def Date_range_specified(df_name,unit_name): #サービス時間内と時間外に分割(サービス全時間のログ、サーバー区別の文字列)
    global one_unit_in_time,one_unit_out_time,two_unit_in_time,two_unit_out_time

    if "one_unit" in unit_name: #"one_unit"の場合
        df_name["c01"] = df_name["c01"].str.replace('(\..*)', '') #ミリ秒を削除
        df_name["c01"] = pd.to_datetime(df_name["c01"], errors='ignore') #"c01"を時間型に変換

        one_unit_in_time = df_name.loc[(df_name['c01'] > start_time) & (df_name['c01'] < end_time)] #サービス時間内に分割
        one_unit_out_time = df_name.loc[(df_name['c01'] < start_time) | (df_name['c01'] > end_time)] #サービス時間外に分割

        one_unit_in_time = (one_unit_in_time[one_unit_in_time["c02"].str.contains("SEVERE", na=False)]) #サービス時間内のエラーログを検索
        one_unit_out_time = (one_unit_out_time[one_unit_out_time["c02"].str.contains("SEVERE", na=False)])  #サービス時間外のエラーログを検索

    elif "two_unit" in unit_name: #ダミーファイル("two_unit")がある場合、変数には空のDataFrame

        if df_name.iat[0,1] == "This":
            two_unit_in_time = pd.DataFrame()
            two_unit_out_time = pd.DataFrame()

            two_unit_in_time = pd.DataFrame()
            two_unit_out_time = pd.DataFrame()
        else: #ダミーファイルがない場合
            df_name["c01"] = pd.to_datetime(df_name["c01"].str.replace('(\..*)', ''))

            two_unit_in_time = df_name.loc[(df_name['c01'] > start_time) & (df_name['c01'] < end_time)] #サービス時間内に分割
            two_unit_out_time = df_name.loc[(df_name['c01'] < start_time) | (df_name['c01'] > end_time)] #サービス時間外に分割

            two_unit_in_time = (two_unit_in_time[two_unit_in_time["c02"].str.contains("SEVERE", na=False)]) #サービス時間内のエラーログを検索
            two_unit_out_time = (two_unit_out_time[two_unit_out_time["c02"].str.contains("SEVERE", na=False)])  #サービス時間外のエラーログを検索
    else:
        print()
