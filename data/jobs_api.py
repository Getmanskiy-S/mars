import flask

from . import db_session
from .jobs import Jobs

blueprint = flask.Blueprint(
    'jobs_api',
    __name__,
    template_folder='templates'
)


@blueprint.route('/api/jobs')
def get_jobs():
    db_sess = db_session.create_session()
    jobs = db_sess.query(Jobs).all()
    return flask.jsonify({'jobs': [item.to_dict(
        only=('id', 'job', 'team_leader', 'work_size', 'collaborators', 'start_date', 'end_date', 'is_finished')) for
        item in jobs]})


@blueprint.route('/api/jobs/<int:job_id>')
def get_one_job(job_id):
    db_sess = db_session.create_session()
    jobs = db_sess.query(Jobs).get(job_id)
    if not jobs:
        return flask.make_response(flask.jsonify({'error': 'Not found'}), 404)
    return flask.jsonify({'jobs': jobs.to_dict(
        only=('id', 'job', 'team_leader', 'work_size', 'collaborators', 'start_date', 'end_date', 'is_finished'))})


@blueprint.route('/api/jobs/<string:job_id>')
def get_one_job_string(job_id):
    return flask.make_response(flask.jsonify({'error': 'TypeError'}), 404)


@blueprint.route('/api/jobs', methods=['POST'])
def create_job():
    if not flask.request.json:
        return flask.make_response(flask.jsonify({'error': 'Empty request'}), 404)
    elif not all(key in flask.request.json for key in ['job', 'team_leader', 'work_size', 'collaborators']):
        return flask.make_response(flask.jsonify({'error': 'Bad request'}), 404)

    db_sess = db_session.create_session()
    job = Jobs(
        job=flask.request.json['job'],
        team_leader=flask.request.json['team_leader'],
        work_size=flask.request.json['work_size'],
        collaborators=flask.request.json['collaborators'],
        is_finished=flask.request.json['is_finished']
    )
    db_sess.add(job)
    db_sess.commit()
    return flask.jsonify({'id': job.id})


@blueprint.route('/api/jobs/<int:job_id>', methods=['DELETE'])
def delete_job(job_id):
    db_sess = db_session.create_session()
    job = db_sess.query(Jobs).get(job_id)

    if not job:
        return flask.make_response(flask.jsonify({'error': 'Not found'}), 404)

    db_sess.delete(job)
    db_sess.commit()

    return flask.make_response('', 204)


@blueprint.route('/api/jobs/<int:job_id>', methods=['PUT'])
def edit_job(job_id):
    if not flask.request.json:
        return flask.make_response(flask.jsonify({'error': 'Empty request'}), 400)

    db_sess = db_session.create_session()
    job = db_sess.query(Jobs).get(job_id)

    if not job:
        return flask.make_response(flask.jsonify({'error': 'Not found'}), 404)

    # Обновляем поля работы из JSON (если они присутствуют)
    if 'job' in flask.request.json:
        job.job = flask.request.json['job']
    if 'team_leader' in flask.request.json:
        job.team_leader = flask.request.json['team_leader']
    if 'work_size' in flask.request.json:
        job.work_size = flask.request.json['work_size']
    if 'collaborators' in flask.request.json:
        job.collaborators = flask.request.json['collaborators']
    if 'is_finished' in flask.request.json:
        job.is_finished = flask.request.json['is_finished']

    db_sess.commit()

    # Возвращаем обновленную работу
    return flask.jsonify({'job': job.to_dict(
        only=('id', 'job', 'team_leader', 'work_size', 'collaborators', 'start_date', 'end_date', 'is_finished'))})