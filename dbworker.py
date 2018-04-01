#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Mar 22 10:05:36 2018

@author: root
"""
from vedis import Vedis
import config

def get_current_state(user_id):
    with Vedis(config.db_file) as db:
        try:
            return db[user_id]
        except KeyError:
            return config.States.S_START.value
    
def set_state(user_id,value):
    with Vedis(config.db_file) as db:
        try:
            db[user_id]=value
            return True
        except:
            return False
        