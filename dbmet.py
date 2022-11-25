import sqlite3

#взять имя по номеру телефона
def getNameByPhone(phone):
    conn = sqlite3.connect('database/Klever_database.db', check_same_thread = False) 
    cursor = conn.cursor()
    cursor.execute('SELECT name FROM users WHERE phone = (?)', (phone, ))
    name = cursor.fetchone()
    conn.close()
    return name[0]

#взять userId по имени
def getUserIdByName(name):
    conn = sqlite3.connect('database/Klever_database.db', check_same_thread = False) 
    cursor = conn.cursor()
    cursor.execute('SELECT user_id FROM users WHERE name = (?)', (name, ))
    name = cursor.fetchone()
    conn.close()
    return name[0]

#взять имя заявителя по номеру заявки
def getNameByTask(id):
    conn = sqlite3.connect('database/Klever_database.db', check_same_thread = False) 
    cursor = conn.cursor()
    cursor.execute('SELECT User FROM tasks_buh WHERE id = (?)', (id, ))
    name = cursor.fetchone()
    conn.close()
    return name[0]

#взять имя по ID телеграмма
def getNameById(id):
    conn = sqlite3.connect('database/Klever_database.db', check_same_thread = False) 
    cursor = conn.cursor()
    cursor.execute('SELECT name FROM users WHERE user_id = (?)', (id, ))
    name = cursor.fetchone()
    conn.close()
    return name[0]

#узнать роль пользователя по id телеграмма
def getAccess(id):
    conn = sqlite3.connect('database/Klever_database.db', check_same_thread = False) 
    cursor = conn.cursor()
    cursor.execute('SELECT access FROM users WHERE user_id = (?)', (id, ))
    name = cursor.fetchone()
    conn.close()
    return name[0]

#взять список ID сотрудников по должности:
#Бух  -бухгалтер
def getIdUsers(access):
    conn = sqlite3.connect('database/Klever_database.db', check_same_thread = False) 
    cursor = conn.cursor()
    cursor.execute('SELECT user_id FROM users WHERE access = (?)', (access,))
    users = cursor.fetchall()
    result = []
    for user in users:
        result.append(user[0])
    conn.close()
    return result

#создать задание
def newTask(task,name,photoid):
    conn = sqlite3.connect('database/Klever_database.db', check_same_thread = False) 
    cursor = conn.cursor()
    cursor.execute('INSERT INTO tasks_buh (Task,User,Status,photo) VALUES (?,?,?,?) RETURNING id', (task, name, "Создана", photoid,))
    result = cursor.fetchall()
    conn.commit()
    conn.close()
    return str(result[0][0])

#взять список задач для бухгалетра со статусом "в работе"
def getTasksBuh():
    conn = sqlite3.connect('database/Klever_database.db', check_same_thread = False) 
    cursor = conn.cursor()
    cursor.execute('SELECT id, Task, User FROM Tasks_buh WHERE Status = "В работе"')
    tasks = cursor.fetchall()
    conn.close()
    return tasks

#Установка статуса задачи на "В работе"
def inWork(id):
    conn = sqlite3.connect('database/Klever_database.db', check_same_thread = False) 
    cursor = conn.cursor()
    cursor.execute('UPDATE tasks_buh SET Status = "В работе" WHERE id = (?)', (id,))
    conn.commit()
    conn.close()

#Установка статуса задачи на "Выполнено"
def inClose(id):
    conn = sqlite3.connect('database/Klever_database.db', check_same_thread = False) 
    cursor = conn.cursor()
    cursor.execute('UPDATE tasks_buh SET Status = "Выполнено" WHERE id = (?)', (id,))
    conn.commit()
    conn.close()

#есть ли пользователь с данным номером
def searchByPhone(phone):
    conn = sqlite3.connect('database/Klever_database.db', check_same_thread = False) 
    cursor = conn.cursor()
    info = cursor.execute('SELECT * FROM users WHERE phone = (?)', (phone, ))
    z = info.fetchall()
    conn.close()
    if len(z):
        return False
    else:
        return True

#поместить id телеграмма в таблицу по номеру телефона
def setUseridByPhone(id, phone):
    conn = sqlite3.connect('database/Klever_database.db', check_same_thread = False) 
    cursor = conn.cursor()
    cursor.execute('UPDATE users SET user_id = (?) WHERE phone = (?)', (id,phone,))
    conn.commit()
    conn.close()


