from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime

db = SQLAlchemy()

class Usuario(db.Model):
    """Modelo de Usuário do FitTrack"""
    __tablename__ = 'usuarios'
    
    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(60), nullable=False)
    email = db.Column(db.String(264), unique=True, nullable=False)
    senha_hash = db.Column(db.String(255), nullable=False)
    idade = db.Column(db.Integer)
    peso = db.Column(db.Float)
    altura = db.Column(db.Integer)  # em cm
    data_criacao = db.Column(db.DateTime, default=datetime.utcnow)
    
    # Relacionamento
    atividades = db.relationship('Atividade', backref='usuario', lazy=True, cascade='all, delete-orphan')
    
    def set_password(self, senha):
        """Hash da senha"""
        self.senha_hash = generate_password_hash(senha)
    
    def check_password(self, senha):
        """Verifica se a senha está correta"""
        return check_password_hash(self.senha_hash, senha)
    
    def serialize(self):
        """Serializa o usuário para JSON"""
        return {
            'id': self.id,
            'nome': self.nome,
            'email': self.email,
            'idade': self.idade,
            'peso': self.peso,
            'altura': self.altura,
            'data_criacao': self.data_criacao.isoformat() if self.data_criacao else None
        }
    
    def serialize_sem_sensivel(self):
        """Serializa o usuário sem dados sensíveis"""
        return {
            'id': self.id,
            'nome': self.nome,
            'email': self.email,
            'idade': self.idade,
            'peso': self.peso,
            'altura': self.altura
        }
    
    def __repr__(self):
        return f'<Usuario {self.nome}>'


class Atividade(db.Model):
    """Modelo de Atividade do FitTrack"""
    __tablename__ = 'atividades'
    
    id = db.Column(db.Integer, primary_key=True)
    usuario_id = db.Column(db.Integer, db.ForeignKey('usuarios.id'), nullable=False)
    tipo = db.Column(db.String(50), nullable=False)  # corrida, caminhada, musculacao, etc
    duracao = db.Column(db.Integer)  # em minutos
    distancia = db.Column(db.Float)  # em km
    intensidade = db.Column(db.String(20))  # baixa, moderada, alta
    calorias_queimadas = db.Column(db.Float)
    data_atividade = db.Column(db.DateTime, nullable=False)
    data_criacao = db.Column(db.DateTime, default=datetime.utcnow)
    observacoes = db.Column(db.Text)
    
    def serialize(self):
        """Serializa a atividade para JSON"""
        return {
            'id': self.id,
            'usuario_id': self.usuario_id,
            'tipo': self.tipo,
            'duracao': self.duracao,
            'distancia': self.distancia,
            'intensidade': self.intensidade,
            'calorias_queimadas': self.calorias_queimadas,
            'data_atividade': self.data_atividade.isoformat() if self.data_atividade else None,
            'data_criacao': self.data_criacao.isoformat() if self.data_criacao else None,
            'observacoes': self.observacoes
        }
    
    def __repr__(self):
        return f'<Atividade {self.tipo} de {self.usuario_id}>'
