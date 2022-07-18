from flask import Flask

def create_app(test_config=None):
    #setting up app configuration
    app = Flask(__name__, static_url_path='/')
    app.url_map.strict_slashes = False
    app.config.from_mapping(
        SECRET_KEY='super_secret_key'
    )
    
    # similar to "app.get('/hello', (req, res) =>... in nodejs"
    @app.route('/hello')
    def hello():
        return 'hello world'
    
    return app