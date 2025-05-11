from flask import abort
from flask_restful import reqparse, Resource
from data.jobs import Jobs
from data import db_session

# Импортируем парсер аргументов (его мы создадим позже)
from . import jobs_parser


class JobsResource(Resource):
    def get(self, job_id):
        """Получение информации о работе по ID."""
        db_sess = db_session.create_session()
        job = db_sess.query(Jobs).get(job_id)
        if not job:
            abort(404, message=f"Job {job_id} not found")
        return job.to_dict(only=('id', 'job', 'team_leader', 'work_size', 'collaborators', 'is_finished'))

    def delete(self, job_id):
        """Удаление работы по ID."""
        db_sess = db_session.create_session()
        job = db_sess.query(Jobs).get(job_id)
        if not job:
            abort(404, message=f"Job {job_id} not found")
        db_sess.delete(job)
        db_sess.commit()
        return '', 204  # Стандартный код успешного удаления

    def put(self, job_id):
        """Редактирование работы по ID."""
        args = jobs_parser.parser.parse_args()  # Используем парсер
        db_sess = db_session.create_session()
        job = db_sess.query(Jobs).get(job_id)
        if not job:
            abort(404, message=f"Job {job_id} not found")

        # Обновляем поля работы, только если они переданы
        if args['job']:
            job.job = args['job']
        if args['team_leader']:
            job.team_leader = args['team_leader']
        if args['work_size']:
            job.work_size = args['work_size']
        if args['collaborators']:
            job.collaborators = args['collaborators']
        if args['is_finished'] is not None:  # is_finished - булево значение!
            job.is_finished = args['is_finished']

        db_sess.commit()
        return job.to_dict(only=('id', 'job', 'team_leader', 'work_size', 'collaborators', 'is_finished'))


class JobsListResource(Resource):
    def get(self):
        """Получение списка всех работ."""
        db_sess = db_session.create_session()
        jobs = db_sess.query(Jobs).all()
        return {'jobs': [item.to_dict(
            only=('id', 'job', 'team_leader', 'work_size', 'collaborators', 'is_finished')) for item in jobs]}

    def post(self):
        """Создание новой работы."""
        args = jobs_parser.parser.parse_args()  # Используем парсер
        db_sess = db_session.create_session()
        job = Jobs(
            job=args['job'],
            team_leader=args['team_leader'],
            work_size=args['work_size'],
            collaborators=args['collaborators'],
            is_finished=args['is_finished']
        )
        db_sess.add(job)
        db_sess.commit()
        return {'id': job.id}, 201  # 201 - код успешного создания
