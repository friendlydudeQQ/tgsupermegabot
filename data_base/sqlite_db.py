import sqlite3 as sq
from create import dp,bot
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from keyboards import kb_client
from aiogram import types
from handlers import client
count = 0
user_id = None
dict1 = None



def sql_start():
    global base, cur
    base = sq.connect('pizza.db')
    cur = base.cursor()
    if base:
        print('Data base connected OK!')
    base.execute('CREATE TABLE IF NOT EXISTS menu(page INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,img TEXT, name TEXT , description TEXT, price INTEGER)')
    base.commit()




async def sql_menu(message, page = 1):
    global user_id
    user_id = message.from_user.id
    sqlite_connection = sq.connect('pizza.db')
    cur = sqlite_connection.cursor()
    pages_count_query = cur.execute(f"SELECT COUNT(*) FROM `menu`")
    pages_count = int(pages_count_query.fetchone()[0])

    sql_select_query = """SELECT * FROM menu WHERE page = ?"""
    a = cur.execute(sql_select_query, (page,))
    for row in a:
        goodpage = row[0]
        name = row[2]
        description = row[3]
        price = row[4]
        photo = row[1]
    global dict1
    dict1 = { 'idpage' : goodpage, 'name': name, 'description': description, 'price' : price, 'photo': photo}
    goodlist = [dict1]
    sqlite_connection.commit()
    cur.execute(f"UPDATE `menu` SET `page` = ? WHERE `page` = ?;", (page, message.chat.id))
    sqlite_connection.commit()

    buttons = types.InlineKeyboardMarkup()
    left = int(page) - 1 if page != 1 else pages_count
    right = int(page) + 1 if page != pages_count else 1

    left_button = types.InlineKeyboardButton("←", callback_data=f'to {left}')
    page_button = types.InlineKeyboardButton(f"{str(page)}/{str(pages_count)}", callback_data='_')
    right_button = types.InlineKeyboardButton("→", callback_data=f'to {right}')
    buy_button = types.InlineKeyboardButton("Добавить в корзину", callback_data='cart')
    buttons.add(left_button, page_button, right_button)
    buttons.add(buy_button)

    mt =  f'- Название:{name}\n  \n- Описание: {description}\n  \n - Цена: {price} рублей'


    await bot.send_photo(message.chat.id, photo ,mt , reply_markup=buttons)

    await bot.delete_message(message.chat.id, message.message_id)

@dp.callback_query_handler(lambda c: c.data == "cart")
async def cart(c):
    global count
    count = 0
    countb = types.InlineKeyboardMarkup()
    minus_button = types.InlineKeyboardButton("-", callback_data='minus')
    count_button = types.InlineKeyboardButton(f"{count}", callback_data='qwe')
    plus_button = types.InlineKeyboardButton("+", callback_data='plus')
    add_button = types.InlineKeyboardButton("Добавить", callback_data='addgoods')
    back_button = types.InlineKeyboardButton("Назад⛔️", callback_data='back')
    countb.add(minus_button, count_button, plus_button)
    countb.add(add_button)
    countb.add(back_button)
    await bot.edit_message_reply_markup(c.message.chat.id, c.message.message_id, reply_markup=countb)

@dp.callback_query_handler(lambda c: c.data == "minus"  )
async def minusG(c):
    global count
    count = count - 1
    countb = types.InlineKeyboardMarkup()
    minus_button = types.InlineKeyboardButton("-", callback_data='minus')
    count_button = types.InlineKeyboardButton(f"{count}", callback_data='qwe')
    plus_button = types.InlineKeyboardButton("+", callback_data='plus')
    add_button = types.InlineKeyboardButton("Добавить", callback_data='addgoods')
    back_button = types.InlineKeyboardButton("Назад⛔️", callback_data='back')
    countb.add(minus_button, count_button, plus_button)
    countb.add(add_button)
    countb.add(back_button)
    await bot.edit_message_reply_markup(c.message.chat.id, c.message.message_id, reply_markup=countb)

@dp.callback_query_handler(lambda c: c.data == "plus"  )
async def plusG(c):
    global count
    count = count + 1
    countb = types.InlineKeyboardMarkup()
    minus_button = types.InlineKeyboardButton("-", callback_data='minus')
    count_button = types.InlineKeyboardButton(f"{count}", callback_data='qwe')
    plus_button = types.InlineKeyboardButton("+", callback_data='plus')
    add_button = types.InlineKeyboardButton("Добавить", callback_data='addgoods')
    back_button = types.InlineKeyboardButton("Назад⛔️", callback_data='back')
    countb.add(minus_button, count_button, plus_button)
    countb.add(add_button)
    countb.add(back_button)
    await bot.edit_message_reply_markup(c.message.chat.id, c.message.message_id, reply_markup=countb)

@dp.callback_query_handler(lambda c: c.data == "addgoods")
async def addgood(c):

    print(dict1)
    name = dict1["name"]
    price = dict1["price"]
    page = dict1["idpage"]
    print(name)
    print(user_id)
    print(price)
    base.execute('CREATE TABLE IF NOT EXISTS korzina(`user_id` VARCHAR(99999) NULL,`name` TEXT DEFAULT NULL,"price" INTEGER, "page" INTEGER )')
    cur.execute('INSERT INTO korzina(user_id, page, name, price)VALUES ( ? , ? , ? , ? )', (user_id, page, name, price))
    base.commit()

@dp.callback_query_handler(lambda x: x.data == "back")
async def backb(x):
         await sql_menu(x.message)



@dp.callback_query_handler(lambda c: True)
async def callback(c):
    if 'to' in c.data:
        page = c.data.split(' ')[1]
    await sql_menu(c.message, page=page)

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