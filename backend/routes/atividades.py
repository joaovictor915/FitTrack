from flask import Blueprint, request, jsonify, session
from models.models import Atividade, Usuario, db
from datetime import datetime

atividades_bp = Blueprint('atividades', __name__, url_prefix='/api/atividades')

def calcular_calorias(tipo, duracao, intensidade, peso=70):
    """Calcula calorias aproximadas queimadas na atividade"""
    # Tabela de calorias por minuto baseada em tipo e intensidade
    calorias_por_minuto = {
        'corrida': {'baixa': 8, 'moderada': 12, 'alta': 15},
        'caminhada': {'baixa': 3.5, 'moderada': 5, 'alta': 7},
        'ciclismo': {'baixa': 6, 'moderada': 10, 'alta': 14},
        'musculacao': {'baixa': 5, 'moderada': 8, 'alta': 12},
        'natacao': {'baixa': 7, 'moderada': 10, 'alta': 14},
        'artesmarciais': {'baixa': 8, 'moderada': 12, 'alta': 16},
        'yoga': {'baixa': 2, 'moderada': 4, 'alta': 6}
    }
    
    if tipo not in calorias_por_minuto:
        return None
    
    intensidade = intensidade or 'moderada'
    if intensidade not in calorias_por_minuto[tipo]:
        intensidade = 'moderada'
    
    calorias = calorias_por_minuto[tipo][intensidade] * duracao
    # Ajusta pelo peso (pessoas mais pesadas queimam mais calorias)
    calorias = calorias * (peso / 70)
    
    return round(calorias, 2)

@atividades_bp.route('', methods=['GET'])
def listar_atividades():
    """Lista todas as atividades do usuário logado"""
    usuario_id = session.get('usuario_id')
    
    if not usuario_id:
        return jsonify({'mensagem': 'Não autenticado'}), 401
    
    usuario = Usuario.query.get(usuario_id)
    if not usuario:
        return jsonify({'mensagem': 'Usuário não encontrado'}), 404
    
    # Parâmetros opcionais para filtro
    tipo = request.args.get('tipo')
    pagina = request.args.get('pagina', 1, type=int)
    por_pagina = request.args.get('por_pagina', 10, type=int)
    
    query = Atividade.query.filter_by(usuario_id=usuario_id)
    
    if tipo:
        query = query.filter_by(tipo=tipo)
    
    # Ordena por data descendente
    query = query.order_by(Atividade.data_atividade.desc())
    
    atividades = query.paginate(page=pagina, per_page=por_pagina)
    
    return jsonify({
        'atividades': [atividade.serialize() for atividade in atividades.items],
        'total': atividades.total,
        'pagina': pagina,
        'por_pagina': por_pagina,
        'total_paginas': atividades.pages
    }), 200

@atividades_bp.route('/<int:atividade_id>', methods=['GET'])
def obter_atividade(atividade_id):
    """Obtém uma atividade específica"""
    usuario_id = session.get('usuario_id')
    
    if not usuario_id:
        return jsonify({'mensagem': 'Não autenticado'}), 401
    
    atividade = Atividade.query.get(atividade_id)
    
    if not atividade:
        return jsonify({'mensagem': 'Atividade não encontrada'}), 404
    
    # Verifica se a atividade pertence ao usuário
    if atividade.usuario_id != usuario_id:
        return jsonify({'mensagem': 'Acesso negado'}), 403
    
    return jsonify(atividade.serialize()), 200

@atividades_bp.route('', methods=['POST'])
def criar_atividade():
    """Cria uma nova atividade"""
    usuario_id = session.get('usuario_id')
    
    if not usuario_id:
        return jsonify({'mensagem': 'Não autenticado'}), 401
    
    usuario = Usuario.query.get(usuario_id)
    if not usuario:
        return jsonify({'mensagem': 'Usuário não encontrado'}), 404
    
    dados = request.get_json()
    
    if not dados or not dados.get('tipo') or not dados.get('data_atividade'):
        return jsonify({'mensagem': 'Tipo e data da atividade são obrigatórios'}), 400
    
    try:
        # Parse da data
        data_atividade = datetime.fromisoformat(dados['data_atividade'].replace('Z', '+00:00'))
        
        duracao = int(dados.get('duracao', 0)) if dados.get('duracao') else None
        distancia = float(dados.get('distancia', 0)) if dados.get('distancia') else None
        intensidade = dados.get('intensidade', 'moderada')
        
        # Calcula calorias
        calorias = None
        if duracao:
            calorias = calcular_calorias(
                dados['tipo'], 
                duracao, 
                intensidade, 
                usuario.peso or 70
            )
        
        nova_atividade = Atividade(
            usuario_id=usuario_id,
            tipo=dados['tipo'],
            duracao=duracao,
            distancia=distancia,
            intensidade=intensidade,
            calorias_queimadas=calorias,
            data_atividade=data_atividade,
            observacoes=dados.get('observacoes')
        )
        
        db.session.add(nova_atividade)
        db.session.commit()
        
        return jsonify({
            'mensagem': 'Atividade criada com sucesso!',
            'atividade': nova_atividade.serialize()
        }), 201
    except ValueError as e:
        return jsonify({'mensagem': f'Formato de data inválido: {str(e)}'}), 400
    except Exception as e:
        db.session.rollback()
        return jsonify({'mensagem': f'Erro ao criar atividade: {str(e)}'}), 500

