import sqlite3 as sq
from create import dp,bot
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from keyboards import kb_client
from aiogram import types

def sql_start():
    global base, cur
    base = sq.connect('pizza.db')
    cur = base.cursor()
    if base:
        print('Data base connected OK!')
    base.execute('CREATE TABLE IF NOT EXISTS menu(page INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,img TEXT, name TEXT , description TEXT, price INTEGER)')
    base.commit()

async def sql_menu(message, page=1):
    pages_count_query = cur.execute(f"SELECT COUNT(*) FROM `menu`")
    pages_count = int(pages_count_query.fetchone()[0])


    product_query = cur.execute(f"SELECT 'name', 'photo', 'description', 'price' FROM 'menu' WHERE 'page' = ?;",(page,))
    

    cur.execute(f"UPDATE `menu` SET `page` = ? WHERE `page` = ?;", (page, message.chat.id))
    base.commit()

    buttons = types.InlineKeyboardMarkup()
    left = page - 1 if page != 1 else pages_count
    right = page + 1 if page != pages_count else 1

    left_button = types.InlineKeyboardButton("←", callback_data=f'to {left}')
    page_button = types.InlineKeyboardButton(f"{str(page)}/{str(pages_count)}", callback_data='_')
    right_button = types.InlineKeyboardButton("→", callback_data=f'to {right}')
    buy_button = types.InlineKeyboardButton("КУПИТЬ", callback_data='buy')
    buttons.add(left_button, page_button, right_button)
    buttons.add(buy_button)

    mt =  f'- Название:{name}\n  \n- Описание: {description}\n  \n - Цена: {price} рублей'

    await  bot.send_photo(message.from_user.id, photo ,mt , reply_markup=buttons)





async def sql_add_command(state):
    async with state.proxy() as data:
        print(data)
        cur.execute("INSERT INTO menu(img, name, description, price) VALUES (? , ? , ? , ? )", tuple(data.values()))
        base.commit()


async def sql_read(message):
    for ret in cur.execute('SELECT * FROM menu WHERE id = 2').fetchall():
        await bot.send_photo(message.from_user.id, ret[1], f'- Название:{ret[2]}\n  \n- Описание: {ret[3]}\n  \n - Цена: {ret[-1]} рублей')

async def sql_read2():
    return cur.execute('SELECT * FROM menu').fetchall()

async def sql_delete_command(data):
    cur.execute('DELETE FROM menu WHERE name = ?', (data,))
    base.commit()