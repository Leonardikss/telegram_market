import telebot
import pickle


def save():
    with open('dict.pkl', 'wb') as f:
        pickle.dump(users, f)


def product_name_create(message):
    return f"{users[message.from_user.id]["group"]} {users[message.from_user.id]["album"]} {users[message.from_user.id]["artist"]}"


bot = telebot.TeleBot([token])


try:
    with open('dict.pkl', 'rb') as f:
        users = pickle.load(f)
except:
    users = {"data": {"password": "admin618admin"}, "products": dict()}
    save()


@bot.message_handler(commands=['start'])
def start_message(message):
    if message.from_user.id not in users:
        users[message.from_user.id] = {"isadmin": False, "admin": False, "panier": list()}
    else:
        users[message.from_user.id]["admin"] = False

    keyboard = telebot.types.InlineKeyboardMarkup()
    for i in users["data"]:
        if i != "password":
            keyboard.add(telebot.types.InlineKeyboardButton(text=i, callback_data=f"g{i}"))
    keyboard.add(telebot.types.InlineKeyboardButton(text="корзина", callback_data=f" panier"))

    bot.send_message(message.from_user.id, "Привет, выбери к-поп группу", reply_markup=keyboard)
    save()


@bot.callback_query_handler(func=lambda call: call.data == " panier")
def panier(call):
    for i in range(len(users[call.from_user.id]["panier"])):
        keyboard = telebot.types.InlineKeyboardMarkup()
        if i + 1 == len(users[call.from_user.id]["panier"]):
            keyboard.add(telebot.types.InlineKeyboardButton(text="очистить корзину", callback_data=f" panier_с"))
        bot.send_message(call.from_user.id, users[call.from_user.id]["panier"][i], reply_markup=keyboard)


@bot.callback_query_handler(func=lambda call: call.data == " panier_с")
def panier(call):
    users[call.from_user.id]["panier"] = list()
    bot.send_message(call.from_user.id, "корзина очищена")

    save()
    start_message(call)

###################################################################################


@bot.message_handler(commands=['admin'])
def admin(message):
    users[message.from_user.id]["isadmin"] = True
    bot.send_message(message.from_user.id, "введите пароль")
    save()


@bot.message_handler(func=lambda message: users[message.from_user.id]["isadmin"])
def login_admin(message):
    if message.text == users["data"]["password"] or users[message.from_user.id]["admin"]:
        users[message.from_user.id]["admin"] = True
        users[message.from_user.id]["isadmin"] = False
        users[message.from_user.id]["password"] = False
        users[message.from_user.id]["addgroup"] = False
        users[message.from_user.id]["delgroup"] = False
        users[message.from_user.id]["addproduct"] = False
        users[message.from_user.id]["delproduct"] = False

        keyboard = telebot.types.InlineKeyboardMarkup()
        keyboard.add(telebot.types.InlineKeyboardButton(text="изменить пароль", callback_data=" password"))
        keyboard.add(telebot.types.InlineKeyboardButton(text="добавить группу", callback_data=" addgroup"))
        keyboard.add(telebot.types.InlineKeyboardButton(text="удалить группу", callback_data=" delgroup"))
        keyboard.add(telebot.types.InlineKeyboardButton(text="добавить товар", callback_data=" addproduct"))
        keyboard.add(telebot.types.InlineKeyboardButton(text="удалить товар", callback_data=" delproduct"))

        bot.send_message(message.from_user.id, "панель управления:", reply_markup=keyboard)
    else:
        bot.send_message(message.from_user.id, "пароль не верен")

    save()


################################


@bot.callback_query_handler(func=lambda call: call.data == " password")
def get_password(call):
    users[call.from_user.id]["password"] = True
    bot.send_message(call.from_user.id, "напишите новый пароль")
    save()


@bot.message_handler(func=lambda message: users[message.from_user.id]["admin"] and
                     users[message.from_user.id]["password"])
def set_password(message):
    users["data"]["password"] = message.text
    users[message.from_user.id]["password"] = False
    bot.send_message(message.from_user.id, "пароль успешно изменен")
    save()
    login_admin(message)


################################


@bot.callback_query_handler(func=lambda call: call.data == " addgroup")
def get_addgroup(call):
    users[call.from_user.id]["addgroup"] = True
    bot.send_message(call.from_user.id, '''напишите название новой группы.
после на следующей строке напишите название всех альбомов через запятую.
после на следующей троке напишите название всех исполнителей через запятую.
ВСЕ ПИШИТЕ В ОДНОМ СООБЩЕНИИ''')
    save()


@bot.message_handler(func=lambda message: users[message.from_user.id]["admin"] and
                     users[message.from_user.id]["addgroup"])
