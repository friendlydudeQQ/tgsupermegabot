from aiogram import Bot
from aiogram.dispatcher import Dispatcher
from aiogram.contrib.fsm_storage.memory import MemoryStorage

storage = MemoryStorage()

bot = Bot(token="6296066436:AAH2poZ58lEJCDzkPr48uC_Dua2hvOv6ecU")
dp = Dispatcher(bot, storage = storage)