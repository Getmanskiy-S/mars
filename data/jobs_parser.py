from flask_restful import reqparse

parser = reqparse.RequestParser()
parser.add_argument('job', required=True, help="Job title is required")
parser.add_argument('team_leader', type=int, required=True, help="Team leader ID is required")
parser.add_argument('work_size', type=int, required=True, help="Work size in hours is required")
parser.add_argument('collaborators', required=True, help="List of collaborators (comma separated) is required")
parser.add_argument('is_finished', type=bool, required=True, help="Is finished (True/False) is required")