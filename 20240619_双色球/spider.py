# -*- coding: utf-8 -*-
import requests
import pandas as pd
from bs4 import BeautifulSoup


# 日期：2024年7月4日
# 功能：双色球数据爬取
# 定时：23:50


def get_data():
    ''' 获取数据 '''
    rep = requests.get(url, headers=headers)
    if rep.status_code == 200:
        soup = BeautifulSoup(rep.text, 'html.parser')
        tbody = soup.find('tbody', {'id': 'tdata'})  # tbody
        rows = tbody.find_all('tr', {'class': 't_tr1'})
        return rows


def get_history_data(rows):
    ''' 获取历史数据 '''
    data = []
    for i in rows:
        cells = i.find_all('td')
        result = [cell.get_text(strip=True) for cell in cells]
        data.append(result)

    columns = ['期号', '号码1', '号码2', '号码3', '号码4', '号码5', '号码6', '号码7', '快乐星期天', '奖池奖金(元)',
               '一等奖注数', '一等奖奖金(元)', '二等奖注数', '二等奖奖金(元)', '总投注额(元)', '开奖日期']
    return pd.DataFrame(data, columns=columns)


def get_today_data(rows):
    ''' 获取当日数据 '''
    data = [i.text for i in rows[0]][1:]
    return pd.DataFrame([data])


url = 'https://datachart.500.com/ssq/history/newinc/history.php'
headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/126.0.0.0 Safari/537.36",
    "Cookie": "sdc_session=1719821921728; Hm_lvt_4f816d475bb0b9ed640ae412d6b42cab=1719821922; __utma=63332592.589523924.1719821923.1719821923.1719821923.1; __utmc=63332592; __utmz=63332592.1719821923.1.1.utmcsr=(direct)|utmccn=(direct)|utmcmd=(none); __utmt=1; WT_FPC=id=undefined:lv=1719821929714:ss=1719821921727; ck_RegFromUrl=https%3A//kaijiang.500.com/shtml/ssq/03001.shtml; sdc_userflag=1719821921729::1719822117452::5; Hm_lpvt_4f816d475bb0b9ed640ae412d6b42cab=1719822118; __utmb=63332592.4.10.1719821923; motion_id=1719822122793_0.47153631257594086; CLICKSTRN_ID=14.145.51.255-1719821921.698249::7C3B96603560EE8ADC28936B3115B8C2"
}

if __name__ == '__main__':
    # 初次运行时使用，获取历史数据
    # df = get_history_data(get_data())
    # df.to_csv('双色球数据.csv', mode='w', index=False)

    # 每日更新
    df = get_today_data(get_data())
    df.to_csv('双色球数据.csv', mode='a', index=False, header=False)
