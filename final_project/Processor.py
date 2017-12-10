import requests
import datetime
import json
import pandas as pd
from pandas.tseries.offsets import *

class processor():
    def three_prices(A, B, C, p1, p2, p3):
        res = []
        res1 = one_price(A, p1)
        res2 = one_price(B, p2)
        res3 = one_price(C, p3)

        res.append(res1)
        res.append(res2)
        res.append(res3)

        return res

    def one_price(symbol, price):

        cur_day = pd.Timestamp(datetime.date.today())
        today_check = cur_day.dayofweek

        if today_check == 5:
            cur_day = cur_day - DateOffset(days=1)

        elif today_check == 6:
            cur_day = cur_day - DateOffset(days=2)

        end_date = str(cur_day)
        end_date = end_date[0:10]
        end_date += 'T00:00:00-00'

        start_date = str(cur_day - BDay(7))
        start_date = start_date[0:10]
        start_date += 'T00:00:00-00'


        url = 'http://dev.markitondemand.com/MODApis/Api/v2/InteractiveChart/json?parameters={"Normalized":false,' \
              '"DataPeriod":"Day","StartDate":"' + start_date + '","EndDate":"' + end_date + '",' \
              '"Elements":[{"Symbol":"' + symbol + '","Type":"price","Params":["c"]}]}'


        try:
            r = requests.get(url)
            res = json.loads(r.content)
            res = res["Elements"][0]["DataSeries"]["close"]["values"]
            cur_price = res[-1]
            cur_share = price / cur_price
            prices = []


            for i, j in zip(res, range(-1, -6, -1)):
                if j == -1:
                    prices.append(float("{0:.2f}".format(price)))
                elif j != -1:
                    temp = i * cur_share
                    prices.append(float("{0:.2f}".format(temp)))

            prices.reverse()


        except KeyError:
            print("JSON KeyError")

        return prices