# -*- coding:<UTF-8> -*-

from pprint import pprint,pformat
import os
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

def debug_var_print(vars,data):
    print("="*50,end="\n")
    print("{} : {}".format(vars, data))
    print("="*50,end="\n")
    
def debug_list_print(var,data):
    print("="*50,end="\n")
    print("{} : ".format(var))
    print(data)
    print("="*50,end="\n")

def error_print(e):
    print("^"*50,end="\n")
    print("{}".format(e))
    print("^"*50,end="\n")
    
def debug_list_pprint(data):
    print("#"*100,end="\n\n")
    pprint(data,indent=4,width=50)
    print("#"*100,end="\n\n")
    
def log_save_print(file):
    print("%"*100,end="\n\n")
    print("save file: {}".format(file))
    print("%"*100,end="\n\n")
    
def debug_list_pprint_none(data):
    if data is None :
        pass
    else:
        print("*"*100,end="\n\n")
        pprint(data,indent=4,width=50)
        print("*"*100,end="\n\n")
        
def debug_var_print_none(vars,data):
    if data is None or data == "":
        pass
    else:
        print("="*50,end="\n")
        print("{} : {}".format(vars, data))
        print("="*50,end="\n")

def debug_test_print(data):
    print("\n\n")
    print("#"*100,end="\n\n")
    pprint(data,indent=4,width=50)
    print("#"*100,end="\n\n")