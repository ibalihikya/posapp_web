import os

from flask import Flask

def create_app(test_config=None):
    # create and configure the app
    app = Flask(__name__, instance_relative_config=True)
    app.config.from_mapping(
        SECRET_KEY='dev',
        DATABASE_URL = os.environ['DATABASE_URL'],
     )

    @app.route('/hello')
    def hello():
        return 'Hello, World!' 
  		
    from posapp import db
    db.init_app(app)

      
    """from posapp import stock
    app.register_blueprint(stock.bp)
    app.add_url_rule('/', endpoint='index')"""

    return app