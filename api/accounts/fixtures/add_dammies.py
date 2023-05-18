import json
import os
import glob
import random
import time
from datetime import datetime
import uuid
import string
import os
import sys
import hashlib
from passlib.hash import pbkdf2_sha256

uid = []
dicts = []
for i in range(100):
    datas = {}
    datas["model"]="accounts.user"
    u_id = str(uuid.uuid4())
    uid.append(u_id)
    datas["pk"]=str(u_id)
    field = {}
    # seed = "あいうえおかきくけこさしすせそたちつてとなにぬねのはひふへほまみむめもやゆよらりるれろわをんぁぃぅぇぉヵゃゅょがぎぐげごだぢづでどばびぶべぼ゛，．ぱぴぷぺぽゔざじずぜぞ"
    seed = "1234567890abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ!@#$^&*()-=+_<>"
    
    rpw = ''
    npc = rpw.join([random.choice(seed) for _ in range(random.randint(10,20))])
    
    
    email_seed = "1234567890abcdefghijklmnopqrstuvwxyz"
    email_semi_list = ["_","."]
    email_domain = ["@meme.co.jp","@netmeme.jp","@inmeme.jp","@meme.com","@inmeme.jp",'@googlemail.com','@yahoooo.co.jp','@unko.co.jp','@manko.jp','@sappro.go.jp','@manko.us','@ace.co.jp',"@netmeme.go.jp","@netmeme.com"]
    if random.randint(1,3) == 1:
        e_mail = ''.join([random.choice(email_seed) for _ in range(random.randint(5,30))])
        email = e_mail+str(random.choice(email_domain))
    elif random.randint(1,3) == 2:
        e_mail = ''.join([random.choice(email_seed) for _ in range(random.randint(5,30))])
        mail_e = ''.join([random.choice(email_seed) for _ in range(random.randint(5,30))])
        email = e_mail+str(random.choice(email_semi_list))+mail_e+str(random.choice(email_domain))
    else:
        e_mail = ''.join([random.choice(email_seed) for _ in range(random.randint(5,30))])
        mail_e = ''.join([random.choice(email_seed) for _ in range(random.randint(5,30))])
        email = e_mail+str(random.choice(email_semi_list))+mail_e+str(random.choice(email_semi_list))+mail_e+str(random.choice(email_domain))
    field["email"]=email
    field["password"] = pbkdf2_sha256.hash(npc)
    datas["fields"]=field
    dicts.append(datas)
    time.sleep(0.2)

for i in range(len(uid)):
    seed = "あいうえおかきくけこさしすせそたちつてとなにぬねのはひふへほまみむめもやゆよらりるれろわをんぁぃぅぇぉヵゃゅょがぎぐげごだぢづでどばびぶべぼ゛，．ぱぴぷぺぽゔざじずぜぞ"
    datas = {}
    datas["model"]="accounts.userprofile"
    datas["pk"]=i+1
    field = {}
    field["nickname"] = ''.join([random.choice(seed) for _ in range(random.randint(5,30))])
    field["user_profile"] = uid[i]
    idseed = "abcdefghijklmnopqrstuvwxyz________1234567890"
    field["account_id"] = ''.join([random.choice(idseed) for _ in range(random.randint(5,30))])
    bioseed ="あいうえおかきくけこさしすせそたちつてとなにぬねのはひふへほまみむめもやゆよらりるれろわをんぁぃぅぇぉヵゃゅょがぎぐげごだぢづでどばびぶべぼ゛，．ぱぴぷぺぽゔざじずぜぞ():,./?';`~!@#$^&*<>" 
    field["bio"] = ''.join([random.choice(bioseed) for _ in range(random.randint(5,30))])
    field["created_on"] = str(datetime.now())
    field["icon"]="icon/defo.png"
    field["link"]="http://localhost:8080"
    datas["fields"]=field
    dicts.append(datas)
    time.sleep(0.2)
for i in range(len(uid)):
    seed = "あいうえおかきくけこさしすせそたちつてとなにぬねのはひふへほまみむめもやゆよらりるれろわをんぁぃぅぇぉヵゃゅょがぎぐげごだぢづでどばびぶべぼ゛，．ぱぴぷぺぽゔざじずぜぞ"
    datas = {}
    datas["model"]="accounts.userchannel"
    datas["pk"]=i+1
    field = {}
    field["channel_name"] = ''.join([random.choice(seed) for _ in range(random.randint(5,30))])
    field["user_channel"] = uid[i]
    idseed = "abcdefghijklmnopqrstuvwxyz________1234567890"
    field["channel_id"] = ''.join([random.choice(idseed) for _ in range(random.randint(5,30))])
    bioseed ="あいうえおかきくけこさしすせそたちつてとなにぬねのはひふへほまみむめもやゆよらりるれろわをんぁぃぅぇぉヵゃゅょがぎぐげごだぢづでどばびぶべぼ゛，．ぱぴぷぺぽゔざじずぜぞ():,./?';`~!@#$^&*<>" 
    # field["bio"] = ''.join([random.choice(bioseed) for _ in range(random.randint(5,30))])
    field["created_on"] = str(datetime.now())
    field["channel_icon"]="channel_icon/defo.png"
    field["channel_cover"]="channel_cover/defo.png"
    
    datas["fields"]=field
    dicts.append(datas)
# for i in range(400):
#     datas = {}
#     datas["model"]="tweets.comment"
#     datas["pk"]=i+1
#     field = {}
#     seed = "あいうえおかきくけこさしすせそたちつてとなにぬねのはひふへほまみむめもやゆよらりるれろわをんぁぃぅぇぉヵゃゅょがぎぐげごだぢづでどばびぶべぼ゛，．ぱぴぷぺぽゔざじずぜぞ"
#     rpw = ''
#     npc_pass = rpw.join([random.choice(seed) for _ in range(random.randint(100,500))])
#     field["text"] = npc_pass
#     field["user_comment"]=random.choice(uid)
#     field["tweet"]=random.randint(1,100)
#     field["created_on"]=str(datetime.now())
#     field["comment_img"]="comment/defo.png"
#     datas["fields"]=field
#     dicts.append(datas)
#     time.sleep(0.5)

# for i in range(400):
#     datas = {}
#     datas["model"]="tweets.retweet"
#     datas["pk"]=i+1
#     field = {}
#     seed = "あいうえおかきくけこさしすせそたちつてとなにぬねのはひふへほまみむめもやゆよらりるれろわをんぁぃぅぇぉヵゃゅょがぎぐげごだぢづでどばびぶべぼ゛，．ぱぴぷぺぽゔざじずぜぞ"
#     rpw = ''
#     npc_pass = rpw.join([random.choice(seed) for _ in range(random.randint(100,500))])
#     field["text"] = npc_pass
#     field["retweet_user"]=random.choice(uid)
#     field["user_tweet"]=random.randint(1,100)
#     field["created_on"]=str(datetime.now())
#     datas["fields"]=field
#     dicts.append(datas)
#     time.sleep(0.5)

uuid_dict ={}
uuid_dict["uid"] = uid
os.remove("./accounts/fixtures/dammie_data.json")
with open("./accounts/fixtures/dammie_data.json","w")as f:
    json.dump(dicts,f,indent=4,ensure_ascii=False)
    
with open("./accounts/fixtures/uid.json","w") as f:
    json.dump(uuid_dict,f,indent=4,ensure_ascii=False)