# encoding=utf-8
import jieba
import pymongo
import time
import os
import types
import re
from pymongo import MongoClient


def get_connection(collection_name):
    client = MongoClient("zc-slave",27017)
    db = client.jd
    collection = db[collection_name]
    return collection


class MongoWord:
    def __init__(self):
        self.collection = get_connection("comments_sorted")
        self.insert_collect = get_connection("word_for_bayes")
        self.all_words = []

    def deal_with_word(self):
        allComments = self.collection.find({})

        for comments in allComments:
            comment = comments["content"]
            comment_id = comments["comment_id"]
            comment_score = comments["score"]
            classify = 0
            if comment_score > 3.0:
                classify = 0
            elif comment_score == 3.0:
                classify = 1
            elif comment_score < 3.0:
                classify = 2

            comment = re.sub("[\s+\.\!\/_,$%^*(+\"\']+|[+——！，。？?;、~@#￥%……&*（）]+|[0-9]*", "",comment)
            word_list = jieba.lcut(comment)
            print(word_list)
            self.insert_collect.insert({"comment_id": comment_id, "words":word_list,"classify":classify})


cutProcess = MongoWord()
cutProcess.deal_with_word()







