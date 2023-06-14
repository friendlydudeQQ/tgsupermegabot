from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, ReplyKeyboardRemove

b1 = KeyboardButton('Режим работы🕐')
b2 = KeyboardButton('Расположение📌')
b3 = KeyboardButton('Меню🍕')

kb_client = ReplyKeyboardMarkup(resize_keyboard=True)

kb_client.add(b1).add(b2).add(b3)

