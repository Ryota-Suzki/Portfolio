import Excel_Write as write
import pandas as pd
import glob
import openpyxl as op
import datetime as dt

from pathlib import Path
from openpyxl import load_workbook

path_join = ""

dt_now = dt.datetime.now()

start_date = pd.to_datetime((str(dt_now.year) + "-" + str(dt_now.month)+ "-" + str(dt_now.day) + " " + "09:00:00"))
end_date = pd.to_datetime((str(dt_now.year) + "-" + str(dt_now.month)+ "-" + str(dt_now.day) + " "  + "22:00:00"))

def dbcp_check(File):
    global in_time_dbcp, out_time_dbcp

    mark = "★"
    message = "Limit,Over"
    _prevdbcps = File.iat[0,2]
    message_list = []
    mark_list = []

    # DataFrameからList(int型)に変換
    dbcp_list = list(map(int, File["DBCP"].values))

    # DBCP数30以上でメッセージ表示
    for dbcp_count in dbcp_list:
        if dbcp_count >= 30:
            message_list.append(message)

        else:
            message_list.append(None)

    alart_message = pd.DataFrame({"MESSAGE":message_list})

    for dbcp_count in dbcp_list:
        if dbcp_count >= _prevdbcps + 2:
            mark_list.append(mark)

        else:
            mark_list.append(None)

        _prevdbcps = dbcp_count

    comparsion_mark = pd.DataFrame({"MARK":mark_list})

    log_data = pd.concat([File, alart_message, comparsion_mark], axis=1)

    in_time_data = log_data.loc[(log_data['Date'] > start_date) & (log_data['Date'] < end_date)].reset_index(drop=True)
    out_time_data = log_data.loc[(log_data['Date'] < start_date) | (log_data['Date'] > end_date)].reset_index(drop=True)

    in_time_comparsion = in_time_data[in_time_data["MARK"].str.contains("★", na=False)]
    in_time_alart = in_time_data[in_time_data["MESSAGE"].str.contains("Limit,Over", na=False)]

    out_time_comparsion = out_time_data[out_time_data["MARK"].str.contains("★", na=False)]
    out_time_alart = out_time_data[out_time_data["MESSAGE"].str.contains("Limit,Over", na=False)]

    in_time_dbcp = (str(min(in_time_data["DBCP"], key=int)) + "-" + str(max(in_time_data["DBCP"], key=int)))
    out_time_dbcp = (str(min(out_time_data["DBCP"], key=int)) + "-" + str(max(out_time_data["DBCP"], key=int)))

    write.detection_excel_write((log_data.iat[1,1]), in_time_dbcp, out_time_dbcp)

    write.dbcp_excel_write(in_time_data, start_date, (log_data.iat[1,1]), in_time_alart)
    write.dbcp_excel_write(out_time_data, start_date, (log_data.iat[1,1]), out_time_alart)
