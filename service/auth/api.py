from flask_restful import Resource, abort, request
from flask import request, make_response, jsonify

class UserApi(Resource):
    """
    User Resource
    """

    def __init__(self, **kwargs):
        pass

    def get(self):
        json_response = {'foo': 'bar'}
        return json_response, 200, {'Content-Type': 'application/json'}
