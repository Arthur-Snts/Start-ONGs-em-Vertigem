from flask_sqlalchemy import SQLAlchemy
import mysql.connector

db = SQLAlchemy()

def init_db(app):
    

    app.config.from_object('database.config.Config')
    db.init_app(app)

    connection = mysql.connector.connect(
        host='localhost',
        user='root',
        password=''
    )
    cursor = connection.cursor()
    cursor.execute(f"CREATE DATABASE IF NOT EXISTS {'databasepi'}")
    cursor.close()
    connection.close()

    with app.app_context():
        db.create_all()

    
