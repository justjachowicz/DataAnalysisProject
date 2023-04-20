from flask import Flask, render_template


def create_app(test_config=None):
    # create and configure the app
    app = Flask(__name__, instance_relative_config=True)
    app.config.from_mapping(
        SECRET_KEY='secretkey'
    )

    @app.route('/')
    def hello():
        return render_template('index.html')

    return app
