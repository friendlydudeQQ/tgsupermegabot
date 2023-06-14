import sqlite3 as sq
from create import dp,bot
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from keyboards import kb_client

def sql_start():
    global base, cur
    base = sq.connect('pizza.db')
    cur = base.cursor()
    if base:
        print('Data base connected OK!')
    base.execute('CREATE TABLE IF NOT EXISTS menu(id INTEGER PRIMARY KEY,img TEXT, name TEXT , description TEXT, price TEXT)')
    base.commit()


async def sql_add_command(state):
    async with state.proxy() as data:
        cur.execute("INSERT INTO menu VALUES (? ,?, ?, ?, ?)", tuple(data.values()))
        base.commit()

async def sql_read(message):
    for ret in cur.execute('SELECT * FROM menu').fetchall():
        await bot.send_photo(message.from_user.id, ret[1], f'- Название:{ret[2]}\n  \n- Описание: {ret[3]}\n  \n - Цена: {ret[-1]} рублей')

async def sql_read2():
    return cur.execute('SELECT * FROM menu').fetchall()

async def sql_delete_command(data):
    cur.execute('DELETE FROM menu WHERE name = ?', (data,))
    base.commit()