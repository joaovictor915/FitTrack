"""
API Routes - Atividades
Refatorado para usar Service Layer
"""

from flask import Blueprint, request, jsonify, session
from repositories.base_repository import AtividadeRepository, UsuarioRepository
from services.usuario_service import AtividadeService
from models.models import db

atividades_bp = Blueprint('atividades', __name__, url_prefix='/api/atividades')


def get_atividade_service():
    """Factory para criar instância do serviço"""
    atividade_repo = AtividadeRepository(db)
    usuario_repo = UsuarioRepository(db)
    return AtividadeService(atividade_repo, usuario_repo)


def get_usuario_id():
    """Obtém o ID do usuário da sessão ou retorna erro"""
    usuario_id = session.get('usuario_id')
    if not usuario_id:
        return None
    return usuario_id


@atividades_bp.route('', methods=['GET'])
def listar():
    """Lista atividades do usuário"""
    usuario_id = get_usuario_id()
    if not usuario_id:
        return jsonify({'mensagem': 'Não autenticado'}), 401
    
    pagina = request.args.get('pagina', 1, type=int)
    por_pagina = request.args.get('por_pagina', 10, type=int)
    
    servico = get_atividade_service()
    atividades, total, mensagem, status_code = servico.listar_atividades(usuario_id, pagina, por_pagina)
    
    if status_code != 200:
        return jsonify({'mensagem': mensagem}), status_code
    
    return jsonify({
        'atividades': [a.serialize() for a in atividades],
        'total': total,
        'pagina': pagina,
        'por_pagina': por_pagina,
        'total_paginas': (total + por_pagina - 1) // por_pagina
    }), status_code


@atividades_bp.route('/<int:atividade_id>', methods=['GET'])
def obter(atividade_id):
    """Obtém uma atividade específica"""
    usuario_id = get_usuario_id()
    if not usuario_id:
        return jsonify({'mensagem': 'Não autenticado'}), 401
    
    servico = get_atividade_service()
    atividade, mensagem, status_code = servico.obter_atividade(atividade_id, usuario_id)
    
    if status_code != 200:
        return jsonify({'mensagem': mensagem}), status_code
    
    return jsonify(atividade.serialize()), status_code


@atividades_bp.route('', methods=['POST'])
def criar():
    """Cria uma nova atividade"""
    usuario_id = get_usuario_id()
    if not usuario_id:
        return jsonify({'mensagem': 'Não autenticado'}), 401
    
    dados = request.get_json()
    servico = get_atividade_service()
    
    atividade, mensagem, status_code = servico.criar_atividade(usuario_id, dados)
    
    if status_code != 201:
        return jsonify({'mensagem': mensagem}), status_code
    
    return jsonify({
        'mensagem': mensagem,
        'atividade': atividade.serialize()
    }), status_code


@atividades_bp.route('/<int:atividade_id>', methods=['PUT'])
def atualizar(atividade_id):
    """Atualiza uma atividade"""
    usuario_id = get_usuario_id()
    if not usuario_id:
        return jsonify({'mensagem': 'Não autenticado'}), 401
    
    dados = request.get_json()
    servico = get_atividade_service()
    
    atividade, mensagem, status_code = servico.atualizar_atividade(atividade_id, usuario_id, dados)
    
    if status_code != 200:
        return jsonify({'mensagem': mensagem}), status_code
    
    return jsonify({
        'mensagem': mensagem,
        'atividade': atividade.serialize()
    }), status_code


@atividades_bp.route('/<int:atividade_id>', methods=['DELETE'])
def deletar(atividade_id):
    """Deleta uma atividade"""
    usuario_id = get_usuario_id()
    if not usuario_id:
        return jsonify({'mensagem': 'Não autenticado'}), 401
    
    servico = get_atividade_service()
    sucesso, mensagem, status_code = servico.deletar_atividade(atividade_id, usuario_id)
    
    if not sucesso:
        return jsonify({'mensagem': mensagem}), status_code
    
    return jsonify({'mensagem': mensagem}), status_code


@atividades_bp.route('/resumo/stats', methods=['GET'])
def obter_estatisticas():
    """Obtém estatísticas do usuário"""
    usuario_id = get_usuario_id()
    if not usuario_id:
        return jsonify({'mensagem': 'Não autenticado'}), 401
    
    servico = get_atividade_service()
    stats = servico.obter_estatisticas(usuario_id)
    
    if not stats:
        return jsonify({'mensagem': 'Usuário não encontrado'}), 404
    
    return jsonify(stats), 200
