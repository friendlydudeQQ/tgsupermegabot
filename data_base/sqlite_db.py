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
    base.execute('CREATE TABLE IF NOT EXISTS menu(page INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,img TEXT, name TEXT , description TEXT, price INTEGER)')
    base.commit()

async def sql_menu(message):
    pages_count_query = cur.execute(f"SELECT COUNT(*) FROM `menu`")
    pages_count = int(pages_count_query.fetchone()[0])
    print(type(page))

    product_query = cur.execute(f"SELECT 'name', 'photo', 'description', 'price' FROM 'menu' WHERE 'page' = ?;",(page,))
    name, photo  ,description, price = product_query.fetchone()

    cur.execute(f"UPDATE `menu` SET `page` = ? WHERE `page` = ?;", (page, message.chat.id))
    connect.commit()

    buttons = types.InlineKeyboardMarkup()
    left = page - 1 if page != 1 else pages_count
    right = page + 1 if page != pages_count else 1
    try:
        try:
            photo = open(photo_path, 'rb')
        except:
            photo = photo_path
        msg = f"Название: *{name}*\nОписание: "
        msg += f"*{description}*\n" if description != None else '_нет_\n'

        bot.send_photo(message.chat.id, photo=photo, caption=msg, reply_markup=buttons)
    except:
        msg = f"Название: *{name}*\nОписание: "
        msg += f"*{description}*\n" if description != None else '_нет_\n'

        bot.send_message(message.chat.id, msg, reply_markup=buttons)

    try:
        bot.delete_message(message.chat.id, previous_message.id)
    except:
        pass




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