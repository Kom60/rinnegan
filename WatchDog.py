#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Apr  1 13:56:13 2018

@author: root
"""

import pickle
import telebot
import config

bot = telebot.TeleBot(config.token)

class WatchDogList():
   def clear_list(self,_chat_id):
       dbfile = open('dog_'+str(_chat_id),'wb')
       pickle.dump('',dbfile)
       dbfile.close()
       self.watch_list=[]

   def add_to_list(self,name,_chat_id):
       self.watch_list=self.read_from_file(_chat_id)
       self.watch_list.append(name)
       self.write_to_file(_chat_id)
    
   def write_to_file(self,_chat_id):
       dbfile = open('dog_'+str(_chat_id),'wb')
       pickle.dump(self.watch_list,dbfile)
       dbfile.close()
                
   def read_from_file(self,_chat_id):
       try:
           out=[]
           dbfile = open('dog_'+str(_chat_id),'rb')
           db=pickle.load(dbfile)
           for i in db:
               out.append(i)
           dbfile.close()
           return out
       except:
           return False
       
   def print_watch_list(self,message_chat_id):
       self.watch_list=self.read_from_file(message_chat_id)
       if self.watch_list:
           for i in self.watch_list:
               bot.send_message(message_chat_id,i,'True')
       else:
           bot.send_message(message_chat_id,'Cписок пуст!','True')
           
   def get_watch_list(self,_chat_id):
       return self.read_from_file(_chat_id) 
    
   def __init__(self,_chat_id):
       self.watch_list=[]
       self.write_to_file(_chat_id)
   

    
if __name__ == "__main__":
    bot.polling(none_stop=True)
    