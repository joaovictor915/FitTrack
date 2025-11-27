"""
Testes Unitários - Serviço de Usuário
"""

import pytest
from services.usuario_service import UsuarioService
from domain.entities import Usuario
from repositories.base_repository import UsuarioRepository
from unittest.mock import Mock, MagicMock


@pytest.fixture
def mock_repository():
    """Mock do repositório"""
    return Mock(spec=UsuarioRepository)


@pytest.fixture
def usuario_service(mock_repository):
    """Instância do serviço com repositório mock"""
    return UsuarioService(mock_repository)


class TestUsuarioServiceValidacoes:
    """Testes de validações do UsuarioService"""
    
    def test_validar_email_valido(self, usuario_service):
        """Testa validação de email válido"""
        assert usuario_service.validar_email("user@example.com") is True
    
    def test_validar_email_invalido(self, usuario_service):
        """Testa validação de email inválido"""
        assert usuario_service.validar_email("invalid-email") is False
        assert usuario_service.validar_email("user@") is False
        assert usuario_service.validar_email("@example.com") is False
    
    def test_validar_senha_forte(self, usuario_service):
        """Testa validação de senha forte"""
        valido, _ = usuario_service.validar_senha("Senha123!")
        assert valido is True
    
    def test_validar_senha_fraca_comprimento(self, usuario_service):
        """Testa validação de senha com comprimento insuficiente"""
        valido, msg = usuario_service.validar_senha("Pass12!")
        assert valido is False
        assert "mínimo 8" in msg
    
    def test_validar_senha_fraca_maiuscula(self, usuario_service):
        """Testa validação de senha sem maiúscula"""
        valido, msg = usuario_service.validar_senha("senha123!")
        assert valido is False
        assert "maiúscula" in msg
    
    def test_validar_senha_fraca_minuscula(self, usuario_service):
        """Testa validação de senha sem minúscula"""
        valido, msg = usuario_service.validar_senha("SENHA123!")
        assert valido is False
        assert "minúscula" in msg
    
    def test_validar_senha_fraca_numero(self, usuario_service):
        """Testa validação de senha sem número"""
        valido, msg = usuario_service.validar_senha("Senhaabcd!")
        assert valido is False
        assert "número" in msg
    
    def test_validar_senha_fraca_especial(self, usuario_service):
        """Testa validação de senha sem caractere especial"""
        valido, msg = usuario_service.validar_senha("Senha1234")
        assert valido is False
        assert "especial" in msg


class TestUsuarioServiceRegistrar:
    """Testes de registro do UsuarioService"""
    
    def test_registrar_sucesso(self, usuario_service, mock_repository):
        """Testa registro bem-sucedido"""
        mock_repository.find_by_email.return_value = None
        mock_usuario = Mock(spec=Usuario)
        mock_usuario.id = 1
        mock_usuario.serialize_sem_sensivel.return_value = {'id': 1, 'email': 'user@test.com'}
        mock_repository.save.return_value = mock_usuario
        
        usuario, msg, status = usuario_service.registrar("User", "user@test.com", "Senha123!")
        
        assert status == 201
        assert msg == "Usuário registrado com sucesso"
        assert usuario is not None
    
    def test_registrar_email_duplicado(self, usuario_service, mock_repository):
        """Testa registro com email duplicado"""
        mock_repository.find_by_email.return_value = Mock()
        
        usuario, msg, status = usuario_service.registrar("User", "user@test.com", "Senha123!")
        
        assert status == 400
        assert "Email já cadastrado" in msg
        assert usuario is None
    
    def test_registrar_dados_obrigatorios(self, usuario_service):
        """Testa registro sem dados obrigatórios"""
        usuario, msg, status = usuario_service.registrar("", "email@test.com", "Senha123!")
        assert status == 400
        
        usuario, msg, status = usuario_service.registrar("User", "", "Senha123!")
        assert status == 400
        
        usuario, msg, status = usuario_service.registrar("User", "email@test.com", "")
        assert status == 400


class TestUsuarioServiceLogin:
    """Testes de login do UsuarioService"""
    
    def test_login_sucesso(self, usuario_service, mock_repository):
        """Testa login bem-sucedido"""
        mock_usuario = Mock(spec=Usuario)
        mock_usuario.check_password.return_value = True
        mock_usuario.serialize_sem_sensivel.return_value = {'id': 1, 'email': 'user@test.com'}
        mock_repository.find_by_email.return_value = mock_usuario
        
        usuario, msg, status = usuario_service.fazer_login("user@test.com", "Senha123!")
        
        assert status == 200
        assert msg == "Login realizado com sucesso"
        assert usuario is not None
    
    def test_login_email_incorreto(self, usuario_service, mock_repository):
        """Testa login com email incorreto"""
        mock_repository.find_by_email.return_value = None
        
        usuario, msg, status = usuario_service.fazer_login("user@test.com", "Senha123!")
        
        assert status == 401
        assert "Email ou senha incorretos" in msg
        assert usuario is None
    
    def test_login_senha_incorreta(self, usuario_service, mock_repository):
        """Testa login com senha incorreta"""
        mock_usuario = Mock(spec=Usuario)
        mock_usuario.check_password.return_value = False
        mock_repository.find_by_email.return_value = mock_usuario
        
        usuario, msg, status = usuario_service.fazer_login("user@test.com", "SenhaErrada123!")
        
        assert status == 401
        assert "Email ou senha incorretos" in msg
        assert usuario is None
