from flask import jsonify, render_template, request
from bson.objectid import ObjectId

from online_school import *

users_collection = db['users']

login_manager = LoginManager(app)


class User(UserMixin):
    def __init__(self, username, email, password):
        self.username = username
        self.email = email
        self.password = password
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
        user = User(user_data['username'], user_data['email'], user_data['password'])
        user._id = user_data['_id']  # Устанавливаем атрибут _id
        return user
    return None

def get(user_id):
    if user_id is None:
        return None
    user_data = users_collection.find_one({'_id': ObjectId(user_id)})
    if user_data:
        user = User(user_data['username'], user_data['email'], user_data['password'])
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
    return render_template('index.html', username=username)


@app.route('/list_of_topic')
def list_of_topic():
    topics = db.topics.find()
    return render_template('list_of_topic.html', topics=topics)

@app.route('/my-course-page')
def my_course_page():
    return render_template('my_course_page.html')

@app.route('/topic/<topic_id>')
def topic_page(topic_id):
    topic = db.topics_course_page.find_one({'_id': ObjectId(topic_id)})
    if topic:
        return render_template('course_page.html', topic=topic)
    else:
        return 'Тема не найдена'


@app.route('/register', methods=['POST'])
def register():
    data = request.get_json()

    # Получаем значения из данных
    username = data['username']
    email = data['email']
    password = data['password']

    # Создаем нового пользователя
    new_user = User(username, email, password)

    # Добавляем пользователя в базу данных
    db.users.insert_one(new_user.__dict__)  # Предполагается, что users - это коллекция в MongoDB

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


if __name__ == '__main__':
    app.run(debug=True)
