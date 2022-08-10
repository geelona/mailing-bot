from aiogram import Bot, Dispatcher, executor, types
import sqlite3

main_admin = open('main_admin.txt', 'r').read()
token = open('token.txt', 'r').read()

bot = Bot(token=token)
dp = Dispatcher(bot)

can_buttons = True


def get_admins():
    conn = sqlite3.connect('admins.db')
    cursor = conn.cursor()
    cursor.execute('CREATE TABLE IF NOT EXISTS admins (username)')
    cursor.execute("SELECT username FROM admins")
    admins = cursor.fetchall()
    conn.close()
    return admins


def get_groups():
    conn = sqlite3.connect('groups.db')
    cursor = conn.cursor()
    cursor.execute('CREATE TABLE IF NOT EXISTS groups (id, name)')
    cursor.execute("SELECT id, name FROM groups")
    groups = cursor.fetchall()
    conn.close()
    return groups


@dp.message_handler(content_types=['text'])
async def send_message(message: types.Message):
    global can_buttons

    groups = get_groups()

    if (message.from_user.username in get_admins() or message.from_user.username == main_admin):
        if message.text == '/add':

            if message.chat.title != None and message.chat.id not in [i[0] for i in groups]:

                conn = sqlite3.connect('groups.db')
                c = conn.cursor()
                c.execute('CREATE TABLE IF NOT EXISTS groups (id, name)')
                c.execute('INSERT INTO groups VALUES (?, ?)', (message.chat.id, message.chat.title))
                conn.commit()
                conn.close()

                await message.answer('Group added to database')

        elif message.text == '/del':

            groups = get_groups()
                
            if message.chat.title != None and message.chat.id in [i[0] for i in groups]:

                conn = sqlite3.connect('groups.db')
                c = conn.cursor()
                c.execute('DELETE FROM groups WHERE id = ?', (message.chat.id,))
                conn.commit()
                conn.close()
    
                await message.answer('Group deleted from database')

        elif message.text == '/list':

            conn = sqlite3.connect('groups.db')
            c = conn.cursor()
            c.execute('SELECT * FROM groups')
            groups = c.fetchall()
            conn.close()
            groups_list = []
            for group in groups:
                groups_list.append(group[1])
            await message.answer('Groups in database: ' + ', '.join(groups_list))

        elif '/add_admin' in message.text:

                if message.from_user.username == main_admin:
    
                    username = message.text.split()[1]
                    conn = sqlite3.connect('admins.db')
                    c = conn.cursor()
                    c.execute('CREATE TABLE IF NOT EXISTS admins (username)')
                    c.execute('INSERT INTO admins VALUES (?)', (username,))
                    conn.commit()
                    conn.close()
                    await message.answer('Admin added to database')
        
        elif '/del_admin' in message.text:

                    if message.from_user.username == main_admin:
        
                        username = message.text.split()[1]
                        conn = sqlite3.connect('admins.db')
                        c = conn.cursor()
                        c.execute('DELETE FROM admins WHERE username = ?', (username,))
                        conn.commit()
                        conn.close()
                        await message.answer('Admin deleted from database')

        elif message.text == '/list_admins':

            conn = sqlite3.connect('admins.db')
            c = conn.cursor()
            c.execute('SELECT * FROM admins')
            admins = c.fetchall()
            conn.close()
            admins_list = []
            for admin in admins:
                admins_list.append(admin[0])
            await message.answer('Admins in database: ' + '\nmain admin: ' + main_admin + '\nanother admins: ' + ', '.join(admins_list))

        elif message.text == '/commands':
                
                await message.answer('Commands:\n/add - add group to database\n/del - delete group from database\n/list - list groups in database\n/add_admin username (without @) - add admin to database\n/del_admin username (without @) - delete admin from database\n/list_admins - list admins in database\n/commands - list commands')

        if message.text == '/send' and can_buttons:
            await message.answer('send me a personal message that you want to send to groups')
            can_buttons = False

        if not can_buttons and message.text != '/send':
            groups = get_groups()
            for group in groups:
                try:
                    await bot.send_message(group[0], message.text)
                except:
                    pass
            can_buttons = True

@dp.message_handler(content_types=['photo'])
async def send_photo(message: types.Message):
    global can_buttons

    if (message.from_user.username in get_admins() or message.from_user.username == main_admin) and can_buttons is False:

        if message.caption == None:
            groups = get_groups()
            for group in groups:
                try:
                    await bot.send_photo(group[0], message.photo[-1].file_id)
                except:
                    pass
            can_buttons = True
        
        else:
            groups = get_groups()
            for group in groups:
                try:
                    await bot.send_photo(group[0], message.photo[-1].file_id, caption=message.caption)
                except:
                    pass
            can_buttons = True

@dp.message_handler(content_types=['document'])
async def send_document(message: types.Message):
    global can_buttons

    if (message.from_user.username in get_admins() or message.from_user.username == main_admin) and can_buttons is False:

        groups = get_groups()
        for group in groups:
            try:
                await bot.send_document(group[0], message.document.file_id)
            except:
                pass
        can_buttons = True
        
@dp.message_handler(content_types=['video'])
async def send_video(message: types.Message):
    global can_buttons

    if (message.from_user.username in get_admins() or message.from_user.username == main_admin) and can_buttons is False:

        groups = get_groups()
        for group in groups:
            try:
                await bot.send_video(group[0], message.video.file_id)
            except:
                pass
        can_buttons = True

