# -*- coding: utf-8 -*-
'''''''''''''''''''''''''''''''''''''''''''''''''''''''''
### Alias : main.py & Last Modded : 2021.06.01. ###
'''''''''''''''''''''''''''''''''''''''''''''''''''''''''
from datareader import *
import api.recentdays as rcd
from datastatizer import *


def search_pattern(search, term_x, term_y, term_f, term_num):
    res = ((abs(term_x[term_f.keys()]-search.T[2-term_num].T[term_f.keys()])*term_f.values()).sum(axis=1)/sum(term_f.values())).idxmin()
    return term_y.T[res]


def calculate_with_weights(term1, term2, res1, res2):
    t1 = pd.Series({key: term1[key] for key in res1.index})
    t2 = pd.Series({key: term2[key] for key in res2.index})
    return ((res1*t1+res2*t2)/(t1+t2))[res1.index]


def conclude(prediction, snowydf, rainydf, df):
    '''
    sn = (abs(snowydf[prediction.index]-prediction).mean()/df[prediction.index].mean()).mean()
    rn = (abs(rainydf[prediction.index]-prediction).mean()/df[prediction.index].mean()).mean()
    print(round(sn, 6), round(rn, 6), end=' ')
    if (sn <= 0.19 and rn >= 0.9) or (0.19413 <= sn <= 0.22046 and rn >= 0.8498):
        return 1
    elif sn >= 0.191 and rn >= 1.0275:
        return 0
    elif (sn > 1.02 or sn < 1) and rn <= 0.49595:
        return 2
    else:
        return 0
    '''
    res = ((abs(df[prediction.index]-prediction)).mean(axis=1)/df[prediction.index].mean(axis=1)).idxmin()
    if "눈" in df['일기현상'][res]:
        return 1
    elif "소나기" in df['일기현상'][res] or "비" in df['일기현상'][res]:
        return 2
    else:
        return 0


if __name__ == '__main__':
    df = read_weather_data()
    recent = rcd.get_data()
    data = read_acci_data()

    PLOT_ON = input() != "n"

    snow, rain, snowydf, rainydf = find_dangerous_weather(df)
    if PLOT_ON: show_weather_pie(snow, rain, df)
    if PLOT_ON: show_weather_pattern(snowydf, df, "눈이 오는 상황에서의 기상 변수 패턴")
    if PLOT_ON: show_weather_pattern(rainydf, df, "비가 오는 상황에서의 기상 변수 패턴")

    term2_x, term2_y = slice_data(df, 2)
    term1_x, term1_y = slice_data(df, 1)
    term2 = corr_data(term2_x, term2_y)
    term1 = corr_data(term1_x, term1_y)
    if PLOT_ON: show_correlation(term2, "term2 기상 변수별 상관계수")
    if PLOT_ON: show_correlation(term1, "term1 기상 변수별 상관계수")
    if PLOT_ON: show_correlation_hist(term2, "term2 상관계수 히스토그램")
    if PLOT_ON: show_correlation_hist(term1, "term1 상관계수 히스토그램")
    if PLOT_ON: show_correlation_scater(term1_x, term1_y, term2_x, term2_y)
    fatal, term1_f, term2_f = find_fatal_var(term1, term2)

    res2 = search_pattern(recent, term2_x, term2_y, term2_f, 2)[fatal]
    res1 = search_pattern(recent, term1_x, term1_y, term1_f, 1)[fatal]
    prediction = calculate_with_weights(term1, term2, res1, res2)
    conclusion = conclude(prediction, snowydf, rainydf, df)

    print(prediction)
    os.system("pause")

    if PLOT_ON: show_acci_pie(data)
    death_rate = trim_data(data)
    if PLOT_ON: show_death_rate(death_rate)
    print("\n눈이 올 확률이 높으므로 고속도로와 시내도로에서 주의하여 운전해야 한다!\n"
          if conclusion == 1 else
          "\n비가 올 확률이 높으므로 고속도로와 시내도로에서 주의하여 운전해야 한다!\n"
          if conclusion == 2 else
          "\n강수 확률이 적으므로 평소처럼 운전하면 된다.\n")

    os.system("pause")
