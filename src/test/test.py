# -*- coding: utf-8 -*-
'''''''''''''''''''''''''''''''''''''''''''''''''''''''''
### Alias : test.py & Last Modded : 2021.06.01. ###
'''''''''''''''''''''''''''''''''''''''''''''''''''''''''
import os
import sys
sys.path.append(os.path.dirname(os.path.abspath(os.path.dirname(__file__))) + "/main")
from main import *


df = read_weather_data()

snow, rain, snowydf, rainydf = find_dangerous_weather(df)

term2_x, term2_y = slice_data(df, 2)
term1_x, term1_y = slice_data(df, 1)
term2 = corr_data(term2_x, term2_y)
term1 = corr_data(term1_x, term1_y)
fatal, term1_f, term2_f = find_fatal_var(term1, term2)


df1 = pd.read_csv(os.path.dirname(os.path.realpath(__file__)) + "/test_snow_days.csv")
df2 = pd.read_csv(os.path.dirname(os.path.realpath(__file__)) + "/test_rain_days.csv")
del df1['Unnamed: 0'], df2['Unnamed: 0']


def test_(ST, END):
    recent = rcd.get_data(ST, END)
    res2 = search_pattern(recent, term2_x, term2_y, term2_f, 2)[fatal]
    res1 = search_pattern(recent, term1_x, term1_y, term1_f, 1)[fatal]
    prediction = calculate_with_weights(term1, term2, res1, res2)
    conclusion = conclude(prediction, snowydf, rainydf, df)
    return "눈" if conclusion == 1 else "비" if conclusion == 2 else "기타"


if __name__ == '__main__':
    print("#1월달 비교")
    count = 0
    for i in range(29):
        print(df1['일시'][i+2], end=' ')
        if "눈" in df1['일기현상'][i+2]:
            stat = "눈"
        elif "소나기" in df1['일기현상'][i+2] or "비" in df1['일기현상'][i+2]:
            stat = "비"
        else:
            stat = "기타"
        con = test_(20210101+i, 20210102+i)
        if stat == con:
            print(" 일치 : " + stat)
            count += 1
        else:
            print("불일치 : " + stat + "/" + con)
    print("일치(%d), 불일치(%d)" % (count, 29-count))
    print("#5월달 비교")
    count = 0
    for i in range(29):
        print(df2['일시'][i+2], end=' ')
        if "눈" in df2['일기현상'][i+2]:
            stat = "눈"
        elif "소나기" in df2['일기현상'][i+2] or "비" in df2['일기현상'][i+2]:
            stat = "비"
        else:
            stat = "기타"
        con = test_(20210501+i, 20210502+i)
        if stat == con:
            print(" 일치 : " + stat)
            count += 1
        else:
            print("불일치 : " + stat + "/" + con)
    print("일치(%d), 불일치(%d)" % (count, 29-count))
