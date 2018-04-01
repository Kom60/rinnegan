#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Feb 28 13:44:52 2018

@author: kom60
"""
import telebot
import config
import hmac, hashlib
import pickle
import urllib.parse
import urllib.request
from urllib.request import urlopen,Request
from urllib.error import HTTPError
from urllib.error import URLError
from bs4 import BeautifulSoup
import re

bot = telebot.TeleBot(config.token)


class Item():
    def __init__(self,_header="",_price=0,_link="",_image="https://img.wallpapersafari.com/desktop/1920/1080/30/5/kFTXVI.jpg"):
        self.header=_header
        self.price=float(_price)
        self.link=_link
        self.image=_image
        
    def __len__(self):
        return len(self.header+self.price+self.link+self.image)
    
    def __str__(self):
        return "%s\n %s бел. руб.\n %s\n" %(self.header,self.price,self.link)
    
    def image(self):
        return self.image
    
    def __lt__(self,other):
        return self.price<other.price
    

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

'''
def getWeather():
    try:
        out=[]
        title = getTittle("http://192.168.1.105/")
        out.append(title.find("p1").get_text())
        out.append(title.find("p2").get_text())
        out.append(title.find("p3",).get_text())
        return out
    except:
        return [0,0,0]
'''
    
def ay_search(item_name):
    Item_list=[]
    title = getTittle("http://ay.by/sch/?"+urllib.parse.urlencode({'kwd':item_name}))
    header_link_list=title.findAll("a",{"class":"item-type-card__link"})
    price_list=title.findAll("p",{"class":"item-type-card__info"})
    img_list=title.findAll("img",{"width":"200", "height":"200"})
    if len(header_link_list):
        for i in range(len(header_link_list)):
            header=re.sub("^\s+|\"|\n|\r|\s+$", '', header_link_list[i].get_text())
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
            header=re.sub("^\s+|\"|\n|\r|\s+$", '',header_list[i].get_text())
            try:
                price = float(re.sub("^\s+| |\n|\r|\s+$", '', price_list[i].get_text().split('р')[0].replace(',','.')))
            except:
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
            header=re.sub("^\s+|\"|\n|\r|\s+$", '', link_header_list[i].get_text())
            try:
                price=re.sub("^\s+|\n|\r|\s+$", '', price_list[i].get_text().split(".")[0])
                price=float(price.split('р')[0].replace(',','.'))
            except:
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

def how_many_links(item_name):
    how_many=0
    
    title = getTittle("http://ay.by/sch/?"+urllib.parse.urlencode({'kwd':item_name}))
    ay_links=title.findAll("a",{"class":"item-type-card__link"})
    how_many=how_many+len(ay_links)
    
    link="https://kufar.by/%D0%B1%D0%B5%D0%BB%D0%B0%D1%80%D1%83%D1%81%D1%8C/"+(urllib.parse.urlencode({'':item_name}))[1:]+"--%D0%BF%D1%80%D0%BE%D0%B4%D0%B0%D0%B5%D1%82%D1%81%D1%8F"
    title = getTittle(link)
    kufar_links=title.findAll("a",{"itemprop":"url"})
    how_many=how_many+len(kufar_links)
    
    link="https://baraholka.onliner.by/search.php?"+urllib.parse.urlencode({'q':item_name})
    title = getTittle(link)
    onliner_links=title.findAll("h2",{"class":"wraptxt"})
    how_many=how_many+len(onliner_links)
    return how_many

class Items():     
    def write_to_file(self):
        dbfile = open(self.item_hash,'wb')
        pickle.dump(self.items_list,dbfile)
        dbfile.close()
        
    def check_for_new(self):
        in_db=0
        try:
            dbfile = open(self.item_hash,'rb')
        except:
            return 1
        db=pickle.load(dbfile)
        for lists in db.values():
            in_db=in_db+len(lists)
        if in_db==how_many_links(self.item_name):
            return 0
        else:
            return 1
                
    def read_from_file(self):
        try:
            dbfile = open(self.item_hash,'rb')
            db=pickle.load(dbfile)
            dbfile.close()
            return db   
        except:
            print('can\'t find db named'+str(self.item_name))     
     
        
    def __init__(self,search_item_name):
        self.item_name=search_item_name
        self.item_hash=hmac.new(bytearray(self.item_name,'utf-8'), bytearray('','utf-8'), hashlib.md5).hexdigest() 
        self.items_list={}
        if self.check_for_new():
            self.items_list={'ay':ay_search(self.item_name),'kufar':kufar_search(self.item_name),'onliner':onliner_search(self.item_name)}
            self.write_to_file() 
        else:
            self.items_list=self.read_from_file()
        
    def __len__(self):
        result=0
        for item_len in self.items_list:
            result=result+len(item_len)
        return result
    
    def get_items(self,message_chat_id):
        for Item_list in self.items_list.values():
            for item in Item_list:
                bot.send_message(message_chat_id,item.__str__(), 'True')
                try:
                    bot.send_photo(message_chat_id,item.image)
                except:
                    bot.send_photo(message_chat_id,"http://www.clker.com/cliparts/B/u/S/l/W/l/no-photo-available-md.png")       
  
    def get_name_filtered(self,message_chat_id):
        k=0
        for Item_list in self.items_list.values():
            for item in Item_list:
                if self.item_name.upper() in item.header or self.item_name.lower() in item.header:
                    bot.send_message(message_chat_id,item.__str__(), 'True')
                    k=k+1
                    try:
                        bot.send_photo(message_chat_id,item.image)
                    except:
                        bot.send_photo(message_chat_id,"http://www.clker.com/cliparts/B/u/S/l/W/l/no-photo-available-md.png") 
        if k==0:
            bot.send_message(message_chat_id,item.__str__(), 'Ничего подходящего нет, Владыка.')
            
    def get_price_filtered(self,message_chat_id,low=0,hight=100000):
        k=0
        for Item_list in self.items_list.values():
            for item in Item_list:
                if item.price > low and item.price < hight:
                    bot.send_message(message_chat_id,item.__str__(), 'True')
                    k=k+1
                    try:
                        bot.send_photo(message_chat_id,item.image)
                    except:
                        bot.send_photo(message_chat_id,"http://www.clker.com/cliparts/B/u/S/l/W/l/no-photo-available-md.png") 
        if k==0:
            bot.send_message(message_chat_id,item.__str__(), 'Ничего подходящего нет, Владыка.')
        
            
          
    def full_result(self,message_chat_id):
        if len(self):
            self.get_items(message_chat_id)
        else:
            bot.send_message(message_chat_id,"Простите Босс, я ничего не нашёл.", 'True')
                
    def sort(self):
        for Item_list in self.items_list.values():
            Item_list.sort()


          
    def print_new(self,message_chat_id):
        if self.check_for_new():
            try:
                dbfile = open(self.item_hash,'rb')
                old_items=pickle.load(dbfile)
                dbfile.close()
            except:
                print('db not found!')            
            new_items=Items(self.item_name)
            #out=[]
            for new_item in new_items.items_list.values():
                for item in new_item:
                    if item not in old_items:
                         bot.send_message(message_chat_id,item.__str__(), 'True')
                         try:
                             bot.send_photo(message_chat_id,item.image)
                         except:
                             bot.send_photo(message_chat_id,"http://www.clker.com/cliparts/B/u/S/l/W/l/no-photo-available-md.png")                            
        else:
            bot.send_message(message_chat_id,'Нет новых лотов!')

