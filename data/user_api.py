import flask
from . import db_session
from .users import User  # Импортируем модель User

blueprint = flask.Blueprint(
    'users_api',
    __name__,
    template_folder='templates'
)


# 1. Получение всех пользователей (GET /api/users)
@blueprint.route('/api/users')
def get_users():
    """Возвращает JSON со списком всех пользователей."""
    db_sess = db_session.create_session()
    users = db_sess.query(User).all()
    return flask.jsonify({'users': [item.to_dict(
        only=('id', 'surname', 'name', 'age', 'position', 'speciality', 'address', 'email')) for item in users]})


# 2. Получение одного пользователя по ID (GET /api/users/<int:user_id>)
@blueprint.route('/api/users/<int:user_id>')
def get_one_user(user_id):
    """Возвращает JSON с информацией об одном пользователе."""
    db_sess = db_session.create_session()
    user = db_sess.query(User).get(user_id)
    if not user:
        return flask.make_response(flask.jsonify({'error': 'Not found'}), 404)
    return flask.jsonify({'user': user.to_dict(
        only=('id', 'surname', 'name', 'age', 'position', 'speciality', 'address', 'email'))})


# 3. Добавление пользователя (POST /api/users)
@blueprint.route('/api/users', methods=['POST'])
def create_user():
    """Создает нового пользователя."""
    if not flask.request.json:
        return flask.make_response(flask.jsonify({'error': 'Empty request'}), 400)
    elif not all(key in flask.request.json for key in
                 ['surname', 'name', 'age', 'position', 'speciality', 'address', 'email']):
        return flask.make_response(flask.jsonify({'error': 'Bad request'}), 400)

    db_sess = db_session.create_session()
    # Проверка, что пользователя с таким email еще нет
    if db_sess.query(User).filter(User.email == flask.request.json['email']).first():
        return flask.make_response(flask.jsonify({'error': 'Email already exists'}), 400)

    user = User(
        surname=flask.request.json['surname'],
        name=flask.request.json['name'],
        age=flask.request.json['age'],
        position=flask.request.json['position'],
        speciality=flask.request.json['speciality'],
        address=flask.request.json['address'],
        email=flask.request.json['email']
    )
    db_sess.add(user)
    db_sess.commit()
    return flask.jsonify({'id': user.id})


# 4. Редактирование пользователя (PUT /api/users/<int:user_id>)
@blueprint.route('/api/users/<int:user_id>', methods=['PUT'])
def edit_user(user_id):
    """Редактирует существующего пользователя."""
    if not flask.request.json:
        return flask.make_response(flask.jsonify({'error': 'Empty request'}), 400)

    db_sess = db_session.create_session()
    user = db_sess.query(User).get(user_id)

    if not user:
        return flask.make_response(flask.jsonify({'error': 'Not found'}), 404)

    # Обновляем поля пользователя из JSON (если они присутствуют)
    if 'surname' in flask.request.json:
        user.surname = flask.request.json['surname']
    if 'name' in flask.request.json:
        user.name = flask.request.json['name']
    if 'age' in flask.request.json:
        user.age = flask.request.json['age']
    if 'position' in flask.request.json:
        user.position = flask.request.json['position']
    if 'speciality' in flask.request.json:
        user.speciality = flask.request.json['speciality']
    if 'address' in flask.request.json:
        user.address = flask.request.json['address']
    if 'email' in flask.request.json:
        # Проверяем, что новый email не занят другим пользователем
        if db_sess.query(User).filter(User.email == flask.request.json['email'], User.id != user_id).first():
            return flask.make_response(flask.jsonify({'error': 'Email already exists'}), 400)
        user.email = flask.request.json['email']

    db_sess.commit()
    return flask.jsonify({'user': user.to_dict(
        only=('id', 'surname', 'name', 'age', 'position', 'speciality', 'address', 'email'))})


# 5. Удаление пользователя (DELETE /api/users/<int:user_id>)
@blueprint.route('/api/users/<int:user_id>', methods=['DELETE'])
def delete_user(user_id):
    """Удаляет пользователя."""
    db_sess = db_session.create_session()
    user = db_sess.query(User).get(user_id)

    if not user:
        return flask.make_response(flask.jsonify({'error': 'Not found'}), 404)

    db_sess.delete(user)
    db_sess.commit()
    return flask.make_response('', 204)
