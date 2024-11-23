from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

def init_db(app):
    app.config.from_object('database.config.Config')
    db.init_app(app)
