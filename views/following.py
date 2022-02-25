from flask import Response, request
from flask_restful import Resource
from models import Following, User, db
import json
import flask_jwt_extended

def get_path():
    return request.host_url + 'api/posts/'

class FollowingListEndpoint(Resource):
    def __init__(self, current_user):
        self.current_user = current_user
    
    @flask_jwt_extended.jwt_required()
    def get(self):
        # Your code here
        user_id = self.current_user.id
        following_list = Following.query.filter(Following.user_id == user_id).all()

        following = [ item.to_dict_following() for item in following_list ]

        return Response(json.dumps(following), mimetype="application/json", status=200)

    @flask_jwt_extended.jwt_required()
    def post(self):
        # Your code here
        body = request.get_json()
        following_id = body.get('user_id')
        user_id = self.current_user.id

        # check user_id
        if following_id:
            try:
                following_id = int(following_id)
            except:
                return Response(json.dumps({'message': 'user_id must be a integer'}), mimetype="application/json", status=400)
        else:
            return Response(json.dumps({'message': 'user_id is required'}), mimetype="application/json", status=400)

        # get users that i already follow to check for duplicates
        following_list = Following.query.filter(Following.user_id == user_id).all()
        following_list = [ x.following_id for x in following_list ]

        if following_id in following_list:
            return Response(json.dumps({'message': 'You already follow this user'}), mimetype="application/json", status=400)


        following = Following(user_id, following_id)
        try:
            db.session.add(following)
            db.session.commit()
        except:
            return Response(json.dumps({'message': 'Invalid id'}), mimetype="application/json", status=404)

        return Response(json.dumps(following.to_dict_following()), mimetype="application/json", status=201)


class FollowingDetailEndpoint(Resource):
    def __init__(self, current_user):
        self.current_user = current_user
    
    @flask_jwt_extended.jwt_required()
    def delete(self, id):
        # Your code here
        try:
            id = int(id)
        except:
            return Response(json.dumps({'message': 'id must be a integer'}), mimetype="application/json", status=400)

        following = Following.query.get(id)
        if not following or following.user_id != self.current_user.id:
            return Response(json.dumps({'message': 'Following does not exist'}), mimetype="application/json", status=404)
       

        Following.query.filter_by(id=id).delete()
        db.session.commit()
        serialized_data = {
            'message': 'Following {0} successfully deleted.'.format(id)
        }
        return Response(json.dumps(serialized_data), mimetype="application/json", status=200)
        


def initialize_routes(api):
    api.add_resource(
        FollowingListEndpoint, 
        '/api/following', 
        '/api/following/', 
        resource_class_kwargs={'current_user': flask_jwt_extended.current_user}
    )
    api.add_resource(
        FollowingDetailEndpoint, 
        '/api/following/<id>', 
        '/api/following/<id>/', 
        resource_class_kwargs={'current_user': flask_jwt_extended.current_user}
    )
