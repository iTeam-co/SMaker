# -*- coding: utf-8 -*-
import telebot
import random
from telebot import types
from telebot import util
from random import randint
import redis
import json
import logging
import urllib
import urllib2
import time
import logging
import subprocess
import math
import requests
import re
import os
import sys
reload(sys)
sys.setdefaultencoding("utf-8")
sudo = 122774063 #SUDO-ID
token = "BOT-TOKEN" #TOKEN
bot = telebot.TeleBot(token)
R = redis.StrictRedis(host='localhost', port=6379, db=0)
@bot.message_handler(commands=['start'])
def start(m):
    try:
        text = "سلام :)\nمن یه رباتم که میتونم تو ساخت استیکرات کمکت کنم\nچجوری؟\nاگه برا من یه متن بفرستی ، برای یه فایل مخصوص @stickers میدم که براش فوروارد کنی و پک بسازی\nبرای دریافت راهنما /help رو ارسال کن"
        bot.send_message(m.chat.id,text)
        if not R.get("type:{}".format(m.chat.id)) :
            R.set("type:{}".format(m.chat.id),"circlepro")
    except Exception as e:
        bot.send_message(sudo,e)
@bot.message_handler(commands=['users'])
def usrs(m):
    try :
        if m.chat.id == sudo :
            usrs = R.scard("our:users")
            bot.send_message(sudo,"*Bot Users :* {}".format(usrs),parse_mode="Markdown")
    except Exception as e:
        bot.send_message(sudo,e)
@bot.message_handler(commands=['sendall'])
def sendall(m):
    if m.chat.id == sudo :
        text = m.text.replace('/sendall ','')
        ids = R.smembers("our:users")
        for id in ids:
            try:
                bot.send_message(id,text)
            except:
                R.srem("our:users",id)
@bot.message_handler(commands=['fwdtoall'])
def fwdall(m):
    if m.chat.id == sudo :
        if m.reply_to_message:
            mid = m.reply_to_message.message_id
            ids = R.smembers("our:users")
            for id in ids:
                try:
                    bot.forward_message(id,m.chat.id,mid)
                except:
                    R.srem("our:users",id)
@bot.message_handler(commands=['help'])
def help(m):
    try :
        markup = types.InlineKeyboardMarkup()
        markup.add(types.InlineKeyboardButton('دایره',callback_data="circ"),types.InlineKeyboardButton('بیضی',callback_data="ovl"),types.InlineKeyboardButton('مربع',callback_data="sqr"))
        text = "سلام !\nاین ربات برای شما فایل هایی مخصوص ربات @stickers میسازه تا بتونید با فوروارد اونا به ربات پکیج استیکر بسازید\nکافیه متنتون رو ارسال کنید\nبرای انتخاب نوع قالب استیکراتون هم روی یکی از ۳ تا دکمه زیر کلیک کنید"
        bot.send_message(m.chat.id,text,reply_markup=markup)
    except Exception as e:
        bot.send_message(logchat,e)
@bot.callback_query_handler(func=lambda call: True)
def callback_inline(call):
    try :
        if call.data == "circ":
            R.set("type:{}".format(call.message.chat.id),"circlepro")
            bot.answer_callback_query(callback_query_id=call.id, show_alert=True, text="قالب فایل های شما به دایره تغییر یافت")
        elif call.data == "sqr":
            R.set("type:{}".format(call.message.chat.id),"squer")
            bot.answer_callback_query(callback_query_id=call.id, show_alert=True, text="قالب فایل های شما به مربع تغییر یافت")
        elif call.data == "ovl":
            R.set("type:{}".format(call.message.chat.id),"oval")
            bot.answer_callback_query(callback_query_id=call.id, show_alert=True, text="قالب فایل های شما به بیضی تغییر یافت")
    except Exception as e:
        bot.send_message(logchat,e)
@bot.message_handler(func=lambda message: True)
def all(m):
    try:
        if m.text == "/start" :
            R.sadd("our:users",m.chat.id)
        elif m.text == "/help" :
            return None
        elif m.text == "/users" :
            return None
        elif m.text == "/fwdall" :
            return None
        elif re.match(r"/sendall (.*)", m.text):
            return None
        else:
            typ = R.get("type:{}".format(m.chat.id))
            text = urllib.urlencode({'txtclr': 'ffffff', 'txt': m.text, 'txtfit': 'max', 'txtsize' : '200', 'txtalign' : 'center,middle', 'txtfont' : 'PT Serif,Bold'})
            text2 = text.replace("+","%20")
            link = "http://iteam.imgix.net/{}.png?{}".format(typ,text2)
            urllib.urlretrieve(link, "SMaker.png")
            file = open('SMaker.png', 'rb')
            bot.send_document(m.chat.id,file)
    except Exception as e:
        bot.send_message(sudo,e)
bot.polling(True)
#end
