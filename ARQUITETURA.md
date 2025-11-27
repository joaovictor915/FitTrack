# FitTrack - Arquitetura em Camadas

## Estrutura do Projeto

### Backend

```
backend/
├── domain/              # Camada de Domínio (Entidades)
│   ├── entities.py      # Classes de entidades de negócio
│   └── __init__.py
├── repositories/        # Camada de Persistência
│   ├── base_repository.py  # Interfaces e implementações de repositórios
│   └── __init__.py
├── services/           # Camada de Serviços (Lógica de Negócio)
│   ├── usuario_service.py  # Serviços de usuário e atividades
│   └── __init__.py
├── routes/            # Rotas e Controllers
│   ├── auth.py        # Rotas de autenticação (legado)
│   ├── auth_refatorada.py  # Rotas refatoradas
│   ├── atividades.py  # Rotas de atividades (legado)
│   ├── atividades_refatorada.py  # Rotas refatoradas
│   └── __init__.py
├── tests/             # Testes
│   ├── unit/          # Testes unitários
│   ├── integration/   # Testes de integração
│   └── __init__.py
├── models/           # Modelos (SQLAlchemy)
│   └── models.py
├── config.py         # Configurações
└── server.py         # Aplicação principal
```

### Frontend

```
frontend/
├── public/                    # Arquivos estáticos
│   ├── *.html                 # Páginas
│   └── style.css              # Estilos
└── src/                       # Código-fonte
    ├── api/                   # Camada de API
    │   └── APIClient.js
    ├── controllers/           # Controladores
    │   └── Controllers.js
    ├── utils/                 # Utilitários
    │   └── Utilidades.js
    └── views/                 # Componentes de visualização
```

## Conceitos de Arquitetura

### 1. Camada de Domínio (Domain Layer)

Contém as entidades de negócio independentes de qualquer framework.

**Exemplo:**
```python
# backend/domain/entities.py
class Usuario:
    def __init__(self, id=None, nome=None, email=None):
        self.id = id
        self.nome = nome
        self.email = email
    
    def to_dict(self):
        return {'id': self.id, 'nome': self.nome, 'email': self.email}
```

**Características:**
- Sem dependências de frameworks
- Lógica de validação do domínio
- Métodos de conversão (to_dict, to_json)

---

### 2. Camada de Persistência (Persistence Layer)

Abstrai o acesso aos dados através de repositórios.

**Exemplo:**
```python
# backend/repositories/base_repository.py
class UsuarioRepository(BaseRepository):
    def __init__(self, db):
        self.db = db
    
    def save(self, entity):
        usuario = UsuarioDB(nome=entity.nome, email=entity.email)
        self.db.session.add(usuario)
        self.db.session.commit()
        return usuario
    
    def find_by_email(self, email):
        return UsuarioDB.query.filter_by(email=email).first()
```

**Responsabilidades:**
- Operações CRUD (Create, Read, Update, Delete)
- Consultas ao banco de dados
- Conversão entre entities do domínio e modelos ORM

---

### 3. Camada de Serviços (Service Layer)

Implementa a lógica de negócio da aplicação.

**Exemplo:**
```python
# backend/services/usuario_service.py
class UsuarioService:
    def __init__(self, repository):
        self.repository = repository
    
    def registrar(self, nome, email, senha):
        # Validações
        if not self.validar_email(email):
            return None, "Email inválido", 400
        
        # Lógica de negócio
        usuario = Usuario(nome=nome, email=email)
        usuario.set_password(senha)
        
        # Persistência
        usuario_salvo = self.repository.save(usuario)
        return usuario_salvo, "Usuário registrado", 201
```

**Responsabilidades:**
- Validações de negócio
- Cálculos e transformações
- Orquestração entre repositórios
- Tratamento de exceções

---

### 4. Camada de Rotas (Routes/Controllers)

Expõe os serviços através de endpoints HTTP.

**Exemplo:**
```python
# backend/routes/auth_refatorada.py
@auth_bp.route('/login', methods=['POST'])
def login():
    dados = request.get_json()
    servico = get_usuario_service()
    
    usuario, mensagem, status_code = servico.fazer_login(
        dados.get('email'),
        dados.get('senha')
    )
    
    if status_code != 200:
        return jsonify({'mensagem': mensagem}), status_code
    
    session['usuario_id'] = usuario.id
    return jsonify({'usuario': usuario.serialize_sem_sensivel()}), status_code
```

---

## Fluxo de Dados

```
Request HTTP
    ↓
Routes/Controllers (auth_refatorada.py)
    ↓
Service Layer (usuario_service.py) - Validações e Lógica
    ↓
Repository Layer (base_repository.py) - Acesso a Dados
    ↓
Domain Entities (entities.py) ↔ ORM Models (models.py)
    ↓
Database (SQLite)
    ↓
Response HTTP
```

## Testes

### Testes Unitários

Testam a lógica de negócio isoladamente com mocks.

```bash
pytest backend/tests/unit -v
```

**Exemplo:**
```python
# backend/tests/unit/test_usuario_service.py
def test_registrar_sucesso(usuario_service, mock_repository):
    mock_repository.find_by_email.return_value = None
    usuario, msg, status = usuario_service.registrar("User", "user@test.com", "Senha123!")
    assert status == 201
```

### Testes de Integração

Testam os endpoints da API com banco de dados de teste.

```bash
pytest backend/tests/integration -v
```

**Exemplo:**
```python
# backend/tests/integration/test_auth_api.py
def test_login_usuario_valido(client):
    # Prepara
    client.post('/api/auth/registrar', json={...})
    
    # Executa
    response = client.post('/api/auth/login', json={...})
    
    # Verifica
    assert response.status_code == 200
```

## GitHub Actions

O workflow `.github/workflows/tests.yml` executa automaticamente:

1. Testes unitários
2. Testes de integração
3. Cobertura de código
4. Upload para Codecov

Acionado por:
- Push para `main` ou `develop`
- Pull requests

## Frontend

### Estrutura

```
frontend/
├── public/             # Distribuição
│   ├── index.html
│   ├── login.html
│   └── style.css
└── src/                # Desenvolvimento
    ├── api/            # HTTP Client
    ├── controllers/    # Lógica de negócio
    ├── utils/          # Helpers
    └── views/          # Componentes (futuro)
```

### Padrão MVC

```
View (HTML)
    ↓
Controller (APIClient + Controllers.js)
    ↓
Model (dados do usuário/atividades)
    ↓
API Backend
```

## Como Usar

### Executar Servidor

```bash
cd backend
python server.py
```

### Executar Testes

```bash
# Todos os testes
pytest

# Apenas unitários
pytest backend/tests/unit -v

# Apenas integração
pytest backend/tests/integration -v

# Com cobertura
pytest --cov=backend/services --cov-report=html
```

### Desenvolver Nova Feature

1. Crie a entidade em `domain/entities.py`
2. Crie o repositório em `repositories/base_repository.py`
3. Crie o serviço em `services/usuario_service.py`
4. Crie a rota em `routes/auth_refatorada.py` ou `routes/atividades_refatorada.py`
5. Escreva testes em `tests/unit/` e `tests/integration/`
6. Faça commit e abra PR

## Boas Práticas

✅ **Faça:**
- Validar dados na camada de serviços
- Usar repositórios para acesso a dados
- Escrever testes para novas features
- Manter entidades do domínio simples e independentes
- Usar type hints em Python 3.9+

❌ **Não faça:**
- Lógica de negócio nas rotas
- Queries SQL diretas (use ORM)
- Dependências circulares entre módulos
- Modificar objetos de domínio sem validação

---

**Última atualização:** 27/11/2025
