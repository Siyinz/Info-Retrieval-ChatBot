from flask import Flask, render_template, request
import csv

import pandas as pd
import numpy as np
from rank_bm25 import BM25Okapi
###########
def data_process(train_data,test_data,whole_data):
    #### READ Train, test, and all replies data ####
    file = open(train_data)
    read_csv = csv.reader(file)
    train = []
    for row in read_csv:
        train.append(row)
    train= train[1:]
    train = pd.DataFrame(train,columns=['message_id','response_id','rating'])

    file = open(test_data)
    read_csv = csv.reader(file)
    test = []
    for row in read_csv:
        test.append(row)
    test= test[1:]
    test = pd.DataFrame(test,columns=['message_id','response_id'])

    tsv = open(whole_data)
    read_tsv = csv.reader(tsv, delimiter="\t")
    data =[]
    for row in read_tsv:
        data.append(row)
    data = pd.DataFrame(data)
    data.rename(columns=data.iloc[0], inplace = True)
    data.drop([0], inplace = True)

    #### Merge data ####################################
    merged_train = pd.merge(train[['message_id']], data[['message_id','message']].drop_duplicates(subset="message_id"), on='message_id', how='left')
    merged_test = pd.merge(test[['message_id']], data[['message_id','message']].drop_duplicates(subset="message_id"), on='message_id', how='left')
    merged2 = pd.merge(train[['response_id','rating']], data[['response_id','response']], on='response_id', how='left')
    merged3 = pd.merge(test[['response_id']], data[['response_id','response']], on='response_id', how='left')

    merged_train['response_id'] = list(merged2['response_id'])
    merged_train['response'] = list(merged2['response'])
    merged_train['rating']= list(merged2['rating'])

    merged_test['response_id'] = list(merged3['response_id'])
    merged_test['response'] = list(merged3['response'])
    ### save to csv
    merged_train[['response']].to_csv('response_without_id_train.csv',index=False)
    merged_test[['response']].to_csv('response_without_id_test.csv',index=False)
    merged_train.to_csv('merged_train.csv',index=False)
    merged_test.to_csv('merged_test.csv',index=False)

    #### get message #####
    me = merged_train[['message']].drop_duplicates(subset="message")
    melist = me['message'].to_list()
    with open('query_train.txt', 'w') as filehandle:
        filehandle.writelines("%s\n" % reid for reid in melist)

    onlyme = merged_test[['message']].drop_duplicates(subset="message")
    melist = onlyme['message'].to_list()
    with open('query_test.txt', 'w') as filehandle:
        filehandle.writelines("%s\n" % reid for reid in melist)


app = Flask(__name__)


@app.route("/")
def home():
    return render_template("home.html")

@app.route("/get")
def get_bot_response():
    
    what_the_user_said = request.args.get('msg')
    #train_path = 'message_without_id_train.csv'
    train_path_res = 'response_without_id_train.csv'

    #### the following code is to use two bm25, match query to message first and then match message to response
    # file = open(train_path)
    # read_csv = csv.reader(file)
    # corpus1 = []
    # for row in read_csv:
    #     corpus1.append(row[0])
    # tokenized_corpus = [doc.split(" ") for doc in corpus1]
    # bm25 = BM25Okapi(tokenized_corpus)
    # tokenized_query = what_the_user_said.split(" ")
    # doc_scores = bm25.get_scores(tokenized_query)
    # result = bm25.get_top_n(tokenized_query, corpus1, n=1)

    # query = result[0]

    # message = pd.read_csv('merged_train.csv')
    # message['re_id']=message['response_id']+' '+ message['response']
    # message_id = message[['message_id']].drop_duplicates(subset="message_id")['message_id'].to_list()
    # corpus = []
    # for i in message_id:
    #     response = message[message['message_id']==i]['re_id'].to_list()
    #     corpus.append(response)
    
    # q = []
    # with open('query_train.txt') as file:
    #     for i in file:
    #         q.append(i.strip())

    # corpus_index = q.index(query)

    # tokenized_corpus1 = [doc.split(" ") for doc in corpus[corpus_index]]
    # BM25 = BM25Okapi(tokenized_corpus1)
    # tokenized_query1 = what_the_user_said.split(" ")
    # doc_scores1 = BM25.get_scores(tokenized_query1)
    # result1 = BM25.get_top_n(tokenized_query1, corpus[corpus_index], n=10)


    # if len(result1) !=0:
    #     return result1[0].split(' ', 1)[1]

    file = open(train_path_res)
    read_csv = csv.reader(file)
    corpus = []
    for row in read_csv:
        corpus.append(row[0])
    tokenized_corpus = [doc.split(" ") for doc in corpus]
    bm25 = BM25Okapi(tokenized_corpus)
    tokenized_query = what_the_user_said.split(" ")
    doc_scores = bm25.get_scores(tokenized_query)
    result = bm25.get_top_n(tokenized_query, corpus, n=1)

    if len(result) !=0:
        return result[0]
    else:
        return "I don't know"

if __name__ == "__main__":

    train_data = "aggregated-hw3-ratings.train.csv"
    test_data ="aggregated-hw3-rating.test.csv"
    whole_data = "chatbot-replies.tsv"
    data_process(train_data,test_data,whole_data)
    app.run()

