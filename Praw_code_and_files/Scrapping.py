# -*- coding: utf-8 -*-
"""
Created on Fri Dec 06 14:18:36 2019

@author: amelie
"""

import praw
import pandas as pd
import datetime as dt
#%% Data extracted from the tutorial : https://www.storybench.org/how-to-scrape-reddit-with-python/

#Get the data from you credentials.

#### WARNING : current folder must be the one with the "credentials" file
def connect(filename ='Credentials.txt') :
    f = open(filename,'r')
    f = f.read()
    strings = f.split(',')

    for k in range(len(strings)) :
        strings[k] = strings[k].split('=')

    client_id = strings[0][1]
    client_secret = strings[1][1]
    user_agent = strings[2][1]
    username = strings[3][1]
    password = strings[4][1]

    #createa request


    reddit = praw.Reddit(client_id=client_id,
                         client_secret=client_secret,
                         user_agent=user_agent,
                         username=username,
                         password=password)
    return reddit

def get_date(created):
    return dt.datetime.fromtimestamp(created)

def create_db(reddit,theme='HongKong',subtheme='Blizzard',getcomments= False, comm_num = None) :

    subreddit = reddit.subreddit(theme)
    top_subreddit = subreddit.search(subtheme)

    if getcomments :
        topics_dict = { "title":[],
                        "score":[],
                        "id":[], "url":[],
                        "comms_num": [],
                        "created": [],
                        "body":[],
                        "comments" : []}

    else :
        topics_dict = { "title":[],
                        "score":[],
                        "id":[], "url":[],
                        "comms_num": [],
                        "created": [],
                        "body":[]}

    for submission in top_subreddit:

        topics_dict["title"].append(submission.title)
        topics_dict["score"].append(submission.score)
        topics_dict["id"].append(submission.id)
        topics_dict["url"].append(submission.url)
        topics_dict["comms_num"].append(submission.num_comments)
        topics_dict["created"].append(submission.created)
        topics_dict["body"].append(submission.selftext)

        if getcomments :
            submission.comments.replace_more(limit=comm_num)
            comments = submission.comments

            l = []
            for com in comments :
                l.append(com.body)

            topics_dict["comments"].append(l)

    if getcomments :
        topics_data = pd.DataFrame(topics_dict,columns = ['title','score','id','url',
                                                      'comms_num','created','body','comments'])
    else :
        topics_data = pd.DataFrame(topics_dict,columns = ['title','score','id','url',
                                                      'comms_num','created','body'])


    _timestamp = topics_data["created"].apply(get_date)
    topics_data = topics_data.assign(timestamp = _timestamp)
    del topics_data['created']
    #save the data
    if getcomments :
        title = theme +'_' + subtheme+'_andcomments'
    else :
        title = theme +'_' + subtheme+'_nocomments'
    topics_data.to_csv(title+'.csv',encoding='utf-8')

    return topics_data

def get_comments_byid(reddit, id_sub,comm_num= None) :
    comment_dict = {"id":[],"score":[],"author":[],"body":[],"created":[],"replies":[]}
    submission = reddit.submission(id=id_sub)
    submission.comments.replace_more(limit=comm_num)


    for com in submission.comments :
        comment_dict["author"].append(com.author)
        comment_dict["body"].append(com.body)
        comment_dict["id"].append(com.id)
        comment_dict["score"].append(com.score)
        comment_dict["created"].append(com.created_utc)

        replies = com.replies
        l = []
        for rep in replies :
            l.append(rep.body)
        comment_dict["replies"].append(l)


        sub_comments = pd.DataFrame(comment_dict,columns = ['id','score','author','body','created','replies'])


        #save the data

        title = 'sub_' + id_sub+'_'+ submission.title + 'comments'
        sub_comments.to_csv(title+'.csv',encoding='utf-8')


    return sub_comments


#%%
