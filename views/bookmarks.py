from flask import Response, request
from flask_restful import Resource
from models import Bookmark, db
import json
from . import can_view_post

class BookmarksListEndpoint(Resource):

    def __init__(self, current_user):
        self.current_user = current_user
    
    def get(self):
        # Your code here
        user_id = self.current_user.id
        bookmarks = Bookmark.query.filter(Bookmark.user_id == user_id).all()
        bookmarks = [ item.to_dict() for item in bookmarks ]

        return Response(json.dumps(bookmarks), mimetype="application/json", status=200)

    def post(self):
        # Your code here
        user_id = self.current_user.id
        body = request.get_json()
        post_id = body.get('post_id')

        bookmark = Bookmark(user_id, post_id)
        db.session.add(bookmark)
        db.session.commit()
        return Response(json.dumps(bookmark.to_dict()), mimetype="application/json", status=201)

class BookmarkDetailEndpoint(Resource):

    def __init__(self, current_user):
        self.current_user = current_user
    
    def delete(self, id):
        # Your code here
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
        resource_class_kwargs={'current_user': api.app.current_user}
    )

    api.add_resource(
        BookmarkDetailEndpoint, 
        '/api/bookmarks/<id>', 
        '/api/bookmarks/<id>',
        resource_class_kwargs={'current_user': api.app.current_user}
    )
