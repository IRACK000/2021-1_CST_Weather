# -*- coding: utf-8 -*-
'''''''''''''''''''''''''''''''''''''''''''''''''''''''''
### Alias : hours.py & Last Modded : 2021.05.31. ###
'''''''''''''''''''''''''''''''''''''''''''''''''''''''''
import os
import json
import pandas as pd
from urllib.request import Request, urlopen
from urllib.parse import urlencode, quote_plus

# read config file
from configparser import ConfigParser
config = ConfigParser()
config.read(os.path.dirname(os.path.realpath(__file__)) + "/key.config")  # https://codechacha.com/ko/python-examples-get-working-directory/
API_KEY = config.get('dataportal', 'decodedkey')


# get data from https://data.kma.go.kr/data/grnd/selectAsosRltmList.do?pgmNo=36
url = 'http://apis.data.go.kr/1360000/AsosHourlyInfoService/getWthrDataList'
queryParams = '?' + urlencode({quote_plus('ServiceKey'): API_KEY,
                               quote_plus('pageNo'): '1',
                               quote_plus('numOfRows'): '999',
                               quote_plus('dataType'): 'JSON',
                               quote_plus('dataCd'): 'ASOS',
                               quote_plus('dateCd'): 'HR',
                               quote_plus('startDt'): '20210101',
                               quote_plus('startHh'): '01',
                               quote_plus('endDt'): '20210530',
                               quote_plus('endHh'): '01',
                               quote_plus('stnIds'): '133'
                               })

request = Request(url + queryParams)
request.get_method = lambda: 'GET'
with urlopen(request) as opened:
    response = opened.read().decode('utf-8')
    item = json.loads(response)['response']['body']['items']['item']
    df = pd.DataFrame(item)
    for col in df.columns:
        if "Qcflg" in col:
            del df[col]
    del df['ss'], df['rnum'], df['stnId'], df['clfmAbbrCd']

print(df)
