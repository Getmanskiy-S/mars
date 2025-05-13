import sqlalchemy
from sqlalchemy import orm
from .db_session import SqlAlchemyBase


class JobCategory(SqlAlchemyBase):
    __tablename__ = 'job_categories'

    job_id = sqlalchemy.Column(sqlalchemy.Integer, sqlalchemy.ForeignKey('jobs.id'), primary_key=True)
    category_id = sqlalchemy.Column(sqlalchemy.Integer, sqlalchemy.ForeignKey('categories.id'), primary_key=True)

    def __repr__(self):
        return f'<JobCategory> job_id={self.job_id}, category_id={self.category_id}'
