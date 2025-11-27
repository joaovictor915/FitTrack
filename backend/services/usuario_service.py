"""
Service Layer - Business Logic
Contém toda a lógica de negócio da aplicação
"""

import re
from typing import Dict, Tuple, List
from domain.entities import Usuario, Atividade
from repositories.base_repository import UsuarioRepository, AtividadeRepository


class UsuarioService:
    """Serviço de lógica de negócio para Usuario"""
    
    def __init__(self, repository: UsuarioRepository):
        self.repository = repository
    
    @staticmethod
    def validar_email(email: str) -> bool:
        """Valida o formato do email"""
        padrao = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
        return re.match(padrao, email) is not None
    
    @staticmethod
    def validar_senha(senha: str) -> Tuple[bool, str]:
        """Valida força da senha"""
        if len(senha) < 8:
            return False, "Senha deve ter no mínimo 8 caracteres"
        if not any(c.isupper() for c in senha):
            return False, "Senha deve conter letras maiúsculas"
        if not any(c.islower() for c in senha):
            return False, "Senha deve conter letras minúsculas"
        if not any(c.isdigit() for c in senha):
            return False, "Senha deve conter números"
        if not any(c in '!@#$%^&*()_+-=[]{}|;:,.<>?' for c in senha):
            return False, "Senha deve conter caracteres especiais"
        return True, "Válida"
    
    def registrar(self, nome: str, email: str, senha: str) -> Tuple[Usuario, str, int]:
        """Registra um novo usuário com validações"""
        # Validações
        if not nome or not email or not senha:
            return None, "Nome, email e senha são obrigatórios", 400
        
        if len(nome) > 60:
            return None, "Nome não pode ter mais de 60 caracteres", 400
        
        if len(email) > 264:
            return None, "Email não pode ter mais de 264 caracteres", 400
        
        if not self.validar_email(email):
            return None, "Email inválido", 400
        
        valido, msg = self.validar_senha(senha)
        if not valido:
            return None, msg, 400
        
        # Verifica se email já existe
        if self.repository.find_by_email(email.lower()):
            return None, "Email já cadastrado", 400
        
        # Cria novo usuário
        usuario = Usuario(nome=nome, email=email.lower())
        usuario.set_password(senha)
        
        usuario_salvo = self.repository.save(usuario)
        return usuario_salvo, "Usuário registrado com sucesso", 201
    
    def fazer_login(self, email: str, senha: str) -> Tuple[Usuario, str, int]:
        """Faz login do usuário"""
        if not email or not senha:
            return None, "Email e senha são obrigatórios", 400
        
        usuario = self.repository.find_by_email(email.lower())
        
        if not usuario or not usuario.check_password(senha):
            return None, "Email ou senha incorretos", 401
        
        return usuario, "Login realizado com sucesso", 200
    
    def obter_perfil(self, usuario_id: int) -> Tuple[Usuario, str, int]:
        """Obtém o perfil do usuário"""
        usuario = self.repository.find_by_id(usuario_id)
        
        if not usuario:
            return None, "Usuário não encontrado", 404
        
        return usuario, "Perfil obtido com sucesso", 200
    
    def atualizar_perfil(self, usuario_id: int, dados: Dict) -> Tuple[Usuario, str, int]:
        """Atualiza o perfil do usuário"""
        usuario = self.repository.find_by_id(usuario_id)
        
        if not usuario:
            return None, "Usuário não encontrado", 404
        
        usuario.nome = dados.get('nome', usuario.nome)
        usuario.idade = dados.get('idade', usuario.idade)
        usuario.peso = dados.get('peso', usuario.peso)
        usuario.altura = dados.get('altura', usuario.altura)
        
        usuario_atualizado = self.repository.update(usuario)
        return usuario_atualizado, "Perfil atualizado com sucesso", 200