def set_addgroup(message):
    group_data = message.text.split("\n")

    if len(group_data) == 3 and len(group_data[0]) < 16:
        users[message.from_user.id]["addgroup"] = False
        users["data"][group_data[0]] = dict()
        users["data"][group_data[0]]["albums"] = group_data[1].split(",")
        users["data"][group_data[0]]["artists"] = group_data[2].split(",")

        bot.send_message(message.from_user.id, "группа успешно добавлена")
        save()
        login_admin(message)
    elif len(group_data) != 3:
        bot.send_message(message.from_user.id, "неверный формат ввода, повторите попытку")
    else:
        bot.send_message(message.from_user.id, "название группы не может быть больше 15 символа, повторите попытку")


################################


@bot.callback_query_handler(func=lambda call: call.data == " delgroup")
def get_delgroup(call):
    users[call.from_user.id]["delgroup"] = True
    bot.send_message(call.from_user.id, '''напишите название группы которую хотите удалить''')
    save()


@bot.message_handler(func=lambda message: users[message.from_user.id]["admin"] and
                                          users[message.from_user.id]["delgroup"])
def set_delgroup(message):
    if message.text in users["data"] and message.text != "password":
        users[message.from_user.id]["delgroup"] = False
        del users["data"][message.text]
        bot.send_message(message.from_user.id, "группа успешно удалена")
        save()
        login_admin(message)
    else:
        bot.send_message(message.from_user.id, "такой группы не найдено")



###################################


@bot.callback_query_handler(func=lambda call: call.data == " addproduct")
def get_addproduct(call):
    users[call.from_user.id]["addproduct"] = True
    
    keyboard = telebot.types.InlineKeyboardMarkup()
    for i in users["data"]:
        if i != "password":
            keyboard.add(telebot.types.InlineKeyboardButton(text=i, callback_data=f"g{i}"))

    bot.send_message(call.from_user.id, "перейдите в раздел в который вы хотите добавить продукт", reply_markup=keyboard)

    save()


@bot.message_handler(func=lambda message: users[message.from_user.id]["admin"] and
                                          users[message.from_user.id]["addproduct"])
def set_addproduct(message):
    product_data = message.text.split("\n")
    
    if "artist" in users[message.from_user.id]:
        if product_name_create(message) not in users["products"]:
            users["products"][product_name_create(message)] = dict()
        users["products"][product_name_create(message)][product_data[0]] = dict()
        users["products"][product_name_create(message)][product_data[0]]["info"] = product_data[1]
        users["products"][product_name_create(message)][product_data[0]]["price"] = product_data[2]
        bot.send_message(message.from_user.id, "отправте фотографию товара или видео с товаром")
        users[message.from_user.id]["product_name"] = product_data[0]

    save()


@bot.message_handler(content_types=['photo'], func=lambda message: users[message.from_user.id]["admin"] and
                                                                   users[message.from_user.id]["addproduct"])
def set_addproduct_photo(message):
    photo = message.photo[-1]
    file_info = bot.get_file(photo.file_id)
    downloaded_file = bot.download_file(file_info.file_path)
    save_path = f'photos/{users[message.from_user.id]["product_name"]}.jpg'
    with open(save_path, 'wb') as new_file:
        new_file.write(downloaded_file)
    users["products"][product_name_create(message)][users[message.from_user.id]["product_name"]]["photo_path"] = save_path

    keyboard = telebot.types.InlineKeyboardMarkup()
    keyboard.add(telebot.types.InlineKeyboardButton(text="без видео", callback_data=" pass"))
    bot.send_message(message.from_user.id, "отправте видео с товаром", reply_markup=keyboard)

    save()


@bot.callback_query_handler(func=lambda call: call.data == " pass" and users[call.from_user.id]["admin"] and
                                                                       users[call.from_user.id]["addproduct"])
def set_addproduct_video_pass(call):
    users["products"][product_name_create(call)][users[call.from_user.id]["product_name"]]["video_path"] = None

    del users[call.from_user.id]["product_name"]
    bot.send_message(call.from_user.id, "товар успешно добавлен")
    users[call.from_user.id]["addproduct"] = False

    save()
    call.text = None
    login_admin(call)


@bot.message_handler(content_types=['video'], func=lambda message: users[message.from_user.id]["admin"] and
                                                                   users[message.from_user.id]["addproduct"])
def set_addproduct_video(message):
    video = message.video
    file_info = bot.get_file(video.file_id)
    downloaded_file = bot.download_file(file_info.file_path)
    save_path = file_info.file_path
    with open(save_path, 'wb') as new_file:
        new_file.write(downloaded_file)
    users["products"][product_name_create(message)][users[message.from_user.id]["product_name"]]["video_path"] = save_path


    del users[message.from_user.id]["product_name"]
    bot.send_message(message.from_user.id, "товар успешно добавлен")
    users[message.from_user.id]["addproduct"] = False

    save()
    login_admin(message)


##################################


@bot.callback_query_handler(func=lambda call: call.data == " delproduct")
def get_delproduct(call):
    users[call.from_user.id]["delproduct"] = True

    keyboard = telebot.types.InlineKeyboardMarkup()
    for i in users["data"]:
        if i != "password":
            keyboard.add(telebot.types.InlineKeyboardButton(text=i, callback_data=f"g{i}"))

    bot.send_message(call.from_user.id, "перейдите в раздел в котором вы хотите удалить продукт",
                     reply_markup=keyboard)

    save()


