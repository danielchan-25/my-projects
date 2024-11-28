# -*- coding: utf-8 -*-
import json
import requests
import pandas as pd
from datetime import datetime


# 日期：2023-11-14
# 功能：获取 maoming.anjuke.com，每日嘅房价


class GetHousePrice():
    def __init__(self):
        self.year = datetime.today().year  # 用于补充年份
        self.columns = ['date', 'price']
        self.url = 'https://maoming.anjuke.com/esf-ajax/houseprice/pc/trend/report/?city_id=129&id=3294&type=2'
        self.headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/115.0.0.0 Safari/537.36'}

    def get_history_data(self) -> pd.DataFrame():
        ''' 获取历史嘅房价，无历史数据嘅时候用 '''
        try:
            r = requests.get(self.url, headers=self.headers)
            json_data = json.loads(r.text)["data"]["priceTrend"][0]["area"]

            result = []
            for i in json_data:
                result.append([f'{self.year}-{i["date"]}', i['price']])
            df = pd.DataFrame(result, columns=self.columns)
            return df

        except Exception as e:
            print(f'异常错误：{e}')
            return pd.DataFrame([])

    def get_today_data(self) -> pd.DataFrame():
        ''' 获取最新嘅房价，每日追加 '''
        try:
            r = requests.get(self.url, headers=self.headers)
            json_data = json.loads(r.text)["data"]["priceTrend"][0]["area"][0]
            df = pd.DataFrame([[f'{self.year}-{json_data["date"]}', json_data['price']]], columns=self.columns)
            return df

        except Exception as e:
            print(f'异常错误：{e}')
            return pd.DataFrame([])

    def run(self):
        # df = self.get_history_data()
        df = self.get_today_data()
        if not df.empty:
            df.to_csv('HousePrice.csv', mode='a', index=False, header=False)


if __name__ == '__main__':
    GetHousePrice().run()
