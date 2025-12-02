# from flask import Blueprint, request, jsonify, session
# from repositories.base_repository import MetaRepository, UsuarioRepository
# from services.services import MetaService
# from utils.auth_utils import login_required

# metas_bp = Blueprint('metas', __name__, url_prefix='/api/metas')

# meta_repo = MetaRepository()
# usuario_repo = UsuarioRepository()
# meta_service = MetaService(meta_repo, usuario_repo)

# @metas_bp.route('', methods=['POST'])
# @login_required
# def criar_meta():
#     """Cria uma nova meta para o usuário logado"""
#     dados = request.get_json()
#     usuario_id = session.get('usuario_id')
    
#     meta, mensagem, status = meta_service.criar_meta(usuario_id, dados)
    
#     if status != 201:
#         return jsonify({'mensagem': mensagem}), status
    
#     return jsonify(meta.serialize()), 201

# @metas_bp.route('', methods=['GET'])
# @login_required
# def listar_metas():
#     """Lista todas as metas do usuário logado"""
#     usuario_id = session.get('usuario_id')
    
#     metas, mensagem, status = meta_service.listar_metas(usuario_id)
    
#     if status != 200:
#         return jsonify({'mensagem': mensagem}), status
        
#     metas_serializadas = [meta.serialize() for meta in metas]
#     return jsonify(metas_serializadas), 200

# # Adicionar rotas para obter, atualizar e deletar metas (semelhante às atividades)

# @metas_bp.route('/<int:meta_id>', methods=['DELETE'])
# @login_required
# def deletar_meta(meta_id):
#     """Deleta uma meta específica do usuário logado"""
#     usuario_id = session.get('usuario_id')
    
#     deletado, mensagem, status = meta_service.deletar_meta(meta_id, usuario_id)
    
#     if status != 200:
#         return jsonify({'mensagem': mensagem}), status
        
#     return jsonify({'mensagem': mensagem}), 200