from flask import Blueprint, request, jsonify, session
from models.models import Usuario, db
from datetime import datetime
import re

auth_bp = Blueprint('auth', __name__, url_prefix='/api/auth')

def validar_email(email):
    """Valida o formato do email"""
    padrao = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    return re.match(padrao, email) is not None

def validar_senha(senha):
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

@auth_bp.route('/registrar', methods=['POST'])
def registrar():
    """Registra um novo usuário"""
    dados = request.get_json()
    
    # Validações
    if not dados or not dados.get('nome') or not dados.get('email') or not dados.get('senha'):
        return jsonify({'mensagem': 'Nome, email e senha são obrigatórios'}), 400
    
    nome = dados.get('nome').strip()
    email = dados.get('email').strip().lower()
    senha = dados.get('senha')
    
    if len(nome) > 60:
        return jsonify({'mensagem': 'Nome não pode ter mais de 60 caracteres'}), 400
    
    if len(email) > 264:
        return jsonify({'mensagem': 'Email não pode ter mais de 264 caracteres'}), 400
    
    if not validar_email(email):
        return jsonify({'mensagem': 'Email inválido'}), 400
    
    valido, msg = validar_senha(senha)
    if not valido:
        return jsonify({'mensagem': msg}), 400
    
    # Verifica se email já existe
    if Usuario.query.filter_by(email=email).first():
        return jsonify({'mensagem': 'Email já cadastrado'}), 400
    
    try:
        novo_usuario = Usuario(nome=nome, email=email)
        novo_usuario.set_password(senha)
        
        db.session.add(novo_usuario)
        db.session.commit()
        
        # Faz login automático
        session['usuario_id'] = novo_usuario.id
        
        return jsonify({
            'mensagem': 'Usuário registrado com sucesso!',
            'usuario': novo_usuario.serialize_sem_sensivel()
        }), 201
    except Exception as e:
        db.session.rollback()
        return jsonify({'mensagem': f'Erro ao registrar: {str(e)}'}), 500

@auth_bp.route('/login', methods=['POST'])
def login():
    """Faz login do usuário"""
    dados = request.get_json()
    
    if not dados or not dados.get('email') or not dados.get('senha'):
        return jsonify({'mensagem': 'Email e senha são obrigatórios'}), 400
    
    email = dados.get('email').strip().lower()
    senha = dados.get('senha')
    
    usuario = Usuario.query.filter_by(email=email).first()
    
    if not usuario or not usuario.check_password(senha):
        return jsonify({'mensagem': 'Email ou senha incorretos'}), 401
    
    # Armazena na sessão
    session['usuario_id'] = usuario.id
    
    return jsonify({
        'mensagem': 'Login realizado com sucesso!',
        'usuario': usuario.serialize_sem_sensivel()
    }), 200

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
    
    usuario = Usuario.query.get(usuario_id)
    
    if not usuario:
        session.pop('usuario_id', None)
        return jsonify({'mensagem': 'Usuário não encontrado'}), 404
    
    return jsonify(usuario.serialize_sem_sensivel()), 200

@auth_bp.route('/atualizar-perfil', methods=['PUT'])
def atualizar_perfil():
    """Atualiza o perfil do usuário logado"""
    usuario_id = session.get('usuario_id')
    
    if not usuario_id:
        return jsonify({'mensagem': 'Não autenticado'}), 401
    
    usuario = Usuario.query.get(usuario_id)
    
    if not usuario:
        session.pop('usuario_id', None)
        return jsonify({'mensagem': 'Usuário não encontrado'}), 404
    
    dados = request.get_json()
    
    if not dados:
        return jsonify({'mensagem': 'Dados inválidos'}), 400
    
    try:
        if 'nome' in dados:
            nome = dados['nome'].strip()
            if len(nome) > 60:
                return jsonify({'mensagem': 'Nome não pode ter mais de 60 caracteres'}), 400
            usuario.nome = nome
        
        if 'idade' in dados:
            usuario.idade = int(dados['idade']) if dados['idade'] else None
        
        if 'peso' in dados:
            usuario.peso = float(dados['peso']) if dados['peso'] else None
        
        if 'altura' in dados:
            usuario.altura = int(dados['altura']) if dados['altura'] else None
        
        db.session.commit()
        
        return jsonify({
            'mensagem': 'Perfil atualizado com sucesso!',
            'usuario': usuario.serialize_sem_sensivel()
        }), 200
    except Exception as e:
        db.session.rollback()
        return jsonify({'mensagem': f'Erro ao atualizar perfil: {str(e)}'}), 500
