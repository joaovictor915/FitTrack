# FitTrack - Aplicativo de Rastreamento de Fitness

Link com vídeo para apresentação: https://youtu.be/T5i0QB1ZaAc?si=ozrVShHI2oc5uRI7

Um aplicativo web completo para rastreamento de atividades físicas, desenvolvido com arquitetura MVC.

## 🏗️ Estrutura do Projeto

```
FitTrack/
├── backend/                    # API Backend (Python/Flask)
│   ├── models/
│   │   └── models.py          # Modelos (Usuario, Atividade)
│   ├── routes/
│   │   ├── auth.py            # Rotas de autenticação
│   │   └── atividades.py      # Rotas de atividades
│   ├── config.py              # Configurações
│   └── server.py              # Servidor principal
├── js/                         # Frontend (JavaScript)
│   ├── api/
│   │   └── APIClient.js       # Cliente HTTP para API
│   ├── controllers/
│   │   └── Controllers.js     # Lógica da aplicação
│   ├── utils/
│   │   └── Utilidades.js      # Funções auxiliares
│   └── views/
│       └── (Views específicas por página)
├── index.html                 # Página inicial
├── login.html                 # Página de login
├── cadastro.html              # Página de cadastro
├── perfil.html                # Página de perfil
├── dashboard.html             # Dashboard
├── registro_atividade.html    # Registro de atividades
├── historico.html             # Histórico de atividades
├── style.css                  # Estilos
└── requirements.txt           # Dependências Python
```

## 🚀 Como Usar

### 1. Instalar Dependências Backend

```bash
# Crie um ambiente virtual (opcional mas recomendado)
python -m venv venv

# No Windows (PowerShell):
.\venv\Scripts\Activate.ps1

# No Mac/Linux:
source venv/bin/activate

# Instale as dependências
pip install -r requirements.txt
```

### 2. Iniciar o Servidor Backend

```bash
# No diretório raiz do projeto
python backend/server.py
```

O servidor estará rodando em `http://127.0.0.1:5000`

### 3. Abrir o Frontend

- Use VS Code com a extensão **Live Server**
- Clique direito em `index.html` → "Open with Live Server"
- Ou acesse `http://127.0.0.1:5500/index.html`

## 🔧 Arquitetura MVC

### Backend (Python/Flask)

**Models** (`backend/models/models.py`):
- `Usuario`: Dados do usuário (nome, email, senha, dados de saúde)
- `Atividade`: Dados de atividade (tipo, duração, intensidade, calorias)

**Routes (Controllers)**:
- `backend/routes/auth.py`: Autenticação e gerenciamento de perfil
- `backend/routes/atividades.py`: CRUD de atividades

**Config** (`backend/config.py`):
- Configurações por ambiente (desenvolvimento, teste, produção)
- Banco de dados SQLite
- Segurança e CORS

### Frontend (JavaScript)

**API Client** (`js/api/APIClient.js`):
- Comunicação com backend via HTTP
- Gerenciamento de requisições

**Controllers** (`js/controllers/Controllers.js`):
- `AuthController`: Lógica de autenticação
- `AtividadesController`: Lógica de atividades

**Utils** (`js/utils/Utilidades.js`):
- Formatação de dados
- Validações
- Cálculos (IMC)
- Mensagens ao usuário

## 📚 Endpoints da API

### Autenticação

```
POST   /api/auth/registrar          # Criar nova conta
POST   /api/auth/login              # Fazer login
POST   /api/auth/logout             # Fazer logout
GET    /api/auth/usuario-atual      # Dados do usuário logado
PUT    /api/auth/atualizar-perfil   # Atualizar perfil
```

### Atividades

```
GET    /api/atividades              # Listar atividades (com paginação)
POST   /api/atividades              # Criar atividade
GET    /api/atividades/<id>         # Obter atividade específica
PUT    /api/atividades/<id>         # Atualizar atividade
DELETE /api/atividades/<id>         # Deletar atividade
GET    /api/atividades/resumo/stats # Estatísticas do usuário
```

## 🗄️ Banco de Dados

O projeto usa **SQLite** por padrão. O arquivo `fittrack.db` será criado automaticamente.

### Tabelas:

**usuarios**
- id (INT, PK)
- nome (VARCHAR)
- email (VARCHAR, UNIQUE)
- senha_hash (VARCHAR)
- idade (INT)
- peso (FLOAT)
- altura (INT)
- data_criacao (DATETIME)

**atividades**
- id (INT, PK)
- usuario_id (INT, FK)
- tipo (VARCHAR)
- duracao (INT)
- distancia (FLOAT)
- intensidade (VARCHAR)
- calorias_queimadas (FLOAT)
- data_atividade (DATETIME)
- data_criacao (DATETIME)
- observacoes (TEXT)

## 🔐 Autenticação

- Senhas são hash com **bcrypt** (via `werkzeug.security`)
- Sessões gerenciadas pelo Flask
- CORS configurado para aceitar requisições do frontend
- Validação de força de senha

## 📊 Funcionalidades

- ✅ Registro e login de usuários
- ✅ Perfil de usuário com dados de saúde
- ✅ Registro de atividades físicas
- ✅ Cálculo automático de calorias queimadas
- ✅ Histórico de atividades
- ✅ Estatísticas de atividades
- ✅ Paginação de dados
- ✅ Validações no frontend e backend

## 📱 Tecnologias

**Backend:**
- Flask (Python)
- SQLAlchemy (ORM)
- Flask-CORS
- Flask-Session
- Werkzeug (Hash de senha)

**Frontend:**
- HTML5
- CSS3
- JavaScript (ES6+)
- Fetch API

## ⚙️ Variáveis de Ambiente

Crie um arquivo `.env` na raiz para configurações customizadas:

```env
FLASK_ENV=development
DATABASE_URL=sqlite:///fittrack.db
SECRET_KEY=sua-chave-secreta
```

## 🐛 Troubleshooting

**Erro: "Não conseguir conectar à API"**
- Certifique-se de que o servidor Flask está rodando
- Verifique se está na porta 5000
- Confira o CORS em `backend/config.py`

**Erro: "Banco de dados corrompido"**
- Delete `fittrack.db` e reinicie o servidor
- As tabelas serão recriadas automaticamente

**Erro: "Sessão expirada"**
- Faça login novamente
- Verifique a configuração de `PERMANENT_SESSION_LIFETIME` em `config.py`

## 📝 Notas

- O projeto usa armazenamento de sessão em arquivo (pasta `flask_session`)
- Para produção, considere usar PostgreSQL ao invés de SQLite
- Implemente autenticação com JWT para APIs mobile

## 👨‍💻 Desenvolvimento

Para adicionar novas funcionalidades:

1. Crie modelos em `backend/models/models.py`
2. Implemente rotas em `backend/routes/`
3. Crie controllers no frontend em `js/controllers/`
4. Adicione métodos ao `APIClient` em `js/api/APIClient.js`

## 📄 Licença

Projeto educacional - Livre para uso e modificação.

---

**Desenvolvido com ❤️ para aprendizado**
