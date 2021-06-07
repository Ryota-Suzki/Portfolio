# -*- coding: utf-8 -*-

import pandas as pd

DEADLOCK = "デッドロック"

def deadlock_count(data,name):
    global one_unit_deadlock_count, two_unit_deadlock_count
    if name == "one_unit":
        one_unit_deadlock_count = len(data[data["1"].str.contains(DEADLOCK)]) #"デッドロック"の文字列を含む行を抽出、カウント

    elif name == "two_unit":
        two_unit_deadlock_count = len(data[data["1"].str.contains(DEADLOCK)]) #"デッドロック"の文字列を含む行を抽出、カウント
