# -*- coding: utf8 -*-
################################################################################################################################
from aiogram import Bot, types
from aiogram.utils import executor
from aiogram.dispatcher import Dispatcher
from aiogram.types import ReplyKeyboardRemove, ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardMarkup, InlineKeyboardButton
import asyncio
#################################################################################################################################
 
######################################################################
from aiogram.dispatcher import FSMContext ## ТО, ЧЕГО ВЫ ЖДАЛИ - FSM
from aiogram.dispatcher.filters import Command ## ТО, ЧЕГО ВЫ ЖДАЛИ - FSM
from aiogram.contrib.fsm_storage.memory import MemoryStorage ## ТО, ЧЕГО ВЫ ЖДАЛИ - FSM
from aiogram.dispatcher.filters.state import StatesGroup, State ## ТО, ЧЕГО ВЫ ЖДАЛИ - FSM
######################################################################
 
######################
import config ## ИМПОРТИРУЕМ ДАННЫЕ ИЗ ФАЙЛОВ config.py
import keyboard ## ИМПОРТИРУЕМ ДАННЫЕ ИЗ ФАЙЛОВ keyboard.py
######################
 
import logging # ПРОСТО ВЫВОДИТ В КОНСОЛЬ ИНФОРМАЦИЮ, КОГДА БОТ ЗАПУСТИТСЯ
import random
import asyncio
import datetime
import json
from aiogram import Bot, Dispatcher, executor, types
from aiogram.utils.markdown import hbold, hunderline, hcode, hlink
from aiogram.dispatcher.filters import Text
from aiogram.utils.deep_linking import get_start_link, decode_payload
from aiogram import types
from bs4 import BeautifulSoup
import requests

storage = MemoryStorage() # FOR FSM
bot = Bot(token=config.botkey, parse_mode=types.ParseMode.HTML)
dp = Dispatcher(bot, storage=storage)

logging.basicConfig(format=u'%(filename)s [LINE:%(lineno)d] #%(levelname)-8s [%(asctime)s]  %(message)s',
                    level=logging.INFO,
                    )


@dp.message_handler(Command("start"), state=None)

async def welcome(message):
    joinedFile = open("user.txt","r")
    joinedUsers = set ()
    for line in joinedFile:
        joinedUsers.add(line.strip())

    if not str(message.chat.id) in joinedUsers:
        joinedFile = open("user.txt","a")
        joinedFile.write(str(message.chat.id)+ "\n")
        joinedUsers.add(message.chat.id)

    await bot.send_message(message.chat.id, f"<b>Привет, {message.from_user.first_name}, Я бот, который позволит быстро находить нужные товары в <a href='https://www.golden-swim.by/'>GoldenSwim</a>\n\nВводи название, а я отправлю тебе нужные товары.</b>", reply_markup=keyboard.start, parse_mode='html', disable_web_page_preview=1)




##################################################################################################ПАРСЕР##############################################################################

@dp.message_handler(content_types=['text'])
async def get_message(message: types.Message):
    url = "https://www.golden-swim.by/search?q=" + message.text
    request = requests.get(url)
    soup = BeautifulSoup(request.text, "html.parser")

    all_links = soup.find_all("a")
    for link in all_links:
        print(link["href"])
        url = "https://www.golden-swim.by/" + link["href"] 
        request = requests.get(url)
        soup = BeautifulSoup(request.text, "html.parser")

        name = soup.find("h1", class_="product__title heading").text
        price = soup.find("span", class_="product__price-cur").text
        img = soup.find("img", class_="lazyload entered loaded")

        await bot.send_photo(message.chat.id, img,
        caption="<b>" + name + "</b>\n<i>" + price + f"</i>\n<a href='{url}'>Ссылка на сайт</a>",
        parse_mode="html")



if __name__ == '__main__':
    print('Монстр пчелы запущен!')                                   
executor.start_polling(dp)
