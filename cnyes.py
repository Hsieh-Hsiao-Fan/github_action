import requests
import pandas as pd
import json
import datetime as dt

url = "https://api.cnyes.com/media/api/v1/newslist/category/headline"
data = []
payload = {
    "page":1,
    "limit":30,
    "startAt":int((dt.datetime.today() - dt.timedelta(days=1)).timestamp()),
    "endAt":int(dt.datetime.today().timestamp())
}

res = requests.get(url, params= payload)
jd = json.loads(res.text)
data.append(pd.DataFrame(jd["items"]["data"]))

for i in range(2, jd['items']['last_page'] + 1):
    payload['page'] = i
    res = requests.get(url, params= payload)
    jd = json.loads(res.text)
    data.append(pd.DataFrame(jd["items"]["data"]))

df = pd.concat(data, ignore_index=True)
df = df[['newsId', 'title', 'summary']].copy()
df['link'] = df['newsId'].apply(lambda  x: 'https://m.cnyes.com/news/id/' + str(x))#建立連結

df.to_csv('news.csv', encoding = 'utf-8-sig', index = False)

