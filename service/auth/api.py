from flask_restful import Resource, abort
from flask import request, make_response, jsonify

from service.database import db, bcrypt
from service.models import Organisation, User

DEFAULT_ORGANISATION_CREDIT = 400
DEFAULT_USER_CREDIT = 50
DEFAULT_ORGANISATION_NAME = 'Industry User'

class CounterApi(Resource):
    """
    Counter Resource
    """

    def get(self):
        # extract the auth token
        auth_header = request.headers.get('Authorization')

        if auth_header:
            try:
                auth_token = auth_header.split(" ")[1]
            except IndexError:
                responseObject = {
                    'status': 'fail',
                    'message': 'Bearer token malformed.'
                }
                return make_response(jsonify(responseObject), 401)
        else:
            auth_token = ''


        if auth_token:
            resp = Organisation.decode_auth_token(auth_token)
            user_id = resp

            # fetch organisation information
            organisation = Organisation.query.first()
            if organisation:
                organisation_credit = organisation.credit
                organisation_tally = organisation.tally
            else:
                organisation_credit = DEFAULT_ORGANISATION_CREDIT
                organisation_tally = 0

            # fetch user information
            user = db.session.query(User).filter_by(id=user_id).first()
            if user is None:
                user_credit = DEFAULT_USER_CREDIT
                user_tally = 0
            else:
                user_credit = user.credit
                user_tally = user.tally


            responseObject = {
                'status': 'success',
                'message': 'user credit',
                'organisation':{
                    'credit': organisation_credit,
                    'tally': organisation_tally,
                },
                'user':{
                    'credit': user_credit,
                    'tally': user_tally,
                }
            }
            return make_response(jsonify(responseObject), 200)
        else:
            responseObject = {
                'status': 'fail',
                'message': 'Provide a valid auth token.'
            }
            return make_response(jsonify(responseObject), 401)



    def post(self):
        # extract the auth token
        auth_header = request.headers.get('Authorization')
        if auth_header:
            try:
                auth_token = auth_header.split(" ")[1]
            except IndexError:
                responseObject = {
                    'status': 'fail',
                    'message': 'Bearer token malformed.'
                }
                return make_response(jsonify(responseObject), 401)
        else:
            auth_token = ''
        if auth_token:
            resp = Organisation.decode_auth_token(auth_token)

            if not isinstance(resp, str):
                user_id = resp

                organisation = Organisation.query.first()
                # create the counter if we need to
                if organisation is None:
                    organisation = Organisation(
                        name=DEFAULT_ORGANISATION_NAME,
                        credit=DEFAULT_ORGANISATION_CREDIT)

                # create the user if we need to
                user = db.session.query(User).filter_by(id=user_id).first()
                if user is None:
                    user = User(organisation=organisation, credit=DEFAULT_USER_CREDIT)

                if organisation.credit < 1 or user.credit < 1:
                    responseObject = {
                        'status': 'error',
                        'message': 'insufficient organisation credit remaining',
                        'organisation': {
                            'name': organisation.name,
                            'tally': organisation.tally,
                            'credit': organisation.credit
                        },
                        'user': {
                            'id': user_id,
                            'credit': user.credit,
                            'tally': user.tally,
                        }
                    }
                    return make_response(jsonify(responseObject), 200)
                else:
                    # decrement credit
                    organisation.credit = organisation.credit - 1
                    user.credit = user.credit - 1

                    # increment tally
                    organisation.tally = organisation.tally + 1
                    user.tally = user.tally + 1

                    db.session.add(organisation)
                    db.session.add(user)
                    db.session.commit()

                    # TODO re-query to check persistence of updated fields
                    responseObject = {
                        'status': 'success',
                        'message': 'updated tally',
                        'organisation': {
                            'name': organisation.name,
                            'tally': organisation.tally,
                            'credit': organisation.credit
                        },
                        'user': {
                            'id': user_id,
                            'credit': user.credit,
                            'tally': user.tally,
                        }
                    }
                    return make_response(jsonify(responseObject), 200)
            responseObject = {
                'status': 'fail',
                'message': resp
            }
            return make_response(jsonify(responseObject), 401)
        else:
            responseObject = {
                'status': 'fail',
                'message': 'Provide a valid auth token.'
            }
            return make_response(jsonify(responseObject), 401)
