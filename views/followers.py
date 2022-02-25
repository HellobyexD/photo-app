from flask import Response, request
from flask_restful import Resource
from models import Following, User
import json
import flask_jwt_extended

def get_path():
    return request.host_url + 'api/posts/'

class FollowerListEndpoint(Resource):
    def __init__(self, current_user):
        self.current_user = current_user
    
    @flask_jwt_extended.jwt_required()
    def get(self):
        # Your code here
        user_id = self.current_user.id
        followers = Following.query.filter(Following.following_id == user_id).all()
        #follower_ids = [follower.user_id for follower in followers]
        #followers = User.query.filter(User.id.in_(follower_ids)).order_by(User.id).all()
        followers = [ item.to_dict_follower() for item in followers ]

        return Response(json.dumps(followers), mimetype="application/json", status=200)

def initialize_routes(api):
    api.add_resource(
        FollowerListEndpoint, 
        '/api/followers', 
        '/api/followers/', 
        resource_class_kwargs={'current_user': flask_jwt_extended.current_user}
    )
