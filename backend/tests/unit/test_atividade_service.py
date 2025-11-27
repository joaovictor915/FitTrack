"""
Testes Unitários - Serviço de Atividades
"""

import pytest
from services.usuario_service import AtividadeService
from domain.entities import Atividade
from repositories.base_repository import AtividadeRepository, UsuarioRepository
from unittest.mock import Mock


@pytest.fixture
def mock_atividade_repository():
    """Mock do repositório de atividades"""
    return Mock(spec=AtividadeRepository)


@pytest.fixture
def mock_usuario_repository():
    """Mock do repositório de usuários"""
    return Mock(spec=UsuarioRepository)


@pytest.fixture
def atividade_service(mock_atividade_repository, mock_usuario_repository):
    """Instância do serviço com repositórios mock"""
    return AtividadeService(mock_atividade_repository, mock_usuario_repository)


class TestAtividadeServiceCalorias:
    """Testes de cálculo de calorias"""
    
    def test_calcular_calorias_corrida(self, atividade_service):
        """Testa cálculo de calorias para corrida"""
        calorias = atividade_service.calcular_calorias('corrida', 30, 'moderada', 70)
        assert calorias == 12 * 30  # 360
    
    def test_calcular_calorias_com_peso_diferente(self, atividade_service):
        """Testa cálculo de calorias com peso diferente"""
        calorias = atividade_service.calcular_calorias('corrida', 30, 'moderada', 85)
        # (12 * 30 * 85) / 70 = 436.28... = 436
        assert calorias == round((12 * 30 * 85) / 70)
    
    def test_calcular_calorias_tipo_invalido(self, atividade_service):
        """Testa cálculo com tipo inválido"""
        calorias = atividade_service.calcular_calorias('tipo_inexistente', 30, 'moderada', 70)
        assert calorias == 0
    
    def test_calcular_calorias_intensidades(self, atividade_service):
        """Testa cálculo com diferentes intensidades"""
        baixa = atividade_service.calcular_calorias('corrida', 30, 'baixa', 70)
        moderada = atividade_service.calcular_calorias('corrida', 30, 'moderada', 70)
        alta = atividade_service.calcular_calorias('corrida', 30, 'alta', 70)
        
        assert baixa < moderada < alta


class TestAtividadeServiceCriar:
    """Testes de criação de atividades"""
    
    def test_criar_atividade_sucesso(self, atividade_service, mock_usuario_repository, mock_atividade_repository):
        """Testa criação bem-sucedida de atividade"""
        mock_usuario = Mock()
        mock_usuario.peso = 70
        mock_usuario_repository.find_by_id.return_value = mock_usuario
        
        mock_atividade = Mock(spec=Atividade)
        mock_atividade.serialize.return_value = {'id': 1, 'tipo': 'corrida'}
        mock_atividade_repository.save.return_value = mock_atividade
        
        dados = {
            'tipo': 'corrida',
            'duracao': 30,
            'intensidade': 'moderada',
            'distancia': 5.0
        }
        
        atividade, msg, status = atividade_service.criar_atividade(1, dados)
        
        assert status == 201
        assert msg == "Atividade criada com sucesso"
        assert atividade is not None
    
    def test_criar_atividade_usuario_inexistente(self, atividade_service, mock_usuario_repository):
        """Testa criação com usuário inexistente"""
        mock_usuario_repository.find_by_id.return_value = None
        
        dados = {'tipo': 'corrida', 'duracao': 30}
        atividade, msg, status = atividade_service.criar_atividade(999, dados)
        
        assert status == 404
        assert "Usuário não encontrado" in msg
    
    def test_criar_atividade_tipo_invalido(self, atividade_service, mock_usuario_repository):
        """Testa criação com tipo inválido"""
        mock_usuario = Mock()
        mock_usuario_repository.find_by_id.return_value = mock_usuario
        
        dados = {'tipo': 'tipo_inexistente', 'duracao': 30}
        atividade, msg, status = atividade_service.criar_atividade(1, dados)
        
        assert status == 400
        assert "Tipo de atividade inválido" in msg


class TestAtividadeServiceListar:
    """Testes de listagem de atividades"""
    
    def test_listar_atividades_sucesso(self, atividade_service, mock_usuario_repository, mock_atividade_repository):
        """Testa listagem bem-sucedida"""
        mock_usuario = Mock()
        mock_usuario_repository.find_by_id.return_value = mock_usuario
        
        mock_atividades = [Mock(spec=Atividade), Mock(spec=Atividade)]
        mock_atividade_repository.find_by_usuario.return_value = (mock_atividades, 2)
        
        atividades, total, msg, status = atividade_service.listar_atividades(1)
        
        assert status == 200
        assert len(atividades) == 2
        assert total == 2
    
    def test_listar_atividades_usuario_inexistente(self, atividade_service, mock_usuario_repository):
        """Testa listagem com usuário inexistente"""
        mock_usuario_repository.find_by_id.return_value = None
        
        atividades, total, msg, status = atividade_service.listar_atividades(999)
        
        assert status == 404
        assert "Usuário não encontrado" in msg
