import pymongo
from pymongo import MongoClient

# Подключение к MongoDB (замените параметры подключения на ваши)
client = MongoClient('mongodb://localhost:27017/')
db = client['online-school']  # Выбираем базу данных (testdb)

# Определим коллекцию (эквивалент таблицы в реляционных базах данных)
collection = db['users']


# Функция для добавления пользователя в базу данных
def add_user(username, email):
    # Проверяем наличие пользователя с таким именем
    if find_user(email):
        print(f'Пользователь с электронной почтой {email} уже существует')
        return

    user_data = {'username': username, 'email': email}
    collection.insert_one(user_data)
    print(f'Пользователь {username} успешно добавлен')


# Функция для поиска пользователя по имени
def find_user(email):
    return collection.find_one({'email': email})


# Примеры тестовых сценариев
if __name__ == '__main__':
    # Добавляем пользователя
    add_user('gucci', 'johndoe@example.com')
    add_user('Ihjn', 'anotherjohndoe@example.com')  # Попытка добавить пользователя с существующим именем
