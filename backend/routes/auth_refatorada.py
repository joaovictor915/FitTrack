"""
API Routes - Autenticação
Refatorado para usar Service Layer
"""

from flask import Blueprint, request, jsonify, session
from repositories.base_repository import UsuarioRepository
from services.usuario_service import UsuarioService
from models.models import db

auth_bp = Blueprint('auth', __name__, url_prefix='/api/auth')


def get_usuario_service():
    """Factory para criar instância do serviço"""
    repo = UsuarioRepository(db)
    return UsuarioService(repo)


@auth_bp.route('/registrar', methods=['POST'])
def registrar():
    """Registra um novo usuário"""
    dados = request.get_json()
    servico = get_usuario_service()
    
    usuario, mensagem, status_code = servico.registrar(
        dados.get('nome'),
        dados.get('email'),
        dados.get('senha')
    )
    
    if status_code != 201:
        return jsonify({'mensagem': mensagem}), status_code
    
    # Faz login automático
    session['usuario_id'] = usuario.id
    
    return jsonify({
        'mensagem': mensagem,
        'usuario': usuario.serialize_sem_sensivel()
    }), status_code


@auth_bp.route('/login', methods=['POST'])
def login():
    """Faz login do usuário"""
    dados = request.get_json()
    servico = get_usuario_service()
    
    usuario, mensagem, status_code = servico.fazer_login(
        dados.get('email'),
        dados.get('senha')
    )
    
    if status_code != 200:
        return jsonify({'mensagem': mensagem}), status_code
    
    # Armazena na sessão
    session['usuario_id'] = usuario.id
    
    return jsonify({
        'mensagem': mensagem,
        'usuario': usuario.serialize_sem_sensivel()
    }), status_code


@auth_bp.route('/logout', methods=['POST'])
def logout():
    """Faz logout do usuário"""
    session.pop('usuario_id', None)
    return jsonify({'mensagem': 'Logout realizado com sucesso!'}), 200


@auth_bp.route('/usuario-atual', methods=['GET'])
def usuario_atual():
    """Obtém os dados do usuário logado"""
    usuario_id = session.get('usuario_id')
    
    if not usuario_id:
        return jsonify({'mensagem': 'Não autenticado'}), 401
    
    servico = get_usuario_service()
    usuario, mensagem, status_code = servico.obter_perfil(usuario_id)
    
    if status_code != 200:
        return jsonify({'mensagem': mensagem}), status_code
    
    return jsonify(usuario.serialize_sem_sensivel()), 200


@auth_bp.route('/atualizar-perfil', methods=['PUT'])
def atualizar_perfil():
    """Atualiza o perfil do usuário"""
    usuario_id = session.get('usuario_id')
    
    if not usuario_id:
        return jsonify({'mensagem': 'Não autenticado'}), 401
    
    dados = request.get_json()
    servico = get_usuario_service()
    
    usuario, mensagem, status_code = servico.atualizar_perfil(usuario_id, dados)
    
    if status_code != 200:
        return jsonify({'mensagem': mensagem}), status_code
    
    return jsonify({
        'mensagem': mensagem,
        'usuario': usuario.serialize_sem_sensivel()
    }), status_code