class AtividadeService:
    """Serviço de lógica de negócio para Atividade"""
    
    # Tabela de calorias por minuto por tipo e intensidade
    TABELA_CALORIAS = {
        'corrida': {'baixa': 8, 'moderada': 12, 'alta': 15},
        'caminhada': {'baixa': 3.5, 'moderada': 5, 'alta': 7},
        'ciclismo': {'baixa': 6, 'moderada': 10, 'alta': 14},
        'musculacao': {'baixa': 5, 'moderada': 8, 'alta': 12},
        'natacao': {'baixa': 7, 'moderada': 10, 'alta': 14},
        'artesmarciais': {'baixa': 8, 'moderada': 12, 'alta': 16},
        'yoga': {'baixa': 2, 'moderada': 4, 'alta': 6}
    }
    
    def __init__(self, repository: AtividadeRepository, usuario_repository: UsuarioRepository):
        self.repository = repository
        self.usuario_repository = usuario_repository
    
    def calcular_calorias(self, tipo: str, duracao: int, intensidade: str, peso: float = 70) -> int:
        """Calcula calorias queimadas baseado em tipo, duração, intensidade e peso"""
        if tipo not in self.TABELA_CALORIAS or not duracao:
            return 0
        
        caloria_por_minuto = self.TABELA_CALORIAS[tipo].get(intensidade, 5)
        calorias = (caloria_por_minuto * duracao * peso) / 70
        return round(calorias)
    
    def criar_atividade(self, usuario_id: int, dados: Dict) -> Tuple[Atividade, str, int]:
        """Cria uma nova atividade"""
        # Valida se usuário existe
        usuario = self.usuario_repository.find_by_id(usuario_id)
        if not usuario:
            return None, "Usuário não encontrado", 404
        
        # Validações
        tipo = dados.get('tipo')
        if not tipo or tipo not in self.TABELA_CALORIAS:
            return None, f"Tipo de atividade inválido. Tipos válidos: {', '.join(self.TABELA_CALORIAS.keys())}", 400
        
        duracao = dados.get('duracao')
        if not duracao or duracao <= 0:
            return None, "Duração deve ser maior que 0", 400
        
        intensidade = dados.get('intensidade', 'moderada')
        if intensidade not in ['baixa', 'moderada', 'alta']:
            return None, "Intensidade inválida", 400
        
        # Calcula calorias
        calorias = self.calcular_calorias(tipo, duracao, intensidade, usuario.peso or 70)
        
        atividade = Atividade(
            usuario_id=usuario_id,
            tipo=tipo,
            duracao=duracao,
            distancia=dados.get('distancia'),
            intensidade=intensidade,
            calorias_queimadas=calorias,
            data_atividade=dados.get('data_atividade'),
            observacoes=dados.get('observacoes')
        )
        
        atividade_salva = self.repository.save(atividade)
        return atividade_salva, "Atividade criada com sucesso", 201
    
    def obter_atividade(self, atividade_id: int, usuario_id: int) -> Tuple[Atividade, str, int]:
        """Obtém uma atividade específica"""
        atividade = self.repository.find_by_id(atividade_id)
        
        if not atividade or atividade.usuario_id != usuario_id:
            return None, "Atividade não encontrada", 404
        
        return atividade, "Atividade obtida com sucesso", 200
    
    def listar_atividades(self, usuario_id: int, pagina: int = 1, por_pagina: int = 10) -> Tuple[List, int, str, int]:
        """Lista atividades do usuário com paginação"""
        # Valida se usuário existe
        usuario = self.usuario_repository.find_by_id(usuario_id)
        if not usuario:
            return None, 0, "Usuário não encontrado", 404
        
        atividades, total = self.repository.find_by_usuario(usuario_id, pagina, por_pagina)
        return atividades, total, "Atividades listadas com sucesso", 200
    
    def atualizar_atividade(self, atividade_id: int, usuario_id: int, dados: Dict) -> Tuple[Atividade, str, int]:
        """Atualiza uma atividade"""
        atividade = self.repository.find_by_id(atividade_id)
        
        if not atividade or atividade.usuario_id != usuario_id:
            return None, "Atividade não encontrado", 404
        
        atividade.tipo = dados.get('tipo', atividade.tipo)
        atividade.duracao = dados.get('duracao', atividade.duracao)
        atividade.distancia = dados.get('distancia', atividade.distancia)
        atividade.intensidade = dados.get('intensidade', atividade.intensidade)
        atividade.observacoes = dados.get('observacoes', atividade.observacoes)
        
        # Recalcula calorias se necessário
        usuario = self.usuario_repository.find_by_id(usuario_id)
        if usuario:
            atividade.calorias_queimadas = self.calcular_calorias(
                atividade.tipo, atividade.duracao, atividade.intensidade, usuario.peso or 70
            )
        
        atividade_atualizada = self.repository.update(atividade)
        return atividade_atualizada, "Atividade atualizada com sucesso", 200
    
    def deletar_atividade(self, atividade_id: int, usuario_id: int) -> Tuple[bool, str, int]:
        """Deleta uma atividade"""
        atividade = self.repository.find_by_id(atividade_id)
        
        if not atividade or atividade.usuario_id != usuario_id:
            return False, "Atividade não encontrada", 404
        
        self.repository.delete(atividade_id)
        return True, "Atividade deletada com sucesso", 200
    
    def obter_estatisticas(self, usuario_id: int) -> Dict:
        """Obtém estatísticas do usuário"""
        usuario = self.usuario_repository.find_by_id(usuario_id)
        if not usuario:
            return {}
        
        atividades, _ = self.repository.find_by_usuario(usuario_id, pagina=1, por_pagina=1000)
        
        if not atividades:
            return {
                'total_atividades': 0,
                'total_duracao_minutos': 0,
                'total_calorias': 0,
                'media_calorias': 0
            }
        
        total_duracao = sum(a.duracao or 0 for a in atividades)
        total_calorias = sum(a.calorias_queimadas or 0 for a in atividades)
        
        return {
            'total_atividades': len(atividades),
            'total_duracao_minutos': total_duracao,
            'total_calorias': total_calorias,
            'media_calorias': total_calorias // len(atividades) if atividades else 0
        }