@bot.callback_query_handler(func=lambda call: call.data[:2] == "dd" and users[call.from_user.id]["admin"] and
                                              users[call.from_user.id]["delproduct"])
def set_delproduct(call):
    users[call.from_user.id]["delproduct"] = False

    del users["products"][product_name_create(call)][list(users["products"][product_name_create(call)])[int(call.data[2:])]]
    if not users["products"][product_name_create(call)]:
        del users["products"][product_name_create(call)]
    bot.send_message(call.from_user.id, "товар успешно удален")

    save()
    call.text = None
    login_admin(call)


###########################################################################################


@bot.callback_query_handler(func=lambda call: call.data[0] == "g")
def set_group(call):
    users[call.from_user.id]["group"] = call.data[1:]

    keyboard = telebot.types.InlineKeyboardMarkup()
    for i in range(len(users["data"][call.data[1:]]["albums"])):
        key = telebot.types.InlineKeyboardButton(text=users["data"][call.data[1:]]["albums"][i], callback_data=f"b{i}")
        keyboard.add(key)

    bot.send_message(call.from_user.id, "теперь выбери альбом", reply_markup=keyboard)
    save()


@bot.callback_query_handler(func=lambda call: call.data[0] == "b")
def set_album(call):
    users[call.from_user.id]["album"] = users["data"][users[call.from_user.id]["group"]]["albums"][int(call.data[1:])]

    keyboard = telebot.types.InlineKeyboardMarkup()
    for i in range(len(users["data"][users[call.from_user.id]["group"]]["artists"])):
        key = telebot.types.InlineKeyboardButton(text=users["data"][users[call.from_user.id]["group"]]["artists"][i], callback_data=f"r{i}")
        keyboard.add(key)

    bot.send_message(call.from_user.id, "теперь выбери исполнителя", reply_markup=keyboard)
    save()


@bot.callback_query_handler(func=lambda call: call.data[0] == "r")
def set_artist(call):
    users[call.from_user.id]["artist"] = users["data"][users[call.from_user.id]["group"]]["artists"][int(call.data[1:])]

    if users[call.from_user.id]["admin"] and users[call.from_user.id]["addproduct"]:
        bot.send_message(call.from_user.id, ''' теперь напишите название нового товара.
после, на следующей строке напишите описание товара.
после, на следующей троке напишите цену без указания валюты.
ВСЕ ПИШИТЕ В ОДНОМ СООБЩЕНИИ''')
    elif users[call.from_user.id]["admin"]:
        try:
            for i in range(len(list(users["products"][product_name_create(call)]))):
                product_name = list(users["products"][product_name_create(call)])[i]

                if users["products"][product_name_create(call)][product_name]["video_path"]:
                    video = open(users["products"][product_name_create(call)][product_name]["video_path"], 'rb')
                    bot.send_video(call.from_user.id, video)

                photo = open(users["products"][product_name_create(call)][product_name]["photo_path"], 'rb')
                bot.send_photo(call.from_user.id, photo)

                keyboard = telebot.types.InlineKeyboardMarkup()
                keyboard.add(telebot.types.InlineKeyboardButton(text="удалить", callback_data=f"dd{i}"))

                text = f'''{product_name}
        {users["products"][product_name_create(call)][product_name]["info"]}
        {users["products"][product_name_create(call)][product_name]["price"]} руб.'''
                bot.send_message(call.from_user.id, text, reply_markup=keyboard)
        except:
            bot.send_message(call.from_user.id, "таких товаров нет")
    else:
        try:
            for i in range(len(list(users["products"][product_name_create(call)]))):
                product_name = list(users["products"][product_name_create(call)])[i]

                if users["products"][product_name_create(call)][product_name]["video_path"]:
                    video = open(users["products"][product_name_create(call)][product_name]["video_path"], 'rb')
                    bot.send_video(call.from_user.id, video)

                photo = open(users["products"][product_name_create(call)][product_name]["photo_path"], 'rb')
                bot.send_photo(call.from_user.id, photo)

                keyboard = telebot.types.InlineKeyboardMarkup()
                keyboard.add(telebot.types.InlineKeyboardButton(text="добавить в корзину", callback_data=f"pp{i}"))

                text = f'''{product_name}
{users["products"][product_name_create(call)][product_name]["info"]}
{users["products"][product_name_create(call)][product_name]["price"]} руб.'''
                bot.send_message(call.from_user.id, text, reply_markup=keyboard)
        except:
            bot.send_message(call.from_user.id, "таких товаров нет")

    save()


@bot.callback_query_handler(func=lambda call: call.data[:2] == "pp")
def add_panier(call):
    users[call.from_user.id]["panier"].append((product_name_create(call),
                                               list(users["products"][product_name_create(call)])[int(call.data[2:])]))

    save()
    start_message(call)


bot.infinity_polling()
