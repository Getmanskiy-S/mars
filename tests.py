from data import db_session
from data.users import User

def main():
    # Считываем имя базы данных из консоли
    db_name = input("Введите имя базы данных: ")

    # Инициализируем подключение к базе данных
    db_session.global_init(db_name)
    db_sess = db_session.create_session()

    # Выполняем запрос к базе данных для получения всех колонистов, проживающих в первом модуле
    colonists = db_sess.query(User).filter(User.address == 'module_1').all()

    # Выводим каждого колониста с новой строки
    for colonist in colonists:
        print(colonist)

if __name__ == '__main__':
    main()