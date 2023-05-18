import json
import os
import glob
import random
import time
from datetime import datetime
ufile = "./accounts/fixtures/uid.json"

with open(ufile,'r') as f:
    uid_json = json.load(f)

uid = uid_json["uid"]
dicts = []
tweet_dicts = []
comment_dicts = []

dicts = []
for i in range(500):
    datas = {}
    datas["model"]="tweets.tweet"
    datas["pk"]=i+1
    field = {}
    seed = "あいうえおかきくけこさしすせそたちつてとなにぬねのはひふへほまみむめもやゆよらりるれろわをんぁぃぅぇぉヵゃゅょがぎぐげごだぢづでどばびぶべぼ゛，．ぱぴぷぺぽゔざじずぜぞ"
    rpw = ''
    npc_pass = rpw.join([random.choice(seed) for _ in range(random.randint(100,500))])
    field["text"] = npc_pass
    field["tweet_user"]=random.choice(uid)
    field["created_on"]=str(datetime.now())
    field["tweet_img"]="tweet/defo.png"
    field["tweet_like"] = random.sample(uid,random.randint(0,50))
    datas["fields"]=field
    dicts.append(datas)
    tweet_dicts.append(datas)

pk=0
for i in range(len(tweet_dicts)):
    for j in range(random.randint(1,30)):
        datas = {}
        field = {}
        datas["model"]="tweets.comment"
        datas["pk"]=pk+1
        
        seed = "あいうえおかきくけこさしすせそたちつてとなにぬねのはひふへほまみむめもやゆよらりるれろわをんぁぃぅぇぉヵゃゅょがぎぐげごだぢづでどばびぶべぼ゛，．ぱぴぷぺぽゔざじずぜぞ"
        rpw = ''
        npc_pass = rpw.join([random.choice(seed) for _ in range(random.randint(100,500))])
        field["text"] = npc_pass
        field["comment_user"]=random.choice(uid)
        field["tweet"]=tweet_dicts[i]["pk"]
        field["created_on"]=str(datetime.now())
        field["comment_img"]="comment/defo.png"
        field["comment_like"] = random.sample(uid,random.randint(0,50))
        datas["fields"]=field
        dicts.append(datas)
        comment_dicts.append(datas)
        pk += 1

pk=0
for i in range(len(tweet_dicts)):
    for j in range(random.randint(1,30)):
        datas = {}
        datas["model"]="tweets.retweet"
        datas["pk"]=pk+1
        field = {}
        seed = "あいうえおかきくけこさしすせそたちつてとなにぬねのはひふへほまみむめもやゆよらりるれろわをんぁぃぅぇぉヵゃゅょがぎぐげごだぢづでどばびぶべぼ゛，．ぱぴぷぺぽゔざじずぜぞ"
        rpw = ''
        npc_pass = rpw.join([random.choice(seed) for _ in range(random.randint(100,500))])
        field["text"] = npc_pass
        field["retweet_user"]=random.choice(uid)
        field["tweet"]=tweet_dicts[i]["pk"]
        field["created_on"]=str(datetime.now())
        field["retweet_like"] = random.sample(uid,random.randint(0,50))
        datas["fields"]=field
        dicts.append(datas)
        pk += 1

os.remove("./tweets/fixtures/dammie_data.json")
with open("./tweets/fixtures/dammie_data.json","w")as f:
    json.dump(dicts,f,indent=4,ensure_ascii=False)