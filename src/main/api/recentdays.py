# -*- coding: utf-8 -*-
'''''''''''''''''''''''''''''''''''''''''''''''''''''''''
### Alias : recentdays.py & Last Modded : 2021.05.31. ###
'''''''''''''''''''''''''''''''''''''''''''''''''''''''''
import os
import json
import pandas as pd
from urllib.request import Request, urlopen
from urllib.parse import urlencode, quote_plus
from datetime import date, timedelta

# read config file
from configparser import ConfigParser

config = ConfigParser()
config.read(os.path.dirname(os.path.realpath(__file__)) + "/key.config")  # https://codechacha.com/ko/python-examples-get-working-directory/
API_KEY = config.get('dataportal', 'decodedkey')

# get data from https://data.kma.go.kr/data/grnd/selectAsosRltmList.do?pgmNo=36
url = 'http://apis.data.go.kr/1360000/AsosDalyInfoService/getWthrDataList'


def get_data(ST=(date.today()-timedelta(2)).strftime("%Y%m%d"), END=(date.today()-timedelta(1)).strftime("%Y%m%d")):
    queryParams = '?' + urlencode({quote_plus('ServiceKey'): API_KEY,
                                   quote_plus('pageNo'): '1',
                                   quote_plus('numOfRows'): '2',
                                   quote_plus('dataType'): 'JSON',
                                   quote_plus('dataCd'): 'ASOS',
                                   quote_plus('dateCd'): 'DAY',
                                   quote_plus('startDt'): ST,
                                   quote_plus('endDt'): END,
                                   quote_plus('stnIds'): '133'
                                   })

    request = Request(url + queryParams)
    request.get_method = lambda: 'GET'
    with urlopen(request) as opened:
        response = opened.read().decode('utf-8')
        item = json.loads(response)['response']['body']['items']['item']
        df = pd.DataFrame(item)
        del df['stnId'], df['stnNm']
        df = df.rename(columns={'tm': '일시',
                                'avgTa': '평균기온',
                                'minTa': '최저기온',
                                'minTaHrmt': '최저기온시각',
                                'maxTa': '최고기온',
                                'maxTaHrmt': '최고기온시각',
                                'mi10MaxRn': '10분최다강수량',
                                'mi10MaxRnHrmt': '10분최다강수량시각',
                                'hr1MaxRn': '1시간최다강수량',
                                'hr1MaxRnHrmt': '1시간최다강수량시각',
                                'sumRnDur': '강수계속시간',
                                'sumRn': '일강수량',
                                'maxInsWs': '최대순간풍속',
                                'maxInsWsWd': '최대순간풍속풍향',
                                'maxInsWsHrmt': '최대순간풍속시각',
                                'maxWs': '최대풍속',
                                'maxWsWd': '최대풍속 풍향',
                                'maxWsHrmt': '최대풍속시각',
                                'avgWs': '평균풍속',
                                'hr24SumRws': '풍정합',
                                'maxWd': '최다풍향',
                                'avgTd': '평균이슬점온도',
                                'minRhm': '최소상대습도',
                                'minRhmHrmt': '평균상대습도시각',
                                'avgRhm': '평균상대습도',
                                'avgPv': '평균증기압',
                                'avgPa': '평균현지기압',
                                'maxPs': '최고해면기압',
                                'maxPsHrmt': '최고해면기압시각',
                                'minPs': '최저해면기압',
                                'minPsHrmt': '최저해면기압시각',
                                'avgPs': '평균해면기압',
                                'ssDur': '가조시간',
                                'sumSsHr': '합계일조시간',
                                'hr1MaxIcsrHrmt': '1시간최다일사시각',
                                'hr1MaxIcsr': '1시간최다일사량',
                                'sumGsr': '합계일사량',
                                'ddMefs': '일최심신적설',
                                'ddMefsHrmt': '일최심신적설시각',
                                'ddMes': '일최심적설',
                                'ddMesHrmt': '일최심적설시각',
                                'sumDpthFhsc': '일최심적설시각',
                                'avgTca': '평균전운량',
                                'avgLmac': '평균중하층운량',
                                'avgTs': '평균지면온도',
                                'minTg': '최저초상온도',
                                'avgCm5Te': '평균5cm지중온도',
                                'avgCm10Te': '평균10cm지중온도',
                                'avgCm20Te': '평균20cm지중온도',
                                'avgCm30Te': '평균30cm지중온도',
                                'avgM05Te': '0.5m지중온도',
                                'avgM10Te': '1.0m지중온도',
                                'avgM15Te': '1.5m지중온도',
                                'avgM30Te': '3.0m지중온도',
                                'avgM50Te': '5.0m지중온도',
                                'sumLrgEv': '합계대형증발량',
                                'sumSmlEv': '합계소형증발량',
                                'n99Rn': '9-9강수',
                                'iscs': '일기현상',
                                'sumFogDur': '안개계속시간'
                                })
        for col in df.columns:
            df = df.replace({col: {'': "0"}})
            try:
                fltFlag: bool = False
                for s in df[col]:
                    if s != '' and '.' in s:
                        fltFlag = True
                        break
                if fltFlag:
                    df = df.astype({col: 'float'})
                else:
                    df = df.astype({col: 'int'})
            except Exception:
                df = df.astype({col: 'str'})
        return df
