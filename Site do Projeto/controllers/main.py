from flask import Blueprint, render_template, redirect, url_for, request, flash
from flask_login import login_user, login_required, logout_user, current_user
from werkzeug.security import generate_password_hash, check_password_hash
from models.user import User
from database import db

main_bp = Blueprint('main', __name__)

@main_bp.route('/')
def index():
    return render_template('index.html')

@main_bp.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form['email']
        senha = request.form['senha']
        user = User.get_by_email(email)

        if user and check_password_hash(user.senha, senha):
            login_user(user)
            return redirect(url_for('main.infoprojeto'))
        flash('Email ou senha incorretos!', 'danger')

    return render_template('login.html')

@main_bp.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        nome = request.form['nome']
        email = request.form['email']
        senha = request.form['senha']
        senha_conf = request.form['senha_conf']

        if senha != senha_conf:
            flash('Os campos de senha não coincidem!', 'danger')
            return redirect(url_for('main.register'))

        existing_user = User.get_by_email(email)
        if existing_user:
            flash('Esse email já está cadastrado!', 'danger')
            return redirect(url_for('main.register'))

        senha_hashed = generate_password_hash(senha)
        User.create(nome, email, senha_hashed)

        flash('Usuário registrado com sucesso!', 'success')
        return redirect(url_for('main.login'))

    return render_template('register.html')

@main_bp.route('/info')
@login_required
def infoprojeto():
    return render_template('info_projeto.html')

@main_bp.route('/infogame')
@login_required
def infogame():
    return render_template('info_jogo.html')

@main_bp.route('/download')
@login_required
def download():
    return render_template('download.html')

@main_bp.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('main.index'))
