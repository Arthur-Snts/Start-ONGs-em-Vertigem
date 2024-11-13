from flask import Flask, render_template, redirect, url_for, request, flash
from flask_login import LoginManager, login_user, login_required, logout_user, current_user
from werkzeug.security import generate_password_hash, check_password_hash
from models import User, obter_conexao

app = Flask(__name__)
app.config['SECRET_KEY'] = 'SUPERSECRETO'

login_manager = LoginManager()
login_manager.init_app(app)

@login_manager.user_loader
def load_user(user_id):
    return User.get(user_id)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form['email']
        senha = request.form['senha']
        user = User.get_by_email(email)

        if user and check_password_hash(user.senha, senha):
            login_user(user)
            return redirect(url_for('infoprojeto'))
        flash('Email ou senha incorretos!', 'danger')
    
    return render_template('login.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        nome = request.form['nome']
        email = request.form['email']
        senha = request.form['senha']
        senha_conf = request.form['senha_conf']

        conn = obter_conexao()
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM tb_usuario WHERE usu_email = %s", (email,))
        existing_user = cursor.fetchone()
        cursor.close()
        conn.close()

        if senha != senha_conf:
            flash('Os campos de senha não coincidem!', 'error')
            return redirect(url_for('register'))

        if existing_user:
            flash('Esse email já está cadastrado!', 'error')
            return redirect(url_for('register'))

        senha_hashed = generate_password_hash(senha)
        
        conn = obter_conexao()
        cursor = conn.cursor()
        cursor.execute("INSERT INTO tb_usuario (usu_email, usu_senha, usu_nome) VALUES (%s, %s, %s)",
                       (email, senha_hashed, nome))
        conn.commit()
        cursor.close()
        conn.close()

        flash('Usuário registrado com sucesso!', 'success')
        flash('Por favor, entre com sua conta.', 'success')
        return redirect(url_for('login'))

    return render_template('register.html')

@app.route('/info')
@login_required
def infoprojeto():
    return render_template('info_projeto.html')

@app.route('/infogame')
@login_required
def infogame():
    return render_template('info_jogo.html')

@app.route('/download')
@login_required
def download():
    return render_template('download.html')

@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('index'))
