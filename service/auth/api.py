from flask_restful import Resource, abort, request
from flask import request, make_response, jsonify

from service.models import User, BlacklistToken

class UserApi(Resource):
    """
    User Resource
    """

    def __init__(self, **kwargs):
        pass

    def get(self):
        responseObject = {
                'status': 'fail',
                'message': 'User already exists. Please Log in.',
            }
        return make_response(jsonify(responseObject), 200)


# class UserAPI(Resource):
#     """
#     User Resource
#     """
#     def get(self):
#         # get the auth token
#         auth_header = request.headers.get('Authorization')
#         if auth_header:
#             try:
#                 auth_token = auth_header.split(" ")[1]
#             except IndexError:
#                 responseObject = {
#                     'status': 'fail',
#                     'message': 'Bearer token malformed.'
#                 }
#                 return make_response(jsonify(responseObject)), 401
#         else:
#             auth_token = ''
#         if auth_token:
#             resp = User.decode_auth_token(auth_token)
#             if not isinstance(resp, str):
#                 user = User.query.filter_by(id=resp).first()
#
#                 # note this information is not stored in the token,
#                 # (the token is used to access the db and fetch this information)
#                 responseObject = {
#                     'status': 'success',
#                     'data': {
#                         'user_id': user.id,
#                         'username': user.username,
#                         'admin': user.admin,
#                         'registered_on': user.registered_on
#                     }
#                 }
#                 return make_response(jsonify(responseObject)), 200
#             responseObject = {
#                 'status': 'fail',
#                 'message': resp
#             }
#             return make_response(jsonify(responseObject)), 401
#         else:
#             responseObject = {
#                 'status': 'fail',
#                 'message': 'Provide a valid auth token.'
#             }
#             return make_response(jsonify(responseObject)), 401
