import os
import sys
import telebot
from pprint import pprint
from string import Template
import mysql.connector
from mysql.connector import errorcode

# Telegram your token
bot = telebot.TeleBot(")
# Telegram your group id
group_id = -1

# получить id канала/группы
#print(bot.get_chat('@botanskiytest').id)

try:
    db = mysql.connector.connect(
      host="localhost",
      user="root",
      passwd="%%%",
      port="1111",
      database="t"
    )
except mysql.connector.Error as err:
  if err.errno == errorcode.ER_ACCESS_DENIED_ERROR:
    print("Что-то не так с вашим именем пользователя или паролем")
    sys.exit()
  elif err.errno == errorcode.ER_BAD_DB_ERROR:
    print("База данных не существует")
    sys.exit()
  else:
    print(err)
    sys.exit()

cursor = db.cursor()

#cursor.execute("CREATE DATABASE tradebot")

#cursor.execute("CREATE TABLE regs (id INT AUTO_INCREMENT PRIMARY KEY, \
#first_name VARCHAR(255), phone VARCHAR(255), description VARCHAR(255), user_id INT(11))")

#cursor.execute("CREATE TABLE users (id INT AUTO_INCREMENT PRIMARY KEY, \
#first_name VARCHAR(255), phone VARCHAR(255), telegram_user_id INT(11) UNIQUE)")

user_data = {}

class User:
    def __init__(self, first_name):
        self.first_name = first_name
        self.phone = ''
       ]

@bot.message_handler(commands=['start', 'help'])
def send_welcome(message):
        msg = bot.send_message(message.chat.id, "Введите имя и фамилию")
        bot.register_next_step_handler(msg, process_firstname_step)

def process_firstname_step(message):
    try:
        user_id = message.from_user.id
        user_data[user_id] = User(message.text)

        # pprint(vars(message))
        # message.photo[-1].file_id
        # bot.send_photo(group_id, message.photo[-1].file_id)

        #msg = bot.send_message(message.chat.id, "Отправьте фотографию желаемого товара")
        #bot.register_next_step_handler(msg, process_photo_step)
    #except Exception as e:
        #bot.reply_to(message, 'oooops')

#def process_photo_step(message):
    #try:
        #if message.content_type == 'photo':
            #user_id = message.from_user.id
            #user = user_data[user_id]
            #user.photo_id = message.photo[-1].file_id

        msg = bot.send_message(message.chat.id, "Напишите данные для отправки")
        bot.register_next_step_handler(msg, process_description_step)
        #else:
            #bot.reply_to(message, 'Это не фотография, пришлите пожалуйста фото.')
            #process_photo_step(message)
    except Exception as e:
        bot.reply_to(message, 'oooops')

def process_description_step(message):
    try:
        user_id = message.from_user.id
        user = user_data[user_id]
        user.description = message.text

        # Проверка есть ли пользователь в БД
        sql = "SELECT * FROM users WHERE telegram_user_id = {0}".format(user_id)
        cursor.execute(sql)
        existsUser = cursor.fetchone()

        # Если нету, то добавить в БД
        if (existsUser == None):
               sql = "INSERT INTO users (first_name, phone, telegram_user_id) \
                                  VALUES (%s, %s, %s)"
               val = (message.from_user.first_name, message.from_user.phone, user_id)
               cursor.execute(sql, val)

        # Регистрация заявки
        sql = "INSERT INTO regs (first_name, phone, description, user_id) \
                                  VALUES (%s, %s, %s, %s)"
        val = (user.first_name, user.phone, user.description, user_id)
        cursor.execute(sql, val)
        db.commit()

        # Сохранение фото на сервере
        #file_photo = bot.get_file(user.photo_id)
        #filename, file_extension = os.path.splitext(file_photo.file_path)
a
        #downloaded_file_photo = bot.download_file(file_photo.file_path)

        #src = 'photos/' + user.photo_id + file_extension
        #with open(src, 'wb') as new_file:
         #   new_file.write(downloaded_file_photo)

        bot.send_message(message.chat.id, "Вы успешно зарегистрированны!")
        #bot.send_message(group_id, getRegData(user, 'Заявка от бота', bot.get_me().username), parse_mode="Markdown")
        #bot.send_photo(group_id) #, user.photo_id)

    except Exception as e:
        bot.reply_to(message, 'oooops')

# формирует вид заявки регистрации
# нельзя делать перенос строки Template
# в send_message должно стоять parse_mode="Markdown"
#def getRegData(user, title, name):
 #   t = Template('$title *$name* \nИмя: *$phone*\nТелефон: *$last_name* \nОписание: *$description*')

  #  return t.substitute({
   #     'title': title,
    #    'name' : name,
     #   'first_name': user.first_name,
      #  'phone': user.phone,
       # 'description': user.description
#})
