"""
Persistence Layer - Repositories
Interface para acesso aos dados
"""

from abc import ABC, abstractmethod
from typing import List, Optional, Tuple


class BaseRepository(ABC):
    """Classe base para todos os repositórios"""
    
    @abstractmethod
    def save(self, entity):
        """Salva uma entidade"""
        pass
    
    @abstractmethod
    def find_by_id(self, entity_id):
        """Busca uma entidade por ID"""
        pass
    
    @abstractmethod
    def find_all(self):
        """Busca todas as entidades"""
        pass
    
    @abstractmethod
    def delete(self, entity_id):
        """Deleta uma entidade"""
        pass
    
    @abstractmethod
    def update(self, entity):
        """Atualiza uma entidade"""
        pass


class UsuarioRepository(BaseRepository):
    """Repositório para Usuario"""
    
    def __init__(self, db):
        self.db = db
        # Importar aqui para evitar circular imports
        from models.models import Usuario as UsuarioDB
        self.Usuario = UsuarioDB
    
    def save(self, entity):
        """Salva um novo usuário"""
        usuario = self.Usuario(
            nome=entity.nome,
            email=entity.email,
            idade=entity.idade,
            peso=entity.peso,
            altura=entity.altura
        )
        usuario.set_password(entity.senha_hash) if hasattr(entity, 'senha_hash') and entity.senha_hash else None
        self.db.session.add(usuario)
        self.db.session.commit()
        return usuario
    
    def find_by_id(self, usuario_id: int):
        """Busca usuário por ID"""
        return self.Usuario.query.get(usuario_id)
    
    def find_by_email(self, email: str):
        """Busca usuário por email"""
        return self.Usuario.query.filter_by(email=email).first()
    
    def find_all(self):
        """Busca todos os usuários"""
        return self.Usuario.query.all()
    
    def delete(self, usuario_id: int):
        """Deleta um usuário"""
        usuario = self.find_by_id(usuario_id)
        if usuario:
            self.db.session.delete(usuario)
            self.db.session.commit()
            return True
        return False
    
    def update(self, entity):
        """Atualiza um usuário"""
        usuario = self.find_by_id(entity.id)
        if usuario:
            usuario.nome = entity.nome
            usuario.idade = entity.idade
            usuario.peso = entity.peso
            usuario.altura = entity.altura
            self.db.session.commit()
            return usuario
        return None


class AtividadeRepository(BaseRepository):
    """Repositório para Atividade"""
    
    def __init__(self, db):
        self.db = db
        from models.models import Atividade as AtividadeDB
        self.Atividade = AtividadeDB
    
    def save(self, entity):
        """Salva uma nova atividade"""
        atividade = self.Atividade(
            usuario_id=entity.usuario_id,
            tipo=entity.tipo,
            duracao=entity.duracao,
            distancia=entity.distancia,
            intensidade=entity.intensidade,
            calorias_queimadas=entity.calorias_queimadas,
            data_atividade=entity.data_atividade,
            observacoes=entity.observacoes
        )
        self.db.session.add(atividade)
        self.db.session.commit()
        return atividade
    
    def find_by_id(self, atividade_id: int):
        """Busca atividade por ID"""
        return self.Atividade.query.get(atividade_id)
    
    def find_by_usuario(self, usuario_id: int, pagina: int = 1, por_pagina: int = 10) -> Tuple[List, int]:
        """Busca atividades por usuário com paginação"""
        query = self.Atividade.query.filter_by(usuario_id=usuario_id).order_by(
            self.Atividade.data_atividade.desc()
        )
        total = query.count()
        atividades = query.paginate(page=pagina, per_page=por_pagina).items
        return atividades, total
    
    def find_all(self):
        """Busca todas as atividades"""
        return self.Atividade.query.all()
    
    def delete(self, atividade_id: int):
        """Deleta uma atividade"""
        atividade = self.find_by_id(atividade_id)
        if atividade:
            self.db.session.delete(atividade)
            self.db.session.commit()
            return True
        return False
    
    def update(self, entity):
        """Atualiza uma atividade"""
        atividade = self.find_by_id(entity.id)
        if atividade:
            atividade.tipo = entity.tipo
            atividade.duracao = entity.duracao
            atividade.distancia = entity.distancia
            atividade.intensidade = entity.intensidade
            atividade.calorias_queimadas = entity.calorias_queimadas
            atividade.data_atividade = entity.data_atividade
            atividade.observacoes = entity.observacoes
            self.db.session.commit()
            return atividade
        return None
