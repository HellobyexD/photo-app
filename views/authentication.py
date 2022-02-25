from flask import (
    request, make_response, render_template, redirect
)
from models import User
import flask_jwt_extended

def logout():
    # hint:  https://dev.to/totally_chase/python-using-jwt-in-cookies-with-a-flask-app-and-restful-api-2p75
    resp = make_response(redirect('/login', code=302))
    flask_jwt_extended.unset_access_cookies(resp)
    return resp
    

def login():
    if request.method == 'POST':
        # authenticate user here. If the user sent valid credentials, set the
        # JWT cookies:
        # https://flask-jwt-extended.readthedocs.io/en/3.0.0_release/tokens_in_cookies/
        print(request.form)
        username = request.form.get('username')
        password = request.form.get('password')
        user = User.query.filter_by(username=username).first()
        if user is None:
            return render_template(
                'login.html',
                message='Invalid username'
            )
            print(user.to_dict())
            print(user, username)
        
        if user.check_password(password):
            access_token = flask_jwt_extended.create_access_token(identity=user.id)
            resp = make_response(redirect('/', 302))
            flask_jwt_extended.set_access_cookies(resp, access_token)
            return resp
        else:
            return render_template(
                'login.html',
                message='Invalid password'
            )

    else:
        return render_template(
            'login.html'
        )

def initialize_routes(app):
    app.add_url_rule('/login', 
        view_func=login, methods=['GET', 'POST'])
    app.add_url_rule('/logout', view_func=logout)