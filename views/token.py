from models import User
import flask_jwt_extended
from flask import Response, request
from flask_restful import Resource
import json
from datetime import timezone, datetime, timedelta

class AccessTokenEndpoint(Resource):
    
    def post(self):
        body = request.get_json() or {}
        # print(body)
        # check username and log in credentials. If valid, return tokens
        username = body.get('username')
        password = body.get('password')

        user = User.query.filter_by(username=username).first()
        if user is None:
            return Response(json.dumps({'message': 'Username not found'}), mimetype="application/json", status=401)

        if user.check_password(password):
            access_token = flask_jwt_extended.create_access_token(identity=user.id)
            refresh_token = flask_jwt_extended.create_refresh_token(identity=user.id)
            return Response(json.dumps({ 
                "access_token": access_token, 
                "refresh_token": refresh_token
            }), mimetype="application/json", status=200)
        else:
            return Response(json.dumps({'message': 'Password is incorrect'}), mimetype="application/json", status=401)


class RefreshTokenEndpoint(Resource):
    
    def post(self):
        body = request.get_json() or {}
        refresh_token = body.get('refresh_token')
        '''
        https://flask-jwt-extended.readthedocs.io/en/latest/refreshing_tokens/
        Hint: To decode the refresh token and see if it expired:
        '''
        try:
            decoded_token = flask_jwt_extended.decode_token(refresh_token)
            exp_timestamp = decoded_token.get("exp")
            current_timestamp = datetime.timestamp(datetime.now(timezone.utc))
            if exp_timestamp < current_timestamp:
                return Response(json.dumps({ 
                        "message": "refresh_token has expired"
                    }), mimetype="application/json", status=401)
            else:
                
                    identity = decoded_token.get("sub")
                    access_token = flask_jwt_extended.create_access_token(identity=identity)
                    return Response(json.dumps({ 
                            "access_token": access_token
                        }), mimetype="application/json", status=200)
        except:
            return Response(json.dumps({ 
                    "message": "bad refresh token"
                }), mimetype="application/json", status=400)
        

def initialize_routes(api):
    api.add_resource(
        AccessTokenEndpoint, 
        '/api/token', '/api/token/'
    )

    api.add_resource(
        RefreshTokenEndpoint, 
        '/api/token/refresh', '/api/token/refresh/'
    )