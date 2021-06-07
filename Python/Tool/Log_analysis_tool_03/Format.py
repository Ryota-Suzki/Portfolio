import glob
import codecs
import pandas as pd
import datetime as dt

dt_now = dt.datetime.now()

start_date = pd.to_datetime((str(dt_now.year) + "-" + str(dt_now.month)+ "-" + str(dt_now.day) + " " + "09:00:00")) #サービス開始時間をdatetimeに変換
end_date = pd.to_datetime((str(dt_now.year) + "-" + str(dt_now.month)+ "-" + str(dt_now.day) + " "  + "22:00:00")) #サービス終了時間をdatetimeに変換

col_names = ['c{0:02d}'.format(i) for i in range(40)]

def Formating(path):
    global one_unit_log_data, one_unit_in_time, one_unit_out_time, two_unit_log_data, two_unit_in_time, two_unit_out_time

    try: #日によって文字コードが異なるため例外処理
        with codecs.open(path, "r",encoding="shift-jis") as file:
            data_lines = file.read()
            data_lines = data_lines.replace("\t"," ")
    except:
        with codecs.open(path, "r",encoding="utf-8") as file:
            data_lines = file.read()
            data_lines = data_lines.replace("\t"," ")

    with codecs.open(path, "w",encoding="shift-jis") as file:
        file.write(data_lines)

    id = open(path)
    lines = id.readlines()
    id.close()

    with open(path,mode='r+',encoding="shift-jis",errors="ignore") as f:
        f.write("*  * * * * *	*	*	*	* * * * *	*	*	*	*	*	*	*		*	* "+"\n") #データ整形時、必要なログまで無視する処理実装予定


    with codecs.open(path,mode='r+',errors="ignore") as File:
        log_data = pd.read_table(File, delim_whitespace=True, names=col_names,
        converters={'c01':str, 'c06':str, 'c08':str, 'c09':str, 'c10':str, 'c11':str, 'c12':str, 'c13':str, 'c14':str,'c16':str, 'c17':str, 'c22':str, 'c29':str, 'c34':str, 'c35':str})

        # print(log_data)
        drop_index = log_data.index[log_data['c00'] != log_data.iat[20,0]] #DataFrame[20,0]を指定

        log_data = log_data.drop(drop_index).reset_index(drop=True) #削除し、indexを振りなおす

        log_data = log_data[log_data["c15"].str.contains("RC_check_DB_conn", na=False)] #検索文字列:"RC_check_DB_conn" "c15"を検索
        log_data = (log_data.dropna(how='all').dropna(how='all', axis=1)) #NaNを含む列を削除
        log_data = log_data[["c02","c03","c21"]].rename(columns={"c02":"Date","c03":"Unit_name","c21":"DBCP"}) #column名をリネーム

        log_data["DBCP"] = log_data["DBCP"].astype(int) #column:DBCPをint型
        log_data["Unit_name"] = log_data["Unit_name"].astype(str) #column:Unit_nameをstr型
        log_data["Date"] = pd.to_datetime(log_data["Date"])

        if (log_data.iat[1,1]) == "●●●●●●":
            one_unit_log_data = log_data.reset_index(drop=True)

        elif (log_data.iat[1,1]) == "●●●●●●":
            two_unit_log_data = log_data.reset_index(drop=True) #indexを振りなおす
