from flask import Response
from flask_restful import Resource
from models import LikePost, db
import json
from . import can_view_post
import flask_jwt_extended

class PostLikesListEndpoint(Resource):

    def __init__(self, current_user):
        self.current_user = current_user
    
    @flask_jwt_extended.jwt_required()
    def post(self, post_id):
        # Your code here
        user_id = self.current_user.id

        try:
            post_id = int(post_id)
        except:
            return Response(json.dumps({'message': 'post_id must be a integer'}), mimetype="application/json", status=400)

        # check if user has access to post+if post id is a valid post
        try:
            if not can_view_post(post_id, self.current_user):
                return Response(json.dumps({'message': 'Post could not be found'}), mimetype="application/json", status=404)
        except:
            return Response(json.dumps({'message': 'Post with the id could not be found'}), mimetype="application/json", status=404)

        like_post = LikePost(user_id, post_id)
        try:
            db.session.add(like_post)
            db.session.commit()
        except:
            return Response(json.dumps({'message': 'Duplicate post'}), mimetype="application/json", status=400)
        return Response(json.dumps(like_post.to_dict()), mimetype="application/json", status=201)

class PostLikesDetailEndpoint(Resource):

    def __init__(self, current_user):
        self.current_user = current_user
    
    @flask_jwt_extended.jwt_required()
    def delete(self, post_id, id):
        # Your code here
        try:
            id = int(id)
        except:
            return Response(json.dumps({'message': 'like_id must be a integer'}), mimetype="application/json", status=400)

        like_post = LikePost.query.get(id)
        if not like_post or like_post.user_id != self.current_user.id:
            return Response(json.dumps({'message': 'Like does not exist'}), mimetype="application/json", status=404)

        LikePost.query.filter_by(id=id).delete()
        db.session.commit()
        serialized_data = {
            'message': 'Like {0} successfully deleted.'.format(id)
        }
        return Response(json.dumps(serialized_data), mimetype="application/json", status=200)



def initialize_routes(api):
    api.add_resource(
        PostLikesListEndpoint, 
        '/api/posts/<post_id>/likes', 
        '/api/posts/<post_id>/likes/', 
        resource_class_kwargs={'current_user': flask_jwt_extended.current_user}
    )

    api.add_resource(
        PostLikesDetailEndpoint, 
        '/api/posts/<post_id>/likes/<id>', 
        '/api/posts/<post_id>/likes/<id>/',
        resource_class_kwargs={'current_user': flask_jwt_extended.current_user}
    )
