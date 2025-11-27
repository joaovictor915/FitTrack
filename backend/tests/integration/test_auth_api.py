"""
Testes de Integração - API de Autenticação
"""

import pytest
import json
from server import create_app
from models.models import db, Usuario


@pytest.fixture
def app():
    """Cria aplicação de teste"""
    app = create_app('testing')
    
    with app.app_context():
        db.create_all()
        yield app
        db.session.remove()
        db.drop_all()


@pytest.fixture
def client(app):
    """Cliente para fazer requisições"""
    return app.test_client()


@pytest.fixture
def runner(app):
    """CLI runner"""
    return app.test_cli_runner()


class TestAuthAPI:
    """Testes da API de Autenticação"""
    
    def test_registrar_usuario_valido(self, client):
        """Testa registro de usuário válido"""
        response = client.post('/api/auth/registrar', 
            json={
                'nome': 'Test User',
                'email': 'test@test.com',
                'senha': 'Senha123!'
            },
            content_type='application/json'
        )
        
        assert response.status_code == 201
        data = json.loads(response.data)
        assert 'usuario' in data
        assert data['usuario']['email'] == 'test@test.com'
    
    def test_registrar_usuario_duplicado(self, client):
        """Testa registro com email duplicado"""
        # Primeiro registro
        client.post('/api/auth/registrar',
            json={
                'nome': 'User 1',
                'email': 'test@test.com',
                'senha': 'Senha123!'
            },
            content_type='application/json'
        )
        
        # Tentativa de registro duplicado
        response = client.post('/api/auth/registrar',
            json={
                'nome': 'User 2',
                'email': 'test@test.com',
                'senha': 'Senha456!'
            },
            content_type='application/json'
        )
        
        assert response.status_code == 400
        data = json.loads(response.data)
        assert 'Email já cadastrado' in data['mensagem']
    
    def test_registrar_campos_obrigatorios(self, client):
        """Testa registro sem campos obrigatórios"""
        response = client.post('/api/auth/registrar',
            json={
                'nome': 'User',
                'email': 'test@test.com'
                # Falta senha
            },
            content_type='application/json'
        )
        
        assert response.status_code == 400
    
    def test_login_usuario_valido(self, client):
        """Testa login com credenciais válidas"""
        # Registro
        client.post('/api/auth/registrar',
            json={
                'nome': 'Test User',
                'email': 'test@test.com',
                'senha': 'Senha123!'
            },
            content_type='application/json'
        )
        
        # Login
        response = client.post('/api/auth/login',
            json={
                'email': 'test@test.com',
                'senha': 'Senha123!'
            },
            content_type='application/json'
        )
        
        assert response.status_code == 200
        data = json.loads(response.data)
        assert 'usuario' in data
    
    def test_login_senha_incorreta(self, client):
        """Testa login com senha incorreta"""
        # Registro
        client.post('/api/auth/registrar',
            json={
                'nome': 'Test User',
                'email': 'test@test.com',
                'senha': 'Senha123!'
            },
            content_type='application/json'
        )
        
        # Login com senha errada
        response = client.post('/api/auth/login',
            json={
                'email': 'test@test.com',
                'senha': 'SenhaErrada123!'
            },
            content_type='application/json'
        )
        
        assert response.status_code == 401
        data = json.loads(response.data)
        assert 'Email ou senha incorretos' in data['mensagem']
    
    def test_logout(self, client):
        """Testa logout"""
        response = client.post('/api/auth/logout', content_type='application/json')
        assert response.status_code == 200
