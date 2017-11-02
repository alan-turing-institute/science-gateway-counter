from flask_restful import Resource, abort
from flask import request, make_response, jsonify

from service.database import db, bcrypt
from service.models import Organisation, User

DEFAULT_TOTAL_CREDIT = 30


class CounterApi(Resource):
    """
    Counter Resource
    """

    def get(self):
        organisation = Organisation.query.first()
        if organisation:
            credit = organisation.credit
        else:
            credit = DEFAULT_TOTAL_CREDIT

        responseObject = {"credit": credit}
        return make_response(jsonify(responseObject), 200)

    def post(self):
        # get the auth token
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
                    organisation = Organisation(credit=DEFAULT_TOTAL_CREDIT)

                # create the user if we need to
                user = db.session.query(User).filter_by(id=user_id).first()

                if user is None:
                    user = User(organisation=organisation)

                if organisation.credit < 1:
                    responseObject = {
                        'status': 'error',
                        'message': 'insufficient organisation credit remaining',
                        'data': {
                            'user_id': user_id,
                            'organisation_credit': organisation.credit,
                            'organisation_tally': organisation.tally,
                            'user_tally': user.tally
                        }
                    }
                    return make_response(jsonify(responseObject), 200)
                else:
                    # decrement credit
                    organisation.credit = organisation.credit - 1

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
                        'data': {
                            'user_id': user_id,
                            'organisation_credit': organisation.credit,
                            'organisation_tally': organisation.tally,
                            'user_tally': user.tally
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
