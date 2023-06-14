from aiogram import types, Dispatcher
from create import dp, bot
from keyboards import kb_client
from aiogram.types import ReplyKeyboardRemove
from data_base import sqlite_db


# @dp.message_handler(commands=['start','help'])
async def command_start(message: types.Message):
    try:
        await bot.send_message(message.from_user.id, 'Приятного оформления заказа!', reply_markup=kb_client)
        await message.delete()
    except:
        await message.reply('Для общение с ботом через личные сообщения, напишите ему:\nссылка на бота')
# @dp.message_handler(commands=['Режим_работы'])
async def operating_mode(message: types.Message):
    await bot.send_message(message.from_user.id, 'Вс-Чт 10:00-23:00, Пт-Сб 10:00-00:00')
# @dp.message_handler(commands=['Расположение'])
async def place(message: types.Message):
    await bot.send_message(message.from_user.id, '5-я просека, 107, 1 этаж, Самара \n Южное шоссе, 1 к2, Самара')

#@dp.message_handler(command=['Меню'])
async def pizza_menu_command(message: types.Message):
     await sqlite_db.sql_read(message)


def register_handlers_client(dp : Dispatcher):
    dp.register_message_handler(command_start, commands=['start','help'] )
    dp.register_message_handler(operating_mode, lambda message: message.text == "Режим работы🕐" )
    dp.register_message_handler(place, lambda message: message.text == "Расположение📌")
    dp.register_message_handler(pizza_menu_command, lambda message: message.text == "Меню🍕" )
