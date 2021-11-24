# -*- coding: utf-8 -*-
"""
Created on Thu Jan 30 14:36:16 2020

@author: amelie
"""
import requests
import time
import datetime
import pandas as pd
import numpy as np

def get_data(dt, subreddit):
    url = 'https://api.pushshift.io/reddit/search/submission/'
    params = {'subreddit':subreddit, 'after':str(dt), 'size':'500'}
    r = requests.get(url = url, params = params)
    data = r.json()
    return data['data']

def format_data(data):
    df = pd.DataFrame(columns=['id', 'full_link',  'created', 'num_comments', 'selftext', 'title', 'score'])
    for i in data:
        if 'selftext' in i:
            df = df.append(pd.Series([i['id'], i['full_link'], i['created_utc'],
                  i['num_comments'], i['selftext'], i['title'], i['score']],index=df.columns),  ignore_index=True)
        else:
            df = df.append(pd.Series([i['id'], i['full_link'], i['created_utc'],
                  i['num_comments'], '', i['title'], i['score']],index=df.columns),  ignore_index=True)
    return df

def add_date(data):
    df_with_dates = data.copy()
    df_with_dates['datetime'] = df_with_dates['created'].apply(lambda x: datetime.datetime.fromtimestamp(x))
    df_with_dates['date'] = df_with_dates['created'].apply(lambda x: datetime.datetime.fromtimestamp(x).date())

    return df_with_dates


def get_all_posts_from(year =2019,month = 5,day =1,num_loop=40,theme = 'Blizzard') :
    dt1 = int(datetime.datetime(year, month, day).timestamp()) #format the given date
    #create a database :
    df_old = pd.DataFrame(columns=['id', 'full_link',  'created', 'num_comments', 'selftext', 'title', 'score'])
    i = 0
    for i in range(num_loop) :
        data = get_data(dt1, theme)
        new_data = format_data(data)
        df_old = df_old.append(new_data, ignore_index=True)
        if new_data.empty== False :
            dt1 = new_data['created'].iloc[-1]
        else :
            break

    df_old = add_date(df_old) #add the date rather than the timestamp
    if i == num_loop -1 :
        print('Hey ! I iterated until the end and still find some info.')
        print('Please increase the num_loop input')
        print('current num_loop = ' +str(num_loop))
    return df_old

def get_posts_between(date1,date2,df_old_dates) :
    y1,m1,d1 = date1
    y2,m2,d2 = date2
    df_bef_cr = df_old_dates[df_old_dates['date'] >= datetime.date(y1, m1, d1)].copy()
    df_near_cris = df_bef_cr[df_bef_cr['date'] <= datetime.date(y2, m2, d2)].copy()
    df_near_cris = df_near_cris.reset_index()

    return df_near_cris

def get_format_text(text,id_num,language = "en") :

    test_doc =     {
            "language": language,
            "id": id_num,
            "text": text
            }

    return test_doc

def request(test_list_of_doc) :
    url = 'https://northeurope.api.cognitive.microsoft.com/text/analytics/v2.1/sentiment'
    params = {'documents':test_list_of_doc}
    head = {"Ocp-Apim-Subscription-Key":"", 'Content-Type':"application/json",
           "Accept":"application/json"}
    r = requests.post(url = url, json = params, headers = head)
    data = r.json()

    return data



def post_opinion_scores(data,textfield) :
    score_column = -1 * np.ones(len(data))
    post = []
    pas = 500
    for k in range(pas,len(data),pas) :
        doc_list = []
        for i in range(k-pas,k) :
            doc = get_format_text(data[textfield].loc[i],i)
            doc_list.append(doc)

        r = request(doc_list)
        post += r['documents']

    if i < len(data) :
        doc_list = []
        for p in range(i,len(data)) :
            doc = get_format_text(data[textfield].loc[p],p)
            doc_list.append(doc)
        r = request(doc_list)
        post += r['documents']

    return post

def get_column_list(data,post) :
    column = -1 * np.ones(len(data))
    for i in range(len(post)) :
            col_num = int(post[i]['id'])
            column[col_num] = post[i]['score']

    return column

def removed_post_treatment(data) :
    new_data_base = data.copy()
    new_data_base['selftext'] = new_data_base['selftext'].replace('[removed]', '')
    new_data_base['title'] = new_data_base['title'].replace('[removed]', '')
    return new_data_base

def data_base_w_opinions(data) :
    opinion_db = data.copy()

    new = removed_post_treatment(data)
    post_title = post_opinion_scores(new,'title')
    post_text = post_opinion_scores(new,'selftext')

    titles_list = get_column_list(data,post_title)
    text_list = get_column_list(data,post_text)

    opinion_db['title_score'] = titles_list
    opinion_db['text_score'] = text_list

    return opinion_db
