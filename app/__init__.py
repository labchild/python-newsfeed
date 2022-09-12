from flask import Flask
from app.routes import home, dashboard, api
from app.db import init_db
from app.utils import filters

def create_app(test_config=None):
    # set up app config
    app = Flask(__name__, static_url_path='/')
    app.url_map.strict_slashes = False
    app.config.from_mapping(
        SECRET_KEY='super_secret_key'
    )

    @app.route('/hello')
    def hello():
        return 'hello world'

    # register blueprint/connect routes
    app.register_blueprint(home)
    app.register_blueprint(dashboard)
    app.register_blueprint(api)

    # open database connection
    init_db(app)

    # resgister filters for Jinja
    app.jinja_env.filters['format_url'] = filters.format_url
    app.jinja_env.filters['format_plural'] = filters.format_plural
    app.jinja_env.filters['format_date'] = filters.format_date
    
    return app