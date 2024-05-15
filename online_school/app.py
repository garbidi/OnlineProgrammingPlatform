from flask import jsonify, render_template, request, session, abort, redirect, url_for
from bson.objectid import ObjectId
import re
from werkzeug.security import generate_password_hash


from online_school import *

users_collection = db['users']
topics_collection=db['topics_course_page']
lessons = db['lessons']
login_manager = LoginManager(app)


class User(UserMixin):
    def __init__(self, username, email, password, added_topics=None):
        self.username = username
        self.email = email
        self.password = password
        self.added_topics = added_topics or ''
        self._id = None  # Добавляем атрибут _id

    def get_id(self):
        # Возвращаем строковое представление _id
        return str(self._id)

    def save(self):
        user_data = {
            'full_name': self.username,
            'email': self.email,
            'password': self.password
        }
        result = db.users.insert_one(user_data)
        self._id = result.inserted_id

@login_manager.user_loader
def load_user(user_id):
    return get(user_id)


def find_user_by_email(email):
    user_data = users_collection.find_one({'email': email})
    if user_data:
        user = User(user_data['username'], user_data['email'], user_data['password'], user_data.get('added_topics', ''))
        user._id = user_data['_id']  # Устанавливаем атрибут _id
        return user
    return None

def update_user_enrolled_courses(user_id, topic_id):
    users_collection.update_one(
        {"_id": ObjectId(user_id)},
        {"$addToSet": {"enrolled_courses": topic_id}}
    )

def get(user_id):
    if user_id is None:
        return None
    user_data = users_collection.find_one({'_id': ObjectId(user_id)})
    if user_data:
        user = User(user_data['username'], user_data['email'], user_data['password'], user_data.get('added_topics', ''))
        user._id = user_data['_id']  # Устанавливаем атрибут _id
        return user
    return None


def check_password(user, password):
    return user.password == password


@app.route('/login', methods=['POST'])
def login():
    data = request.get_json()
    email = data.get('email')
    password = data.get('password')

    user = find_user_by_email(email)
    if user and check_password(user, password):
        login_user(user)
        session['user_id'] = str(user.get_id())  # Добавление user_id в сессию
        session['user_email'] = user.email
        return jsonify({'success': True, 'message': 'Успешный вход'}), 200
    else:
        return jsonify({'error': 'Неверные учетные данные'}), 401


@app.route('/check_auth', methods=['GET'])
def check_auth():
    if current_user.is_authenticated:
        return jsonify({'is_authenticated': True, 'email': current_user.email})
    else:
        return jsonify({'is_authenticated': False})


@app.route('/logout', methods=['POST'])
def logout():
    logout_user()
    return jsonify({'success': True})


@app.route('/')
def index():
    if current_user.is_anonymous:
        username = ''
    else:
        username = current_user.email
    return render_template('Code_editior.html', username=username)


@app.route('/list_of_topic')
def list_of_topic():
    topics = db.topics.find()
    return render_template('list_of_topic.html', topics=topics)

@app.route('/my-course-page')
def my_course_page():
    return render_template('my_course_page.html')


@app.route('/my_started_course')
def my_started_course():
    topic_id = request.args.get('topic_id')
    if not topic_id:
        return "Ошибка: topic_id не указан", 400

    main = topics_collection.find_one({'_id': ObjectId(str(topic_id))})

    # Поиск документа в коллекции lessons, где topic_id совпадает с регулярным выражением
    topic_doc = db.lessons.find_one({'topic_id': f'ObjectId("{topic_id}")'})

    if not topic_doc:
        return "Ошибка: контента нет пока что. Ждите", 404

    lessons = list(topic_doc['materials'])

    return render_template('my_started_course.html', topic=main, materials=topic_doc['materials'])


@app.route('/topic/<topic_id>')
def topic_page(topic_id):
    topic = db.topics_course_page.find_one({'_id': ObjectId(topic_id)})
    if topic:
        return render_template('course_page.html', topic=topic)
    else:
        return 'Тема не найдена'


def validate_user_data(username, email, password):
    if not username or not email or not password:
        abort(400, description='Необходимо заполнить все поля')

@app.route('/register', methods=['POST'])
def register():
    data = request.get_json()
    validate_user_data(data['username'], data['email'], data['password'])

    # Проверка наличия всех необходимых полей
    username = data.get('username')
    email = data.get('email')
    password = data.get('password')
    if not username or not email or not password:
        abort(400, description='Необходимо заполнить все поля')

    # Проверка, что пользователь с таким email ещё не зарегистрирован
    if find_user_by_email(email):
        return jsonify({'error': 'Пользователь с таким email уже существует'}), 400

    # Хэширование пароля
    hashed_password = generate_password_hash(password)

    # Создание нового пользователя
    new_user = User(username, email, hashed_password)
    new_user.save()  # Сохранение пользователя в базу данных

    return jsonify({'message': 'Регистрация прошла успешно!'}), 200

@app.route('/api/topics', methods=['GET'])
def get_topics():
    topics = db.topics_course_page.find()
    topic_list = []
    for topic in topics:
        topic_data = {
            '_id': str(topic['_id']),
            'title': topic['title'],
            'description': topic['description'],
            'content': topic['content'],
            'duration': topic['duration']
        }
        topic_list.append(topic_data)
    return jsonify(topic_list)

@app.route('/get_user_email', methods=['GET'])
def get_user_email():
    user_email = session.get('user_email')
    if user_email:
        return jsonify({'email': user_email}), 200
    else:
        return jsonify({'error': 'Email пользователя не найден в сессии'}), 404

@app.route("/add_topic_to_user", methods=["POST"])
def add_topic_to_user():
    if not current_user.is_authenticated:
        return jsonify({"success": False, "error": "Пользователь не авторизован"}), 401

    # Получить название темы из запроса
    topic_name = request.json.get("topic_name")

    # Найти тему по названию
    topic = topics_collection.find_one({"name": topic_name})
    if not topic:
        return jsonify({"success": False, "error": "Тема не найдена"}), 404

    topic_id = topic["_id"]
    user_id = str(current_user.id)

    # Обновить документ пользователя, добавив topic_id в enrolled_courses
    update_user_enrolled_courses(user_id, topic_id)

    return jsonify({"success": True})


@app.route('/my_course_page/<string:email>', methods=['GET'])
def user_topics(email):
    user = find_user_by_email(email)
    if user:
        added_topics = user.added_topics.split(',') if user.added_topics else []
        topic_details = []
        for topic_id in added_topics:
            topic = topics_collection.find_one({'title': topic_id})
            if topic:
                topic_details.append({
                    '_id': str(topic['_id']),  # Преобразование ObjectId в строку
                    'title': topic['title'],
                    'description': topic['description'],
                    'duration': topic['duration']
                })
        return jsonify({'topics': topic_details})
    return jsonify({'topics': []})

if __name__ == '__main__':
    app.run(debug=True)
