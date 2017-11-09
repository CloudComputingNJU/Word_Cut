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
        self.insert_collect = get_connection("all_words")
        self.all_words = []
    def deal_with_word(self):
        allComments = self.collection.find({})

        for comments in allComments:
            comment = comments["content"]
            comment_id = comments["comment_id"]
            comment = re.sub("[\s+\.\!\/_,$%^*(+\"\']+|[+——！，。？、~@#￥%……&*（）]", "",comment)
            word_list = jieba.lcut(comment)
            print(word_list)
            self.insert_collect.insert({"comment_id": comment_id, "words":word_list})

cutProcess = MongoWord()
cutProcess.deal_with_word()







