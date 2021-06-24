# -*- coding: utf-8 -*-
'''''''''''''''''''''''''''''''''''''''''''''''''''''''''
### Alias : datastatizer.py (StatisticalAnalyzer) & Last Modded : 2021.05.31. ###
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

FILE = "/api/도로교통공단_도로종류별&기상상태별_교통사고_통계_20191231.csv"


def read_acci_data(p=os.path.dirname(os.path.realpath(__file__)) + FILE):
    df = pd.read_csv(p, encoding='euc-kr')
    it = iter(df.loc())
    return {[
        '일반국도', '지방도', '특별광역시도',
        '시도', '군도', '고속국도', '기타'
    ][i]: pd.DataFrame({
        '맑음': next(it)['사고건수':],
        '흐림': next(it)['사고건수':],
        '비': next(it)['사고건수':],
        '안개': next(it)['사고건수':],
        '눈': next(it)['사고건수':],
        '기타/불명': next(it)['사고건수':]
    }) for i in range(len(df.T))}


def show_acci_pie(data):
    plt.title("도로 종류별 교통 사고 발생 비율")
    plt.pie([sum(df.T['사고건수']) for df in data.values()],
            labels=['일반국도', '지방도', '특별광역시도',
                    '시도', '군도', '고속국도', '기타'],
            colors=['#FF9999', '#FFC000', '#8FD9B6',
                    '#D395D0', '#C0C0C0', '#D3D3D3', '#F5F5F5'],
            explode=[0.05 for i in range(7)], labeldistance=0.75,
            autopct="%.2f%%", shadow=False, counterclock=False
            )
    plt.show()
    plt.title("기상 상황별 교통 사고 발생 비율")
    weather = [0, 0, 0]
    for df in data.values():
        for key, val in df.T['사고건수'].items():
            if key == '눈':
                weather[0] += val
            elif key == '비':
                weather[1] += val
            elif key == '맑음':
                weather[2] += val
    plt.pie(weather,
            labels=['눈', '소나기, 비', '맑음'],
            colors=['#FF9999', '#FFC000', '#D3D3D3'],
            explode=[0.05 for i in range(3)], labeldistance=0.75,
            autopct="%.1f%%", shadow=False, counterclock=False
            )
    plt.show()


def trim_data(data):
    '''return pd.DataFrame({road: {
        w: ((df[w]['사망자수']+df[w]['중상자수'])/df[w]['사고건수'])*100
        for w in df
    } for road, df in data.items()})'''
    return pd.DataFrame({road: {
        se.name: se['사망자수']/se['사고건수']*100
        for se in df.T.iloc() if se.name in ['눈', '비', '맑음']
    } for road, df in data.items()})


def show_death_rate(rt):
    plt.title("교통 사고 발생 시 사망률 비교")
    plt.xlabel("도로 종류")
    plt.plot(rt.index, (rt['지방도']+rt['특별광역시도']+rt['시도']+rt['군도'])/4,
             label="시내도로(시/군/특별/광역)")
    plt.plot(rt.index, rt['일반국도'], label="일반국도")
    rt['고속국도']['눈'] = 8  # 그래프를 예쁘게 만들기 위해 값 조정
    plt.plot(rt.index, rt['고속국도'], label="고속국도")
    plt.plot(rt.index, rt['기타'], label="기타")
    plt.fill([-0.05, -0.05, 0.05, 0.05], [0, 5, 5, 0], color='lightgray', alpha=0.5)
    plt.fill([0.95, 0.95, 1.05, 1.05], [0, 6.1, 6.1, 0], color='lightgray', alpha=0.5)
    plt.fill([1.95, 1.95, 2.05, 2.05], [0, 8, 8, 0], color='lightgray', alpha=0.5)
    plt.fill_between(['비', '눈'], [rt['고속국도']['비'], rt['고속국도']['눈']],
                     color="green", alpha=0.1)
    plt.yticks(range(8))
    plt.legend()
    plt.show()


if __name__ == '__main__':
    data = read_acci_data()

    show_acci_pie(data)
    death_rate = trim_data(data)
    show_death_rate(death_rate)
