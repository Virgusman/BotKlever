from aiogram.types import ContentType
import telebot
from telebot import types
import dbmet

token = "5497304680:AAH4QBbTWrMKLTdF81y1_nysUjBD4A71ZTU"
bot = telebot.TeleBot(token)


flag = 0   #флаг определяет какое действие будет выполнено при вводе ссобщения пользователем
text_task = ""    #формируем текст запроса от пользователя


#рисуем главное меню
def main_menu(message):
    but1=types.KeyboardButton("Бухгалтерия")
    but2=types.KeyboardButton("Служба персонала - В РАЗРАБОТКЕ")
    but3=types.KeyboardButton("Рассылки - В РАЗРАБОТКЕ")
    but4=types.KeyboardButton("Администратор - В РАЗРАБОТКЕ")
    markup=types.ReplyKeyboardMarkup(resize_keyboard=True)
    markup.add(but1).add(but2).add(but3).add(but4)
    bot.send_message(message.chat.id, "Выполнен переход в главное меню. Выберите необходимый раздел:",  reply_markup=markup)
    
#отправка фото документа
@bot.message_handler(content_types=ContentType.PHOTO)
def send_photo(message):
    global text_task
    if flag == "2-НДФЛ":
        name = dbmet.getNameById(message.from_user.id)
        id_task = dbmet.newTask(text_task, name, message.photo[-1].file_id)
        buhs = dbmet.getIdUsers("Бух")
        markup = types.InlineKeyboardMarkup(row_width=2)
        but_task = types.InlineKeyboardButton("Принять в работу", callback_data= "ДляБух_" + name + "_" + id_task)
        markup.add(but_task)
        
        for buh in buhs:   #Рассылка запроса всем Бухгалтерам Фото+текст задачи
            bot.send_message(buh, text_task + f"\nЗапросил: {name}\nФото документа:")
            bot.send_photo(buh, message.photo[-1].file_id, reply_markup=markup)

        bot.send_message(message.chat.id, "Отправлен запрос на создание справки 2-НДФЛ")
        main_menu(message)

#кнопка в чате
@bot.callback_query_handler(func=lambda call: True)
def callback(call):
    req = call.data.split('_')
    if req[0] == 'ДляБух':
        bot.send_message(dbmet.getUserIdByName(req[1]), f"Заявка № {req[2]} принята в работу.")
        dbmet.inWork(req[2])
    if req[0] == 'СделалБух':
        z = dbmet.getNameByTask(int(req[1]))
        bot.send_message(dbmet.getUserIdByName(z), "Ваша справка готова, можете забрать в кабинете №35")
        dbmet.inClose(int(req[1]))
        

#Старт бота
@bot.message_handler(commands=["start"])
def register(message):
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    reg_button = types.KeyboardButton("Вход по номеру телефона", request_contact=True)
    markup.add(reg_button)
    bot.send_message(message.chat.id, "Добро пожаловать!\nпожалуйста, пройдите проверку по номеру телефона",  reply_markup=markup)

#Проверка по номеру телефона
@bot.message_handler(content_types=["contact"])
def contact_handler(message):
    if dbmet.searchByPhone(message.contact.phone_number,): 
        bot.send_message(message.chat.id, "Вы не являетесь сотрудником компании")
    else:
        bot.send_message(message.chat.id, "Вы вошли как " + dbmet.getNameByPhone(message.contact.phone_number))
        main_menu(message)
        dbmet.setUseridByPhone(message.from_user.id,message.contact.phone_number)

#Выполнение команд меню
@bot.message_handler(content_types=["text"])
def handle_text(message):
    global text_task
    global flag
    if message.text == "Бухгалтерия":
        but1=types.KeyboardButton("Запрос справки 2-НДФЛ")
        but2=types.KeyboardButton("В главное меню")
        markup=types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=1)
        if dbmet.getAccess(message.from_user.id) == "Бух":
            markup.add(types.KeyboardButton("Справки в работе"))
        markup.add(but1)
        markup.add(but2)
        bot.send_message(message.chat.id, "БУХГАЛТЕРИЯ:",  reply_markup=markup)
    if message.text == "Запрос справки 2-НДФЛ":
        flag = "2-НДФЛ"
        text_task = "Запрошена справка 2-НДФЛ за "
        but1=types.KeyboardButton("2019 г.")
        but2=types.KeyboardButton("2020 г.")
        but3=types.KeyboardButton("2021 г.")
        but4=types.KeyboardButton("2022 г.")
        but5=types.KeyboardButton("В главное меню")
        markup=types.ReplyKeyboardMarkup(resize_keyboard=True)
        markup.add(but1).add(but2).add(but3).add(but4).add(but5)
        bot.send_message(message.chat.id, "Справка за какой период:",  reply_markup=markup)    
    if (message.text == "2019 г." or message.text =="2020 г." or message.text =="2021 г." or message.text =="2022 г.") and (flag == "2-НДФЛ"):
        text_task = text_task + message.text
        but5=types.KeyboardButton("В главное меню")
        markup=types.ReplyKeyboardMarkup(resize_keyboard=True)
        markup.add(but5)
        bot.send_message(message.chat.id, "Пришлите скан или фото паспорта:",  reply_markup=markup)
    if message.text == "Справки в работе":
        tasks = dbmet.getTasksBuh()
        if not len(tasks):
            bot.send_message(message.chat.id, "Справок в работе НЕТ")
        for task in tasks:
            markupline = types.InlineKeyboardMarkup(row_width=2)
            butline = types.InlineKeyboardButton("Справка готова!", callback_data= "СделалБух_" + str(task[0]))
            markupline.add(butline)
            bot.send_message(message.chat.id, f"{task[1]}\nЗапросил: {task[2]}", reply_markup=markupline)

    if message.text == "В главное меню":
        main_menu(message)
        flag = 0         #обнуление флага
        text_task = ""   #обнуление текста задачи
    
    




#обращается постоянно к серверам телеграмм
bot.polling(non_stop=True, interval=1, timeout=0)