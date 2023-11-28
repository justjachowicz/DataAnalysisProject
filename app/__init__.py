from flask import Flask, render_template


def create_app():
    """
    create and configure the app, register blueprints
    :return: flask application
    """
    app = Flask(__name__, instance_relative_config=True)
    app.config['SECRET_KEY'] = 'anksdjfhb4iubkfgv8s3n.d1'


    @app.route('/')
    def hello():
        """
        check configuration settings and reset database if needed
        :return: index page
        """

        return render_template('index.html', title='Home')

    return app
