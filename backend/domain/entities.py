"""
Domain Layer - Entities (Domain Objects)
Define as entidades do negócio de forma independente do framework
"""

from datetime import datetime, timezone
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
        self.data_criacao = data_criacao or datetime.now(timezone.utc)
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
        self.data_atividade = data_atividade or datetime.now(timezone.utc)
        self.observacoes = observacoes
        self.data_criacao = data_criacao or datetime.now(timezone.utc)
    
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
    
# class Meta:
#     """Entidade de Meta de Fitness do domínio"""

# def __init__(self, id=None, usuario_id=None, titulo=None, tipo=None, 
#                 valor_alvo=None, progresso_atual=0.0, data_alvo=None, 
#                 data_criacao=None, data_conclusao=None):
    
#     self.id = id
#     self.usuario_id = usuario_id
#     self.titulo = titulo
#     self.tipo = tipo
#     self.valor_alvo = valor_alvo
#     self.progresso_atual = progresso_atual
    
#     # data_alvo será do tipo date (se for um objeto datetime, converte para date)
#     if isinstance(data_alvo, datetime):
#         self.data_alvo = data_alvo.date()
#     else:
#         self.data_alvo = data_alvo
        
#     self.data_criacao = data_criacao or datetime.now(timezone.utc)
#     self.data_conclusao = data_conclusao
    
    
# def to_dict(self):
#     """Converte para dicionário"""
#     # Determina o status
#     status = 'Concluída' if self.progresso_atual >= self.valor_alvo else 'Em Progresso'
    
#     return {
#         'id': self.id,
#         'usuario_id': self.usuario_id,
#         'titulo': self.titulo,
#         'tipo': self.tipo,
#         'valor_alvo': self.valor_alvo,
#         'progresso_atual': self.progresso_atual,
#         'data_alvo': self.data_alvo.isoformat() if self.data_alvo else None,
#         'data_criacao': self.data_criacao.isoformat() if self.data_criacao else None,
#         'data_conclusao': self.data_conclusao.isoformat() if self.data_conclusao else None,
#         'status': status
#     }