@atividades_bp.route('/<int:atividade_id>', methods=['PUT'])
def atualizar_atividade(atividade_id):
    """Atualiza uma atividade existente"""
    usuario_id = session.get('usuario_id')
    
    if not usuario_id:
        return jsonify({'mensagem': 'Não autenticado'}), 401
    
    atividade = Atividade.query.get(atividade_id)
    
    if not atividade:
        return jsonify({'mensagem': 'Atividade não encontrada'}), 404
    
    if atividade.usuario_id != usuario_id:
        return jsonify({'mensagem': 'Acesso negado'}), 403
    
    dados = request.get_json()
    
    if not dados:
        return jsonify({'mensagem': 'Dados inválidos'}), 400
    
    try:
        if 'tipo' in dados:
            atividade.tipo = dados['tipo']
        
        if 'duracao' in dados:
            atividade.duracao = int(dados['duracao']) if dados['duracao'] else None
        
        if 'distancia' in dados:
            atividade.distancia = float(dados['distancia']) if dados['distancia'] else None
        
        if 'intensidade' in dados:
            atividade.intensidade = dados['intensidade']
        
        if 'data_atividade' in dados:
            atividade.data_atividade = datetime.fromisoformat(dados['data_atividade'].replace('Z', '+00:00'))
        
        if 'observacoes' in dados:
            atividade.observacoes = dados['observacoes']
        
        # Recalcula calorias se necessário
        usuario = Usuario.query.get(usuario_id)
        if atividade.duracao:
            atividade.calorias_queimadas = calcular_calorias(
                atividade.tipo,
                atividade.duracao,
                atividade.intensidade,
                usuario.peso or 70
            )
        
        db.session.commit()
        
        return jsonify({
            'mensagem': 'Atividade atualizada com sucesso!',
            'atividade': atividade.serialize()
        }), 200
    except ValueError as e:
        return jsonify({'mensagem': f'Formato de data inválido: {str(e)}'}), 400
    except Exception as e:
        db.session.rollback()
        return jsonify({'mensagem': f'Erro ao atualizar atividade: {str(e)}'}), 500

@atividades_bp.route('/<int:atividade_id>', methods=['DELETE'])
def deletar_atividade(atividade_id):
    """Deleta uma atividade"""
    usuario_id = session.get('usuario_id')
    
    if not usuario_id:
        return jsonify({'mensagem': 'Não autenticado'}), 401
    
    atividade = Atividade.query.get(atividade_id)
    
    if not atividade:
        return jsonify({'mensagem': 'Atividade não encontrada'}), 404
    
    if atividade.usuario_id != usuario_id:
        return jsonify({'mensagem': 'Acesso negado'}), 403
    
    try:
        db.session.delete(atividade)
        db.session.commit()
        
        return jsonify({'mensagem': 'Atividade excluída com sucesso!'}), 200
    except Exception as e:
        db.session.rollback()
        return jsonify({'mensagem': f'Erro ao deletar atividade: {str(e)}'}), 500

@atividades_bp.route('/resumo/stats', methods=['GET'])
def obter_estatisticas():
    """Obtém estatísticas de atividades do usuário"""
    usuario_id = session.get('usuario_id')
    
    if not usuario_id:
        return jsonify({'mensagem': 'Não autenticado'}), 401
    
    usuario = Usuario.query.get(usuario_id)
    if not usuario:
        return jsonify({'mensagem': 'Usuário não encontrado'}), 404
    
    atividades = Atividade.query.filter_by(usuario_id=usuario_id).all()
    
    total_atividades = len(atividades)
    total_duracao = sum(a.duracao or 0 for a in atividades)
    total_distancia = sum(a.distancia or 0 for a in atividades)
    total_calorias = sum(a.calorias_queimadas or 0 for a in atividades)
    
    # Atividade mais comum
    tipos = {}
    for a in atividades:
        tipos[a.tipo] = tipos.get(a.tipo, 0) + 1
    
    atividade_favorita = max(tipos, key=tipos.get) if tipos else None
    
    return jsonify({
        'total_atividades': total_atividades,
        'total_duracao_minutos': total_duracao,
        'total_distancia_km': round(total_distancia, 2),
        'total_calorias': round(total_calorias, 2),
        'atividade_favorita': atividade_favorita,
        'distribuicao_tipos': tipos
    }), 200
