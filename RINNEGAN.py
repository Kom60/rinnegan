#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Feb 28 13:44:52 2018

@author: kom60
"""
import urllib.parse
import urllib.request
from urllib.request import urlopen,Request
from urllib.error import HTTPError
from urllib.error import URLError
from bs4 import BeautifulSoup
import re
import telebot
import sqlite3 as sql
#from telebot import util
import time
import hmac, hashlib

token="548898691:AAFbphBpkqr3wJ3G5LH2tbeYUWxFhI8yFS4"

bot = telebot.TeleBot(token)

def getTittle(url):
    hdr = {'User-Agent': 'Mozilla/5.0'}
    try:
        req = Request(url,headers=hdr)
        html=urlopen(req)
    except HTTPError as e:
        print("Can't open "+ url[:15]+"page!")
        return None
    except URLError as e:
        print("URL Error!")
        return None
    try:
        bsObj = BeautifulSoup(html,"lxml")
    except AttributeError as e:
        print("Can't find atribute!")
        return None
    return bsObj   

def getWeather():
    out=[]
    title = getTittle("http://192.168.1.105/")
    out.append(title.find("p1").get_text())
    out.append(title.find("p2").get_text())
    out.append(title.find("p3",).get_text())
    return out
    
def ay_search(item_name):
    Item_list=[]
    title = getTittle("http://ay.by/sch/?"+urllib.parse.urlencode({'kwd':item_name}))
    header_link_list=title.findAll("a",{"class":"item-type-card__link"})
    price_list=title.findAll("p",{"class":"item-type-card__info"})
    img_list=title.findAll("img",{"width":"200", "height":"200"})
    if len(header_link_list):
        for i in range(len(header_link_list)):
            header=re.sub("^\s+|\n|\r|\s+$", '', header_link_list[i].get_text())
            try:
                price = float(re.sub("^\s+|\n|\r|\s+$", '',price_list[i].get_text())[10:29].split('б')[0].replace(',','.'))
            except:
                price=0.0
            if 'href' in header_link_list[i].attrs:
                link=header_link_list[i].attrs['href']
            if 'src' in img_list[i].attrs:
                image=img_list[i].attrs['src']
            Item_list.append(Item(header,price,link,image))
        return Item_list
    else:
        return Item_list       
    

def kufar_search(item_name):
    Item_list=[]
    link="https://kufar.by/%D0%B1%D0%B5%D0%BB%D0%B0%D1%80%D1%83%D1%81%D1%8C/"+(urllib.parse.urlencode({'':item_name}))[1:]+"--%D0%BF%D1%80%D0%BE%D0%B4%D0%B0%D0%B5%D1%82%D1%81%D1%8F"
    title = getTittle(link)
    header_list=title.findAll("a",{"class":"list_ads__title"})
    price_list=title.findAll("b",{"class":"list_ads__price"})
    img_link_list=title.findAll("a",{"itemprop":"url"})
    if len(header_list):
        for i in range(len(header_list)):
            header=header_list[i].get_text()
            if price_list[i].get_text() and (price_list[i].get_text().find('Дого'))!=True:
                price = float(re.sub("^\s+| |\n|\r|\s+$", '', price_list[i].get_text().split('р')[0].replace(',','.')))
            else:
                price=0
            if 'href' in img_link_list[i].attrs:
                link=img_link_list[i].attrs['href']
            if 'data-images' in img_link_list[i].attrs:
                if img_link_list[i].attrs['data-images'].split(",")[0]:
                    image="https://content.kufar.by/mobile_thumbs"+ img_link_list[i].attrs['data-images'].split(",")[0]
                else :
                    image="NO PHOTO!"
            Item_list.append(Item(header,price,link,image))
        return Item_list
    else:
        return Item_list
    
def onliner_search(item_name):
    Item_list=[]
    link="https://baraholka.onliner.by/search.php?"+urllib.parse.urlencode({'q':item_name})
    title = getTittle(link)
    link_header_list=title.findAll("h2",{"class":"wraptxt"})
    price_list=title.findAll("td",{"class":"cost","class":"cost"})
    if len(link_header_list):
        i=0
        for img in link_header_list:
            header=re.sub("^\s+|\n|\r|\s+$", '', link_header_list[i].get_text())
            if(re.sub("^\s+|\n|\r|\s+$", '', price_list[i].get_text().split(".")[0])):
                price=re.sub("^\s+|\n|\r|\s+$", '', price_list[i].get_text().split(".")[0])
                price=float(price.split('р')[0].replace(',','.'))
            else:
                price=0
            if 'href' in link_header_list[i].find("a").attrs:
                link="https://baraholka.onliner.by"+img.find("a").attrs['href']
                title=getTittle(link)               
                try:
                    image=title.find("img",{"class":"msgpost-img"}).attrs['src']
                except:
                    image='http://www.clker.com/cliparts/B/u/S/l/W/l/no-photo-available-md.png'
            i=i+1
            Item_list.append(Item(header,price,link,image))
        return Item_list
    else:
        return Item_list


class Item():
    def __init__(self,_header="",_price=0,_link="",_image="https://img.wallpapersafari.com/desktop/1920/1080/30/5/kFTXVI.jpg"):
        self.header=_header
        self.price=_price
        self.link=_link
        self.image=_image
        
    def __len__(self):
        return len(self.header+self.price+self.link+self.image)
    
    def __str__(self):
        return "%s\n %s бел. руб.\n %s\n" %(self.header,self.price,self.link)
    
    def database(self):
        return (self.header,self.price,self.link,self.image)
    
    def image(self):
        return self.image
    
    def __lt__(self,other):
        return self.price<other.price
    
class Items():     
    def write_sql(self):
        conn = sql.connect(self.item_hash)
        curs=conn.cursor()     
        try:
            td='create table ay_'+self.item_hash+' (header char(150),price float(10),link char(180),image char(150))' 
            curs.execute(td)
        except:
            pass
        for item in self.ay_list:
            curs.execute('insert into ay_'+self.item_hash+' values (?,?,?,?)',item.database())
            
            ''' if (curs.execute('select * from ay_'+self.item_hash+' where link = ?',[item.link])):
                pass
            else:'''
            
                
        try:
            td='create table ku_'+self.item_hash+' (header char(150),price float(10),link char(180),image char(150))' 
            curs.execute(td)
        except:
            pass
        for item in self.kufar_list:
            curs.execute('insert into ku_'+self.item_hash+' values (?,?,?,?)',item.database())
            
            '''if (curs.execute('select * from ku_'+self.item_hash+' where link = ?',[item.link])):
                pass
            else:'''
            
                
        try:
            td='create table onliner_'+self.item_hash+' (header char(150),price float(10),link char(180),image char(150))' 
            curs.execute(td)
        except:
            pass
        for item in self.onliner_list:
            curs.execute('insert into onliner_'+self.item_hash+' values (?,?,?,?)',item.database())
            
            '''if (curs.execute('select * from onliner_'+self.item_hash+' where link = ?',[item.link])):
                pass
            else:'''
            
                
        conn.commit()
    
    def __init__(self,search_item_name): 
        self.onliner_list=onliner_search(search_item_name)
        self.ay_list=ay_search(search_item_name)
        self.kufar_list=kufar_search(search_item_name)
        self.item_name=search_item_name
        self.item_hash=hmac.new(bytearray(self.item_name,'utf-8'), bytearray('','utf-8'), hashlib.md5).hexdigest()
        self.write_sql()
        
       
        
         #   curs.execute('insert into '+ str(item_hash) + ' values (?,?,?,?)',item.database())
        #curs.executemany('insert into some values (?,?,?,?)',self.ay_list)
        #curs.executemany('insert into some values (?,?,?,?)',self.kufar_list)
        #print(curs.rowcount)
        #print(sql.paramstyle)
        #conn.commit()w
        #curs.execute('select * from '+ str(item_hash))
        #for row in curs.fetchall():
         #   print(row)
        
    def __len__(self):
        return len(self.ay_list+self.kufar_list+self.onliner_list)
    
    def get_items(self,message_chat_id,Item_list):
        for item in Item_list:
            bot.send_message(message_chat_id,item.__str__(), 'True')
            try:
                bot.send_photo(message_chat_id,item.image)
            except:
                bot.send_photo(message_chat_id,"http://www.clker.com/cliparts/B/u/S/l/W/l/no-photo-available-md.png")       
            
    def full_result(self,message_chat_id):
        if len(self):
            self.get_items(message_chat_id,self.ay_list)
            #time.sleep(1)
            self.get_items(message_chat_id,self.kufar_list)
            #time.sleep(1)
            self.get_items(message_chat_id,self.onliner_list)
        else:
            bot.send_message(message_chat_id,"Простите Босс, я ничего не нашёл.", 'True')
                
    def sort(self):
        self.ay_list.sort()
        self.kufar_list.sort()
        self.onliner_list.sort()
    
        
        
            

@bot.message_handler(commands=['start'])
def find_file_id(message):
    message.text="Я создан служить вам, просто скажите, что я должен найти."
    bot.send_message(message.chat.id,message.text, 'True')
    bot.send_photo(message.chat.id, "https://img.wallpapersafari.com/desktop/1920/1080/30/5/kFTXVI.jpg");   
         
   
   
@bot.message_handler(commands=['weather'])
def find_file_id(message):
    out=getWeather()
    message.text="Temp= "+out[0]+"C, P = " + out[1] + ", Hum = " + out[2]+" %. "
    bot.send_message(message.chat.id,message.text, 'True')   
   
@bot.message_handler(func=lambda message: True, content_types=['text'])
def outler(message):  
    Z=Items(message.text)
    #Z.sort()
    Z.full_result(message.chat.id)


if __name__ == '__main__':
    bot.polling(none_stop=True)
