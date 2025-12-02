#!/usr/bin/env python3
"""
FitTrack API Server
Servidor backend para o aplicativo de rastreamento de atividades físicas
"""

from flask import Flask, jsonify
from flask_cors import CORS
from flask_session import Session
from models.models import db
from routes.auth_refatorada import auth_bp
from routes.atividades_refatorada import atividades_bp
from config import config
import os
from datetime import datetime
# from routes.metas_refatorada import metas_bp

def create_app(config_name='development'):
    """Factory para criar e configurar a aplicação Flask"""
    
    # Cria a aplicação
    app = Flask(__name__)
    
    # Carrega configuração
    app.config.from_object(config.get(config_name, config['default']))
    
    # Inicializa extensões
    db.init_app(app)
    Session(app)
    
    # Configura CORS - permite requisições do frontend
    # IMPORTANTE: Inclui todas as portas possíveis do Live Server e outros servidores locais
    CORS(
        app,
        origins=[
            'http://127.0.0.1:5500',
            'http://127.0.0.1:5501',
            'http://127.0.0.1:3000',
            'http://localhost:5500',
            'http://localhost:5501',
            'http://localhost:3000',
            'http://localhost:8080'
        ],
        supports_credentials=True,
        allow_headers=['Content-Type', 'Authorization', 'X-Requested-With'],
        methods=['GET', 'POST', 'PUT', 'DELETE', 'OPTIONS', 'PATCH'],
        expose_headers=['Content-Type']
    )
    
    # Registra blueprints (rotas)
    app.register_blueprint(auth_bp)
    app.register_blueprint(atividades_bp)
    # app.register_blueprint(metas_bp)
    
    # Cria as tabelas do banco de dados
    with app.app_context():
        db.create_all()
    
    # ==================== ROTAS AUXILIARES ====================
    
    @app.route('/api/health', methods=['GET'])
    def health_check():
        """Verifica se a API está funcionando"""
        return jsonify({
            'status': 'API FitTrack está funcionando!',
            'version': '1.0.0',
            'timestamp': datetime.utcnow().isoformat()
        }), 200
    
    @app.route('/', methods=['GET'])
    def index():
        """Rota raiz com informações da API"""
        return jsonify({
            'app': 'FitTrack API',
            'version': '1.0.0',
            'description': 'API para rastreamento de atividades físicas',
            'endpoints': {
                'auth': {
                    'registrar': 'POST /api/auth/registrar',
                    'login': 'POST /api/auth/login',
                    'logout': 'POST /api/auth/logout',
                    'usuario-atual': 'GET /api/auth/usuario-atual',
                    'atualizar-perfil': 'PUT /api/auth/atualizar-perfil'
                },
                'atividades': {
                    'listar': 'GET /api/atividades',
                    'obter': 'GET /api/atividades/<id>',
                    'criar': 'POST /api/atividades',
                    'atualizar': 'PUT /api/atividades/<id>',
                    'deletar': 'DELETE /api/atividades/<id>',
                    'estatisticas': 'GET /api/atividades/resumo/stats'
                },
                # 'metas': {
                #     'listar': 'GET /api/metas',
                #     'obter': 'GET /api/metas/<id>',
                #     'criar': 'POST /api/metas',
                #     'atualizar': 'PUT /api/metas/<id>',
                #     'deletar': 'DELETE /api/metas/<id>'
                # }
            }
        }), 200
    
    # ==================== TRATAMENTO DE ERROS ====================
    
    @app.errorhandler(404)
    def not_found(error):
        """Tratamento para erro 404"""
        return jsonify({
            'mensagem': 'Recurso não encontrado',
            'status': 404
        }), 404
    
    @app.errorhandler(500)
    def internal_error(error):
        """Tratamento para erro 500"""
        db.session.rollback()
        return jsonify({
            'mensagem': 'Erro interno do servidor',
            'status': 500
        }), 500
    
    @app.errorhandler(400)
    def bad_request(error):
        """Tratamento para erro 400"""
        return jsonify({
            'mensagem': 'Requisição inválida',
            'status': 400
        }), 400
    
    @app.errorhandler(401)
    def unauthorized(error):
        """Tratamento para erro 401"""
        return jsonify({
            'mensagem': 'Não autorizado',
            'status': 401
        }), 401
    
    @app.errorhandler(403)
    def forbidden(error):
        """Tratamento para erro 403"""
        return jsonify({
            'mensagem': 'Acesso proibido',
            'status': 403
        }), 403
    
    # ==================== MIDDLEWARE ====================
    
    @app.before_request
    def antes_request():
        """Executado antes de cada requisição"""
        pass
    
    @app.after_request
    def apos_request(response):
        """Executado após cada requisição"""
        response.headers['Content-Type'] = 'application/json; charset=utf-8'
        return response
    
    return app


if __name__ == '__main__':
    # Detecta ambiente (development ou production)
    env = os.getenv('FLASK_ENV', 'development')
    debug_mode = env == 'development'
    
    # Cria e executa a aplicação
    app = create_app(env)
    
    print(f"""
    ╔════════════════════════════════════════╗
    ║         FitTrack API Server            ║
    ║       Iniciando em modo {env}      ║
    ╚════════════════════════════════════════╝
    
    🚀 Servidor rodando em http://0.0.0.0:5000 (ou http://127.0.0.1:5000)
    📚 Documentação em http://127.0.0.1:5000/
    """)
    
    app.run(
        debug=debug_mode,
        host='0.0.0.0',
        port=5000,
        use_reloader=debug_mode
    )
