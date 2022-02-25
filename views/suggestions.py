from flask import Response, request
from flask_restful import Resource
from models import User, Following
from . import get_authorized_user_ids
import json
import flask_jwt_extended

class SuggestionsListEndpoint(Resource):

    def __init__(self, current_user):
        self.current_user = current_user
    
    @flask_jwt_extended.jwt_required()
    def get(self):
        # Your code here:
        user_id = self.current_user.id
        following_list = Following.query.filter(Following.user_id == user_id).all()
        following_ids = [following.following_id for following in following_list]
        following_ids = get_authorized_user_ids(self.current_user)

        not_following = User.query.filter(User.id.notin_(following_ids)).order_by(User.id).limit(7).all()
        not_following = [ item.to_dict() for item in not_following ]
        return Response(json.dumps(not_following), mimetype="application/json", status=200)


def initialize_routes(api):
    api.add_resource(
        SuggestionsListEndpoint, 
        '/api/suggestions', 
        '/api/suggestions/', 
        resource_class_kwargs={'current_user': flask_jwt_extended.current_user}
    )
