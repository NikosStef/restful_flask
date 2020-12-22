from flask import Flask
from flask_jwt import JWT
from auth.auth import authenticate, identity
import config


def create_app(config_class=config.Config):

    app = Flask(__name__)
    app.config.from_object(config_class)
    jwt = JWT(app, authenticate, identity)

    from api import api_bp
    app.register_blueprint(api_bp, url_prefix='/api')
    '''
    from auth import auth as auth_bp
    app.register_blueprint(auth_bp, url_prefix='/auth')
    '''

    return app

def main():

    app = create_app()

    app.app_context().push()
    app.run(debug=True)


if __name__ == '__main__':
    main()
