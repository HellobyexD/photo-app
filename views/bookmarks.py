from flask import Response, request
from flask_restful import Resource
from models import Bookmark, db
import json
from . import can_view_post
import flask_jwt_extended

class BookmarksListEndpoint(Resource):

    def __init__(self, current_user):
        self.current_user = current_user
    
    @flask_jwt_extended.jwt_required()
    def get(self):
        # Your code here
        user_id = self.current_user.id
        bookmarks = Bookmark.query.filter(Bookmark.user_id == user_id).all()
        bookmarks = [ item.to_dict() for item in bookmarks ]

        return Response(json.dumps(bookmarks), mimetype="application/json", status=200)

    @flask_jwt_extended.jwt_required()
    def post(self):
        # Your code here
        user_id = self.current_user.id
        body = request.get_json()
        post_id = body.get('post_id')
        
        # check post_id
        if post_id:
            try:
                post_id = int(post_id)
            except:
                return Response(json.dumps({'message': 'post_id must be a integer'}), mimetype="application/json", status=400)
        else:
            return Response(json.dumps({'message': 'post_id is required'}), mimetype="application/json", status=400)
        # check if user has access to post+if post id is a valid post
        try:
            if not can_view_post(post_id, self.current_user):
                return Response(json.dumps({'message': 'Post could not be found'}), mimetype="application/json", status=404)
        except:
            return Response(json.dumps({'message': 'Post with the id could not be found'}), mimetype="application/json", status=404)

        bookmark = Bookmark(user_id, post_id)

        try:
            db.session.add(bookmark)
            db.session.commit()
        except:
            return Response(json.dumps({'message': 'Duplicate post'}), mimetype="application/json", status=400)

        return Response(json.dumps(bookmark.to_dict()), mimetype="application/json", status=201)

class BookmarkDetailEndpoint(Resource):

    def __init__(self, current_user):
        self.current_user = current_user
    
    @flask_jwt_extended.jwt_required()
    def delete(self, id):
        # Your code here
        try:
            id = int(id)
        except:
            return Response(json.dumps({'message': 'post_id must be a integer'}), mimetype="application/json", status=400)

        bookmark = Bookmark.query.get(id)
        if not bookmark or bookmark.user_id != self.current_user.id:
            return Response(json.dumps({'message': 'Bookmark does not exist'}), mimetype="application/json", status=404)
       

        Bookmark.query.filter_by(id=id).delete()
        db.session.commit()
        serialized_data = {
            'message': 'Bookmark {0} successfully deleted.'.format(id)
        }
        return Response(json.dumps(serialized_data), mimetype="application/json", status=200)


def initialize_routes(api):
    api.add_resource(
        BookmarksListEndpoint, 
        '/api/bookmarks', 
        '/api/bookmarks/', 
        resource_class_kwargs={'current_user': flask_jwt_extended.current_user}
    )

    api.add_resource(
        BookmarkDetailEndpoint, 
        '/api/bookmarks/<id>', 
        '/api/bookmarks/<id>',
        resource_class_kwargs={'current_user': flask_jwt_extended.current_user}
    )
