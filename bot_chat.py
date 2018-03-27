# -*- coding: utf-8 -*-

import telebot
import config
import dbworker
import RINNEGAN as RN
 #state = dbworker.get_current_state(message.chat.id)
bot = telebot.TeleBot(config.token)

@bot.message_handler(commands=["reset"])
def cmd_reset(message):
    bot.send_message(message.chat.id, "Начнём сначала, введите /start")
    dbworker.set_state(message.chat.id, config.States.S_START.value)

# Начало диалога
@bot.message_handler(commands=["start"])
def cmd_start(message):
    bot.send_message(message.chat.id, "Я создан для того, чтобы служить вам, Владыка.")
    bot.send_message(message.chat.id, "Если желаете найти что-нибудь на барахолках, введите /search")
    bot.send_message(message.chat.id, "Если хотите, чтобы я отслеживал новые лоты, введите /watchdog")
    bot.send_message(message.chat.id, "Если хотите познать множество тайн, введите /help")
    dbworker.set_state(message.chat.id, config.States.S_START.value)
 
@bot.message_handler(commands=["help"],func=lambda message: dbworker.get_current_state(message.chat.id) == config.States.S_START.value)
def cmd_help(message):
    bot.send_message(message.chat.id, "Я создан для того, чтобы служить вам, Владыка.")

    
@bot.message_handler(commands=["search"],func=lambda message: dbworker.get_current_state(message.chat.id) == config.States.S_START.value)
def cmd_search(message):
    bot.send_message(message.chat.id, "Что желаете найти, мой Повелитель?")
    dbworker.set_state(message.chat.id, config.States.S_SEARCH.value)
    
@bot.message_handler(func=lambda message: dbworker.get_current_state(message.chat.id) == config.States.S_SEARCH.value)
def input_lot_name(message):
    global lot_name
    lot_name=message.text
    dbworker.set_state(message.chat.id, config.States.S_RESULT.value)
    bot.send_message(message.chat.id, "Отлично, если хотите увидеть всё, что я нашёл, введите /result")
    bot.send_message(message.chat.id, "Если желаете вывести в порядке возрастания цены, введите /price")
    bot.send_message(message.chat.id, "Если желаете вывести в заданном диапазоне цен, введите /price_filter")
    bot.send_message(message.chat.id, "Если желаете активировать фильтр по названию, введите /name_filter")
    
@bot.message_handler(commands=["result"],func=lambda message: dbworker.get_current_state(message.chat.id) == config.States.S_RESULT.value)
def cmd_result(message):
    global lot_name
    OUT=RN.Items(lot_name)
    OUT.full_result(message.chat.id)
    dbworker.set_state(message.chat.id, config.States.S_START.value)
    
@bot.message_handler(commands=["price"],func=lambda message: dbworker.get_current_state(message.chat.id) == config.States.S_RESULT.value)
def cmd_price(message):
    global lot_name
    OUT=RN.Items(lot_name)
    OUT.sort()
    OUT.full_result(message.chat.id)
    dbworker.set_state(message.chat.id, config.States.S_START.value)
    
@bot.message_handler(commands=["name_filter"],func=lambda message: dbworker.get_current_state(message.chat.id) == config.States.S_RESULT.value)
def cmd_name_filter(message):
    global lot_name
    OUT=RN.Items(lot_name)
    OUT.get_name_filtered(message.chat.id)
    dbworker.set_state(message.chat.id, config.States.S_START.value)
    
@bot.message_handler(commands=["price_filter"],func=lambda message: dbworker.get_current_state(message.chat.id) == config.States.S_RESULT.value)
def cmd_price_filtered(message):
    bot.send_message(message.chat.id, "Пожалуйста, введите цену в формате: минимальная_цена максимальная_цена")
    dbworker.set_state(message.chat.id, config.States.S_PRICE_RANGE.value)

@bot.message_handler(func=lambda message: dbworker.get_current_state(message.chat.id) == config.States.S_PRICE_RANGE.value)
def out_price_range(message):   
    try:
        min_price=float(message.text.split(' ')[0])
        max_price=float(message.text.split(' ')[1])
    except:
        min_price=0
        max_price=10000
    OUT=RN.Items(lot_name)
    OUT.get_price_filtered(message.chat.id,min_price,max_price)
    dbworker.set_state(message.chat.id, config.States.S_START.value)
    
if __name__ == "__main__":
    bot.polling(none_stop=True)

