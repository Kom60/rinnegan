#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import pickle

class User_State():
    def __init__(self,_chat_id,_state):
        self.state=_state
        try:
            self.state=self.read_from_file(_chat_id)
        except:
            self.write_to_file(_chat_id)
       
       
    def get_current_state(self,_chat_id):
        return self.read_from_file(_chat_id)   
    
    def set_state(self,chat_id,value):
        self.write_to_file(chat_id,value)
    
    def write_to_file(self,chat_id,_state):
        dbfile = open(str(chat_id),'wb')
        pickle.dump(_state,dbfile)
        dbfile.close()
                 
    def read_from_file(self,_chat_id):
        try:
            dbfile = open(str(_chat_id),'rb')
            db=pickle.load(dbfile)
            dbfile.close()
            return db
        except:
            return False


     