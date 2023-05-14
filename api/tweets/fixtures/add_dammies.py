import json
import os
import glob
import random
import time
from datetime import datetime
uid=[
    "e5a7959c-696e-4503-968a-1bb6573c17df",
    "795c54b0-6af1-4dfc-ae9a-c34dbfd59406",
    "d49797a1-4a57-4bd4-a908-227431706308",
    "b0293f39-e6f7-4eed-a3b7-ee8b4ca1c47f",
    "e3203429-f71a-4655-9233-e1f33cb16c97",
    "bfa5ca26-1154-49f9-8524-9b39a7a872f8",
    "0ff76bbf-3384-47e4-b927-9389cadd7022",
    "5d4f92cc-be43-4e4c-ae08-adfb0cc71e25",
    "8e53a792-9326-479a-aa0b-ef73da72cedb",
    "868804af-7d57-48e5-a250-eadedb829595",
    "ab9b4724-9339-4115-8b29-fdf2077dc6b8",
    "acb53523-742f-4265-b704-712512005271"
]

dicts = []
for i in range(200):
    datas = {}
    datas["model"]="tweets.tweet"
    datas["pk"]=i+1
    field = {}
    seed = "あいうえおかきくけこさしすせそたちつてとなにぬねのはひふへほまみむめもやゆよらりるれろわをんぁぃぅぇぉヵゃゅょがぎぐげごだぢづでどばびぶべぼ゛，．ぱぴぷぺぽゔざじずぜぞ"
    rpw = ''
    npc_pass = rpw.join([random.choice(seed) for _ in range(random.randint(100,500))])
    field["text"] = npc_pass
    field["user_tweet"]=random.choice(uid)
    field["created_on"]=str(datetime.now())
    field["tweet_img"]="tweet/defo.png"
    datas["fields"]=field
    dicts.append(datas)
    time.sleep(0.0)


for i in range(400):
    datas = {}
    datas["model"]="tweets.comment"
    datas["pk"]=i+1
    field = {}
    seed = "あいうえおかきくけこさしすせそたちつてとなにぬねのはひふへほまみむめもやゆよらりるれろわをんぁぃぅぇぉヵゃゅょがぎぐげごだぢづでどばびぶべぼ゛，．ぱぴぷぺぽゔざじずぜぞ"
    rpw = ''
    npc_pass = rpw.join([random.choice(seed) for _ in range(random.randint(100,500))])
    field["text"] = npc_pass
    field["user_comment"]=random.choice(uid)
    field["tweet"]=random.randint(1,100)
    field["created_on"]=str(datetime.now())
    field["comment_img"]="comment/defo.png"
    datas["fields"]=field
    dicts.append(datas)
    time.sleep(0.5)

for i in range(400):
    datas = {}
    datas["model"]="tweets.retweet"
    datas["pk"]=i+1
    field = {}
    seed = "あいうえおかきくけこさしすせそたちつてとなにぬねのはひふへほまみむめもやゆよらりるれろわをんぁぃぅぇぉヵゃゅょがぎぐげごだぢづでどばびぶべぼ゛，．ぱぴぷぺぽゔざじずぜぞ"
    rpw = ''
    npc_pass = rpw.join([random.choice(seed) for _ in range(random.randint(100,500))])
    field["text"] = npc_pass
    field["retweet_user"]=random.choice(uid)
    field["user_tweet"]=random.randint(1,100)
    field["created_on"]=str(datetime.now())
    datas["fields"]=field
    dicts.append(datas)
    time.sleep(0.5)

with open("./api/tweets/fixtures/dammies.json","w")as f:
    json.dump(dicts,f,indent=4,ensure_ascii=False)