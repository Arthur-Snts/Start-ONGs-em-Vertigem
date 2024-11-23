from database import db
from sqlalchemy.orm import mapped_column, Mapped
from sqlalchemy import Integer, String
from flask_login import UserMixin

class User(db.Model, UserMixin):
    __tablename__ = 'tb_usuario'

    # Mapeando os atributos para os nomes de colunas na tabela
    id: Mapped[int] = mapped_column('usu_id', Integer, primary_key=True)
    nome: Mapped[str] = mapped_column('usu_nome', String(50), nullable=False)
    email: Mapped[str] = mapped_column('usu_email', String(120), unique=True, nullable=False)
    senha: Mapped[str] = mapped_column('usu_senha', String(100), nullable=False)

    def __init__(self, nome, email, senha):
        self.nome = nome
        self.email = email
        self.senha = senha

    @staticmethod
    def get_by_email(email):
        print(f"Buscando usuário com email: {email}")
        return db.session.query(User).filter_by(email=email).first()

    @staticmethod
    def create(nome, email, senha):
        new_user = User(nome=nome, email=email, senha=senha)
        db.session.add(new_user)
        db.session.commit()
