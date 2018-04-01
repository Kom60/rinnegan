#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Mar 22 10:09:46 2018

@author: root
"""

from enum import Enum

token="550900373:AAGBco24Kw9sKCryxDFiGX657p8Adqc34mk"
db_file = "state.vdb"
dog_file = "watchlist.vdb"

class States(Enum):
    S_START="0"
    S_SEARCH="1"
    S_WATCHDOG="2"
    S_WATCHLIST="3"
    S_HELP="4"
    S_SET_PLACE="5"
    S_FILTER="6"
    S_FILTER_PRICE="7"
    S_FILTER_NAME="8"
    S_NO_FILTER="9"
    S_WATCHLIST_DELETE="10"
    S_WATCHLIST_ADD="11"
    S_WATCHLIST_CLEAR="12"
    S_RESULT="13"
    S_PRICE_RANGE="14"
    S_WATCHDOG_ON="15"