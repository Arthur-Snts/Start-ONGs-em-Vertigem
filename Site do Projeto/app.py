from flask import Flask
from flask_login import LoginManager
from controllers.main import main_bp
from database import init_db
from models.user import User

app = Flask(__name__)

login_manager = LoginManager()
login_manager.init_app(app)

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

init_db(app)

app.register_blueprint(main_bp)

if __name__ == "__main__":
    app.run(debug=True)


