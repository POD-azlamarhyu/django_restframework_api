import os
from glob import glob
import io
import time
import socket
import sys
import re
from datetime import datetime,date,timedelta,timezone
import calendar as cld
import collections
import pickle
import shutil
import decimal
from .console import *
import math


from .env import *
ROOT="../assets/"

def round_up_to_highest_place(n):
    if n == 0:
        return 0
    
    # 桁数を計算
    digits = len(str(abs(n)))
    
    # 切り上げのための係数を計算
    factor = 10 ** (digits - 1)
    
    # 切り上げ
    result = math.ceil(n / factor) * factor
    return result

def create_derectory(path_name):
    
    if os.path.exists(path_name) is False:
        os.makedirs(path_name)
        os.chown(path_name,uid,gid)
        os.chmod(path_name,permission)

def admin_derectory(path_name):
    os.chown(path_name,uid,gid)
    os.chmod(path_name,permission)

def df_plot_file_glob(path:str):
    unitfile:list[str]= sorted(glob(path),reverse=True)
    # debug_list_pprint(unitfile)
    input_num = 0
    return unitfile[input_num]