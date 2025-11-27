"""
Domain Layer - Entities (Domain Objects)
Define as entidades do negócio de forma independente do framework
"""

from datetime import datetime
from werkzeug.security import generate_password_hash, check_password_hash


class Usuario:
    """Entidade de Usuário do domínio"""
    
    def __init__(self, id=None, nome=None, email=None, idade=None, peso=None, altura=None, data_criacao=None):
        self.id = id
        self.nome = nome
        self.email = email
        self.idade = idade
        self.peso = peso
        self.altura = altura
        self.data_criacao = data_criacao or datetime.utcnow()
        self.senha_hash = None
    
    def set_password(self, senha):
        """Define a senha com hash"""
        self.senha_hash = generate_password_hash(senha)
    
    def check_password(self, senha):
        """Verifica se a senha está correta"""
        return check_password_hash(self.senha_hash, senha)
    
    def to_dict(self):
        """Converte para dicionário"""
        return {
            'id': self.id,
            'nome': self.nome,
            'email': self.email,
            'idade': self.idade,
            'peso': self.peso,
            'altura': self.altura,
            'data_criacao': self.data_criacao.isoformat() if self.data_criacao else None
        }


class Atividade:
    """Entidade de Atividade do domínio"""
    
    def __init__(self, id=None, usuario_id=None, tipo=None, duracao=None, distancia=None, 
                 intensidade=None, calorias_queimadas=None, data_atividade=None, 
                 observacoes=None, data_criacao=None):
        self.id = id
        self.usuario_id = usuario_id
        self.tipo = tipo
        self.duracao = duracao
        self.distancia = distancia
        self.intensidade = intensidade
        self.calorias_queimadas = calorias_queimadas
        self.data_atividade = data_atividade or datetime.utcnow()
        self.observacoes = observacoes
        self.data_criacao = data_criacao or datetime.utcnow()
    
    def to_dict(self):
        """Converte para dicionário"""
        return {
            'id': self.id,
            'usuario_id': self.usuario_id,
            'tipo': self.tipo,
            'duracao': self.duracao,
            'distancia': self.distancia,
            'intensidade': self.intensidade,
            'calorias_queimadas': self.calorias_queimadas,
            'data_atividade': self.data_atividade.isoformat() if self.data_atividade else None,
            'observacoes': self.observacoes,
            'data_criacao': self.data_criacao.isoformat() if self.data_criacao else None
        }