@dp.message_handler(content_types=['audio'])
async def send_audio(message: types.Message):
    global can_buttons

    if (message.from_user.username in get_admins() or message.from_user.username == main_admin) and can_buttons is False:

        groups = get_groups()
        for group in groups:
            try:
                await bot.send_audio(group[0], message.audio.file_id)
            except:
                pass
        can_buttons = True

@dp.message_handler(content_types=['voice'])
async def send_voice(message: types.Message):
    global can_buttons

    if (message.from_user.username in get_admins() or message.from_user.username == main_admin) and can_buttons is False:

        groups = get_groups()
        for group in groups:
            try:
                await bot.send_voice(group[0], message.voice.file_id)
            except:
                pass
        can_buttons = True

@dp.message_handler(content_types=['sticker'])
async def send_sticker(message: types.Message):
    global can_buttons

    if (message.from_user.username in get_admins() or message.from_user.username == main_admin) and can_buttons is False:

        groups = get_groups()
        for group in groups:
            try:
                await bot.send_sticker(group[0], message.sticker.file_id)
            except:
                pass
        can_buttons = True

@dp.message_handler(content_types=['location'])
async def send_location(message: types.Message):
    global can_buttons

    if (message.from_user.username in get_admins() or message.from_user.username == main_admin) and can_buttons is False:

        groups = get_groups()
        for group in groups:
            try:
                await bot.send_location(group[0], message.location.latitude, message.location.longitude)
            except:
                pass
        can_buttons = True

@dp.message_handler(content_types=['contact'])
async def send_contact(message: types.Message):
    global can_buttons

    if (message.from_user.username in get_admins() or message.from_user.username == main_admin) and can_buttons is False:

        groups = get_groups()
        for group in groups:
            try:
                await bot.send_contact(group[0], message.contact.phone_number, message.contact.first_name)
            except:
                pass
        can_buttons = True

@dp.message_handler(content_types=['poll'])
async def send_poll(message: types.Message):
    global can_buttons

    if (message.from_user.username in get_admins() or message.from_user.username == main_admin) and can_buttons is False:

        groups = get_groups()
        for group in groups:
            try:
                await bot.send_poll(group[0], message.poll.question, message.poll.options)
            except:
                pass
        can_buttons = True

@dp.message_handler(content_types=['dice'])
async def send_dice(message: types.Message):
    global can_buttons

    if (message.from_user.username in get_admins() or message.from_user.username == main_admin) and can_buttons is False:

        groups = get_groups()
        for group in groups:
            try:
                await bot.send_dice(group[0], message.dice.emoji)
            except:
                pass
        can_buttons = True

@dp.message_handler(content_types=['venue'])
async def send_venue(message: types.Message):
    global can_buttons

    if (message.from_user.username in get_admins() or message.from_user.username == main_admin) and can_buttons is False:

        groups = get_groups()
        for group in groups:
            try:
                await bot.send_venue(group[0], message.venue.latitude, message.venue.longitude, message.venue.title, message.venue.address)
            except:
                pass
        can_buttons = True

@dp.message_handler(content_types=['video_note'])
async def send_video_note(message: types.Message):
    global can_buttons

    if (message.from_user.username in get_admins() or message.from_user.username == main_admin) and can_buttons is False:

        groups = get_groups()
        for group in groups:
            try:
                await bot.send_video_note(group[0], message.video_note.file_id)
            except:
                pass
        can_buttons = True

@dp.message_handler(content_types=['animation'])
async def send_animation(message: types.Message):
    global can_buttons

    if (message.from_user.username in get_admins() or message.from_user.username == main_admin) and can_buttons is False:

        groups = get_groups()
        for group in groups:
            try:
                await bot.send_animation(group[0], message.animation.file_id)
            except:
                pass
        can_buttons = True

@dp.message_handler(content_types=['invoice'])
async def send_invoice(message: types.Message):
    global can_buttons

    if (message.from_user.username in get_admins() or message.from_user.username == main_admin) and can_buttons is False:

        groups = get_groups()
        for group in groups:
            try:
                await bot.send_invoice(group[0], message.invoice.title, message.invoice.description, message.invoice.payload, message.invoice.provider_token, message.invoice.start_parameter, message.invoice.currency, message.invoice.prices)
            except:
                pass
        can_buttons = True

@dp.message_handler(content_types=['successful_payment'])
async def send_successful_payment(message: types.Message):
    global can_buttons

    if (message.from_user.username in get_admins() or message.from_user.username == main_admin) and can_buttons is False:

        groups = get_groups()
        for group in groups:
            try:
                await bot.send_successful_payment(group[0], message.successful_payment.invoice_payload, message.successful_payment.provider_payment_charge_id)
            except:
                pass
        can_buttons = True

@dp.message_handler(content_types=['passport_data'])
async def send_passport_data(message: types.Message):
    global can_buttons

    if (message.from_user.username in get_admins() or message.from_user.username == main_admin) and can_buttons is False:

        groups = get_groups()
        for group in groups:
            try:
                await bot.send_passport_data(group[0], message.passport_data.data)
            except:
                pass
        can_buttons = True

@dp.message_handler(content_types=['game'])
async def send_game(message: types.Message):
    global can_buttons

    if (message.from_user.username in get_admins() or message.from_user.username == main_admin) and can_buttons is False:

        groups = get_groups()
        for group in groups:
            try:
                await bot.send_game(group[0], message.game.game_short_name)
            except:
                pass
        can_buttons = True


executor.start_polling(dp, skip_updates=True)