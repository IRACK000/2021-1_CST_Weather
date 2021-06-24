# -*- coding: utf-8 -*-
'''''''''''''''''''''''''''''''''''''''''''''''''''''''''
### Alias : datareader.py & Last Modded : 2021.05.31. ###
'''''''''''''''''''''''''''''''''''''''''''''''''''''''''
import os
import numpy as np
import pandas as pd
import matplotlib
import matplotlib.pyplot as plt
import matplotlib.font_manager as fm

# path = os.path.dirname(os.path.realpath(__file__)) + "/font/D2Coding1.3.2.ttc"
path = os.path.dirname(os.path.realpath(__file__)) + "/font/BMDOHYEON.ttf"
plt.rc('font', family=fm.FontProperties(fname=path).get_name())
matplotlib.rcParams['axes.unicode_minus'] = False


def read_weather_data(p=os.path.dirname(os.path.realpath(__file__)) + "/api/days.csv"):
    df = pd.read_csv(p)
    del df['일시'], df['Unnamed: 0']
    return df


def find_dangerous_weather(df):
    snow = [day for day, stat in enumerate(df['일기현상']) if "눈" in stat and day > 1]
    rain = [day for day, stat in enumerate(df['일기현상']) if "소나기" in stat or "비" in stat]
    snowydf = df.loc[snow]
    rainydf = df.loc[rain]
    return snow, rain, snowydf, rainydf


def show_weather_pie(snow, rain, df):
    plt.title("대전광역시 2015.01.01~2020.12.31 일기현상 비율")
    plt.pie([len(snow)+1, len(rain), len(df)-len(snow)-1-len(rain)],
            labels=['눈', '소나기, 비', '기타'],
            colors=['#ff9999', '#8fd9b6', '#d395d0'],
            explode=[0.05, 0.05, 0.05], labeldistance=0.35,
            autopct="%.1f%%", shadow=False, counterclock=False
            )
    plt.show()


def show_weather_pattern(target, base, title):
    bardata = target.mean()/base.mean()
    plt.title(title)
    plt.bar(bardata.index, bardata.values,
            edgecolor="gray", linewidth=3, color="springgreen")
    plt.yticks(np.arange(-1, 3.1, 1))
    plt.xticks(rotation=45)
    plt.show()


def slice_data(df, num):
    term_x = df.iloc[0:len(df)-num]
    term_y = df.iloc[num:len(df)]
    term_y.reset_index(drop=True, inplace=True)
    return term_x, term_y


def corr_data(term_x, term_y):
    term = dict()
    for col in term_x.columns:
        try:
            term[col] = pd.DataFrame({0: term_x[col], 1: term_y[col]}).corr()[0][1]
        except KeyError:
            pass
    return term


def show_correlation(term, title):
    plt.figure(figsize=(12, 10))
    plt.title(title)
    plt.bar(term.keys(), term.values(),
            edgecolor="gray", linewidth=1.5, color="orange")
    plt.yticks(np.arange(-0.2, 1.1, 0.1))
    plt.xticks(rotation=45)
    plt.show()


def show_correlation_hist(term, title):
    plt.title(title)
    plt.xlabel("상관계수 평균 = %.5f" % (sum(term.values())/len(term.values())))
    plt.hist(term.values(), edgecolor="aliceblue", linewidth=1.5, color="teal")
    plt.xticks(np.arange(-0.2, 1.1, 0.1))
    plt.yticks(range(0, 22))
    plt.show()


def show_correlation_scater(term1_x, term1_y, term2_x, term2_y):
    rd = np.random.rand
    plt.title("상관계수가 높은 기상변수 예시(양의 상관관계) - 평균기온(r=0.975259)")
    plt.scatter(term1_x['평균기온'], term1_y['평균기온'],
                c=rd(len(term1_x)), alpha=0.5)
    plt.xlabel("하루 전날")
    plt.ylabel("당일날")
    plt.show()
    plt.title("상관계수가 낮은 기상변수 예시(양의 상관관계) - 최다풍향(r=0.360005)")
    plt.scatter(term1_x['최다풍향'], term1_y['최다풍향'],
                c=rd(len(term1_x)), alpha=0.5)
    plt.xlabel("하루 전날")
    plt.ylabel("당일날")
    plt.show()
    plt.title("상관계수가 높은 기상변수 예시(음의 상관관계) - 임의데이터")
    plt.scatter(np.arange(0, 250, 1.4), np.arange(285, -1, -1.6),
                c=rd(179), alpha=0.5)
    plt.show()
    plt.title("상관계수가 낮은 기상변수 예시(음의 상관관계) - 최고해면기압시각(r=-0.194720)")
    plt.scatter(term2_x['최고해면기압시각'], term2_y['최고해면기압시각'],
                c=rd(len(term2_x)), alpha=0.5)
    plt.xlabel("2일 전날")
    plt.ylabel("당일날")
    plt.show()


def find_fatal_var(term1, term2):
    fatal = set()
    term1_f = dict()
    term2_f = dict()
    for key, val in term2.items():
        if val > 0.9 or val < -0.9:
            fatal.add(key)
            term2_f[key] = val
    for key, val in term1.items():
        if val > 0.6 or val < -0.6:
            fatal.add(key)
            term1_f[key] = val
    return fatal, term1_f, term2_f


if __name__ == '__main__':
    df = read_weather_data()

    snow, rain, snowydf, rainydf = find_dangerous_weather(df)
    show_weather_pie(snow, rain, df)
    show_weather_pattern(snowydf, df, "눈이 오는 상황에서의 기상 변수 패턴")
    show_weather_pattern(rainydf, df, "비가 오는 상황에서의 기상 변수 패턴")

    term2_x, term2_y = slice_data(df, 2)
    term1_x, term1_y = slice_data(df, 1)
    term2 = corr_data(term2_x, term2_y)
    term1 = corr_data(term1_x, term1_y)
    show_correlation(term2, "term2 기상 변수별 상관계수")
    show_correlation(term1, "term1 기상 변수별 상관계수")
    show_correlation_hist(term2, "term2 상관계수 히스토그램")
    show_correlation_hist(term1, "term1 상관계수 히스토그램")
    show_correlation_scater(term1_x, term1_y, term2_x, term2_y)
    fatal = find_fatal_var(term1, term2)
    print(fatal)
