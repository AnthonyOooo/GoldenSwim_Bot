from aiogram import Bot, types
from aiogram.types import ReplyKeyboardRemove, ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardMarkup, InlineKeyboardButton

######################################################
start = types.ReplyKeyboardMarkup(resize_keyboard=True) # СОЗДАЕМ ВООБЩЕ ОСНОВУ ДЛЯ КНОПОК

info = types.KeyboardButton("Шапочки")            # ДОБАВЛЯЕМ КНОПКУ ИНФОРМАЦИИ
stats = types.KeyboardButton("Очки")            # ДОБАВЛЯЕМ КНОПКУ СТАТИСТИКИ

start.add(stats, info) #ДОБАВЛЯЕМ ИХ В БОТА