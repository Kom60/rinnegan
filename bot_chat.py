# -*- coding: utf-8 -*-

import telebot
import config
import dbworker
import _thread,time
import RINNEGAN as RN
import WatchDog as WD


bot = telebot.TeleBot(config.token)

global State
State=dbworker.User_State('1',config.States.S_START.value)


def watch_dog_funk(OUT,message_chat_id):
    while True:
        time.sleep(60)
        for item in OUT:
            item.print_new(message_chat_id)

@bot.message_handler(commands=["reset"])
def cmd_reset(message):
    global Watch_Dog
    Watch_Dog=WD.WatchDogList(message.chat.id)
    Watch_Dog.read_from_file(message.chat.id)
    global State
    State=dbworker.User_State(message.chat.id,config.States.S_START.value) 
    State.set_state(message.chat.id, config.States.S_START.value)
    bot.send_message(message.chat.id, "Начнём сначала, введите /start")    

# Начало диалога
@bot.message_handler(commands=["start"])
def cmd_start(message):
    global State
    State.set_state(message.chat.id, config.States.S_START.value)
    bot.send_message(message.chat.id, "Я создан для того, чтобы служить вам, Владыка.")
    bot.send_message(message.chat.id, "Если желаете найти что-нибудь на барахолках, введите /search")
    bot.send_message(message.chat.id, "Если хотите, чтобы я отслеживал новые лоты, введите /watchdog")
    bot.send_message(message.chat.id, "Если хотите познать множество тайн, введите /help")
    
 
@bot.message_handler(commands=["watchdog"],func=lambda message: State.get_current_state(message.chat.id) == config.States.S_START.value)
def cmd_watchdog(message):
    State.set_state(message.chat.id, config.States.S_WATCHDOG.value)
    bot.send_message(message.chat.id, "Я могу отслеживать новые лоты, Владыка..")    
    bot.send_message(message.chat.id, "Чтобы добавить новый лот, введите /add")
    bot.send_message(message.chat.id, "Чтобы вывести список отслеживаемых товаров, введите /watchlist")
    bot.send_message(message.chat.id, "Чтобы очистить список, введите /delete")
    bot.send_message(message.chat.id, "Чтобы я начал отслеживать лоты, введите /dog_start")
    
    #bot.send_message(message.chat.id, "Чтобы добавить новый лот, введите /add")
@bot.message_handler(commands=["dog_start"],func=lambda message: State.get_current_state(message.chat.id) == config.States.S_WATCHDOG.value)
def cmd_dog_start(message):
    global Watch_Dog
    OUT=[]
    for name in Watch_Dog.get_watch_list(message.chat.id):
        OUT.append(RN.Items(str(name)))
    _thread.start_new_thread(watch_dog_funk,(OUT,message.chat.id,))
    
    
    
@bot.message_handler(commands=["add"],func=lambda message: State.get_current_state(message.chat.id) == config.States.S_WATCHDOG.value)
def cmd_add(message):
    State.set_state(message.chat.id, config.States.S_WATCHLIST_ADD.value)
    bot.send_message(message.chat.id, "Введите пожалуйста имя добавляемого лота")
    
    
@bot.message_handler(func=lambda message: State.get_current_state(message.chat.id) == config.States.S_WATCHLIST_ADD.value)
def input_watch_name(message):
    State.set_state(message.chat.id, config.States.S_WATCHDOG.value)
    global Watch_Dog
    Watch_Dog.add_to_list(message.text,message.chat.id)
    bot.send_message(message.chat.id, message.text+" успешно добавлен!")
    bot.send_message(message.chat.id, "Чтобы добавить новый лот, введите /add")
    bot.send_message(message.chat.id, "Чтобы вывести список отслеживаемых товаров, введите /watchlist")
    bot.send_message(message.chat.id, "Чтобы очистить список, введите /delete")
    bot.send_message(message.chat.id, "Чтобы я начал отслеживать лоты, введите /dog_start")
    
