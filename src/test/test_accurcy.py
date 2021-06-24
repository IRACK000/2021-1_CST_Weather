# -*- coding: utf-8 -*-
import os
import sys
import unittest
sys.path.append(os.path.dirname(os.path.abspath(os.path.dirname(__file__))) + "/main")
from main import *


class CustomTests(unittest.TestCase):
    def setUp(self):
        """테스트 시작되기 전 실행"""
        global df, data, snow, rain, snowydf, rainydf, term2_x, term2_y,\
            term1_x, term1_y, term2, term1, fatal, term1_f, term2_f
        df = read_weather_data()

        snow, rain, snowydf, rainydf = find_dangerous_weather(df)
        term2_x, term2_y = slice_data(df, 2)
        term1_x, term1_y = slice_data(df, 1)
        term2 = corr_data(term2_x, term2_y)
        term1 = corr_data(term1_x, term1_y)
        fatal, term1_f, term2_f = find_fatal_var(term1, term2)

    def tearDown(self):
        """테스트 종료 후 실행"""
        pass

    def test_runs(self):
        """단순 실행여부 판별하는 테스트 메소드"""
        global cmpr
        try:
            cmpr = pd.read_csv(os.path.dirname(os.path.realpath(__file__)) + "/test_days.csv")
            del cmpr['Unnamed: 0']
        except Exception as e:
            print(e)
            print("test_days.py를 실행하여 test_days.csv를 생성하였는지 확인해주세요!")
            exit(1)

        global chech_snow, chech_rain
        chech_snow = [0, 0, 0]  # [일치, 왔는데 안왔다고, 안왔는데 왔다고]
        chech_rain = [0, 0, 0]  # [일치, 왔는데 안왔다고, 안왔는데 왔다고]
        for i in range(158):
            self.compare(i)
        print(chech_snow)
        print(chech_rain)

    def compare(self, i):
        print(cmpr['일시'][i+2], end=' ')
        recent = cmpr.loc()[i:i+1]
        recent.reset_index(drop=True, inplace=True)
        res2 = search_pattern(recent, term2_x, term2_y, term2_f, 2)[fatal]
        res1 = search_pattern(recent, term1_x, term1_y, term1_f, 1)[fatal]
        prediction = calculate_with_weights(term1, term2, res1, res2)
        conclusion = conclude(prediction, snowydf, rainydf, df)
        con = "눈" if conclusion == 1 else "비" if conclusion == 2 else "기타"
        if "눈" in cmpr['일기현상'][i+2]:
            if con == "눈":
                print(" 일치 : " + con)
                chech_snow[0] += 1
            elif con == "비":
                print("불일치 : " + "눈" + "/" + con)
                chech_snow[1] += 1
                chech_rain[2] += 1
            else:
                print("불일치 : " + "눈" + "/" + con)
                chech_snow[1] += 1
        elif "소나기" in cmpr['일기현상'][i+2] or "비" in cmpr['일기현상'][i+2]:
            if con == "눈":
                print("불일치 : " + "비" + "/" + con)
                chech_snow[2] += 1
                chech_rain[1] += 1
            elif con == "비":
                print(" 일치 : " + con)
                chech_rain[0] += 1
            else:
                print("불일치 : " + "비" + "/" + con)
                chech_rain[1] += 1
        else:
            if con == "눈":
                print("불일치 : " + "기타" + "/" + con)
                chech_snow[2] += 1
            elif con == "비":
                print("불일치 : " + "기타" + "/" + con)
                chech_rain[2] += 1
            else:
                print(" 일치 : " + con)


if __name__ == '__main__':
    unittest.main()
