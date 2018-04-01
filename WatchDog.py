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
   def clear_list(self):
       dbfile = open('dump','wb')
       pickle.dump('',dbfile)
       dbfile.close()
       self.watch_list=[]

   def add_to_list(self,name):
       self.watch_list.append(name)
       self.write_to_file()
    
   def write_to_file(self):
       dbfile = open('dump','wb')
       pickle.dump(self.watch_list,dbfile)
       dbfile.close()
                
   def read_from_file(self):
       try:
           dbfile = open('dump','rb')
           db=pickle.load(dbfile)
           self.watch_list=db   
           dbfile.close()
       except:
           return False
       
   def print_watch_list(self,message_chat_id):
       if self.watch_list:
           for i in self.watch_list:
               bot.send_message(message_chat_id,i,'True')
       else:
           bot.send_message(message_chat_id,'Cписок пуст!','True')
           
   def get_watch_list(self):
       if self.watch_list:
           out=[]
           for i in self.watch_list:
               out.append(i)
           return out
       else:
           return ''
    
   def __init__(self):
       self.watch_list=[]
   
Z=WatchDogList()          
@bot.message_handler(func=lambda message: True, content_types=['text'])
def input_watch_name(message):
    global Z
    Z.add_to_list(message.text)
    Z.print_watch_list(message.chat.id)
    bot.send_message(message.chat.id, message.text+" успешно добавлен!")
    print(Z.get_watch_list())      

    
if __name__ == "__main__":
    bot.polling(none_stop=True)
    