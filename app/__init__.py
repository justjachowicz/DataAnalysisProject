from flask import Flask, render_template


def create_app():
    """
    create and configure the app, register blueprints
    :return: flask application
    """
    app = Flask(__name__, instance_relative_config=True)
    app.config['SECRET_KEY'] = 'anksdjfhb4iubkfgv8s3n.d1'

    from app import db
    db.init_app(app)

    from app.config.configGetter import get_db_state
    reset_db_state = get_db_state()

    from .views import views
    app.register_blueprint(views, url_prefix='/views')

    from .data import data
    app.register_blueprint(data, url_prefix='/data')

    @app.route('/')
    def hello():
        """
        check configuration settings and reset database if needed
        :return: index page
        """
        if reset_db_state == 'True':
            conn = db.get_db()
            db.init_db()
            db.fill_db(conn)

        return render_template('index.html', title='Home')

    return app