@bot.message_handler(commands=["watchlist"],func=lambda message: State.get_current_state(message.chat.id) == config.States.S_WATCHDOG.value)
def cmd_watchlist(message):
    State.set_state(message.chat.id, config.States.S_WATCHDOG.value)
    global Watch_Dog
    Watch_Dog.print_watch_list(message.chat.id)
        
@bot.message_handler(commands=["delete"],func=lambda message: State.get_current_state(message.chat.id) == config.States.S_WATCHDOG.value)
def cmd_delete(message):
    Watch_Dog.clear_list(message.chat.id)
    bot.send_message(message.chat.id, "Список успешно очищен!")
    
@bot.message_handler(commands=["help"],func=lambda message: State.get_current_state(message.chat.id) == config.States.S_START.value)
def cmd_help(message):
    bot.send_message(message.chat.id, "Я создан для того, чтобы служить вам, Владыка.")

    
@bot.message_handler(commands=["search"],func=lambda message: State.get_current_state(message.chat.id) == config.States.S_START.value)
def cmd_search(message):
    State.set_state(message.chat.id, config.States.S_SEARCH.value)
    bot.send_message(message.chat.id, "Что желаете найти, мой Повелитель?")
    
@bot.message_handler(func=lambda message: State.get_current_state(message.chat.id) == config.States.S_SEARCH.value)
def input_lot_name(message):
    State.set_state(message.chat.id, config.States.S_RESULT.value)
    global lot_name
    lot_name=message.text
    bot.send_message(message.chat.id, "Отлично, если хотите увидеть всё, что я нашёл, введите /result")
    bot.send_message(message.chat.id, "Если желаете вывести в порядке возрастания цены, введите /price")
    bot.send_message(message.chat.id, "Если желаете вывести в заданном диапазоне цен, введите /price_filter")
    bot.send_message(message.chat.id, "Если желаете активировать фильтр по названию, введите /name_filter")
    
@bot.message_handler(commands=["result"],func=lambda message: State.get_current_state(message.chat.id) == config.States.S_RESULT.value)
def cmd_result(message):
    State.set_state(message.chat.id, config.States.S_START.value)
    OUT=RN.Items(lot_name)
    OUT.full_result(message.chat.id)
    
@bot.message_handler(commands=["price"],func=lambda message: State.get_current_state(message.chat.id) == config.States.S_RESULT.value)
def cmd_price(message):
    State.set_state(message.chat.id, config.States.S_START.value)
    OUT=RN.Items(lot_name)
    OUT.sort()
    OUT.full_result(message.chat.id)
    
@bot.message_handler(commands=["name_filter"],func=lambda message: State.get_current_state(message.chat.id) == config.States.S_RESULT.value)
def cmd_name_filter(message):
    State.set_state(message.chat.id, config.States.S_START.value)
    OUT=RN.Items(lot_name)
    OUT.get_name_filtered(message.chat.id)
    
    
@bot.message_handler(commands=["price_filter"],func=lambda message: State.get_current_state(message.chat.id) == config.States.S_RESULT.value)
def cmd_price_filtered(message):
    State.set_state(message.chat.id, config.States.S_PRICE_RANGE.value)
    bot.send_message(message.chat.id, "Пожалуйста, введите цену в формате: минимальная_цена максимальная_цена")
    

@bot.message_handler(func=lambda message: State.get_current_state(message.chat.id) == config.States.S_PRICE_RANGE.value)
def out_price_range(message):   
    State.set_state(message.chat.id, config.States.S_START.value)
    try:
        min_price=float(message.text.split(' ')[0])
        max_price=float(message.text.split(' ')[1])
    except:
        min_price=0
        max_price=10000
    OUT=RN.Items(lot_name)
    OUT.get_price_filtered(message.chat.id,min_price,max_price)
    
if __name__ == "__main__":
    bot.polling(none_stop=True)

