# 🚀 FitTrack - Guia de Uso

## ✅ Checklist de Inicialização

### 1️⃣ Instalar Dependências

Abra o PowerShell na pasta do projeto e execute:

```powershell
pip install -r requirements.txt
```

Ou use o script de inicialização:

```powershell
python iniciar.py
```

### 2️⃣ Iniciar o Servidor Backend

```powershell
python backend/server.py
```

Você verá a mensagem:
```
╔════════════════════════════════════════╗
║         FitTrack API Server            ║
║       Iniciando em modo development    ║
╚════════════════════════════════════════╝

🚀 Servidor rodando em http://127.0.0.1:5000
📚 Documentação em http://127.0.0.1:5000/
```

### 3️⃣ Abrir o Frontend

**Opção A: Com Live Server (VS Code)**
1. Instale a extensão "Live Server"
2. Clique direito em `login.html`
3. Selecione "Open with Live Server"

**Opção B: Manualmente**
- Abra seu navegador em `http://127.0.0.1:5500/login.html`

---

## 🎮 Como Usar a Aplicação

### 📝 Criar uma Conta

1. Acesse `http://127.0.0.1:5500/login.html`
2. Clique em "Crie sua conta"
3. Preencha os dados:
   - **Nome:** Seu nome completo
   - **Email:** Um email válido (não precisa existir de verdade)
   - **Senha:** Mín. 8 caracteres com letras, números e caracteres especiais

Exemplo de senha forte: `Senha123!@#`

### 🔑 Fazer Login

1. Volte à tela de login
2. Digite o email e senha cadastrados
3. Clique em "Entrar"
4. Será redirecionado para o Dashboard

### 👤 Atualizar Perfil

1. No Dashboard, clique em "Meu Perfil"
2. Atualize seus dados:
   - Idade
   - Peso (kg)
   - Altura (cm)
3. O sistema calcula automaticamente seu IMC
4. Clique em "Salvar Alterações"

### 💪 Registrar uma Atividade

1. No Dashboard, clique em "Registrar Atividade"
2. Preencha os dados:
   - **Tipo:** Corrida, Caminhada, Musculação, etc.
   - **Duração:** Em minutos
   - **Distância:** Em km (opcional)
   - **Intensidade:** Baixa, Moderada, Alta
3. As calorias são calculadas automaticamente baseado no seu peso
4. Clique em "Salvar Atividade"

### 📊 Ver Histórico de Atividades

1. No Dashboard, clique em "Histórico"
2. Veja todas as suas atividades listadas
3. Para **editar**: Clique em "✏️ Editar" e atualize os dados
4. Para **deletar**: Clique em "🗑️ Deletar" e confirme

### 📈 Ver Estatísticas

As estatísticas aparecem no Dashboard:
- Total de atividades
- Total de minutos de exercício
- Total de km percorridos
- Total de calorias queimadas
- Atividade favorita

---

## 🗄️ Banco de Dados

O arquivo `fittrack.db` é criado automaticamente na primeira execução.

Para **resetar** o banco de dados (apagar todos os dados):
1. Feche o servidor
2. Delete o arquivo `fittrack.db`
3. Reinicie o servidor

---

## 🔗 API Endpoints

Todos os endpoints requerem autenticação via sessão.

### Autenticação
```
POST   /api/auth/registrar          # Criar conta
POST   /api/auth/login              # Fazer login
POST   /api/auth/logout             # Fazer logout
GET    /api/auth/usuario-atual      # Dados do usuário
PUT    /api/auth/atualizar-perfil   # Atualizar perfil
```

### Atividades
```
GET    /api/atividades              # Listar atividades
POST   /api/atividades              # Criar atividade
GET    /api/atividades/<id>         # Obter uma atividade
PUT    /api/atividades/<id>         # Atualizar atividade
DELETE /api/atividades/<id>         # Deletar atividade
GET    /api/atividades/resumo/stats # Estatísticas
```

---

## 📝 Exemplos de Requisições (cURL)

### Registrar
```bash
curl -X POST http://127.0.0.1:5000/api/auth/registrar \
  -H "Content-Type: application/json" \
  -d '{
    "nome": "João Silva",
    "email": "joao@example.com",
    "senha": "Senha123!@#"
  }' \
  -c cookies.txt
```

### Login
```bash
curl -X POST http://127.0.0.1:5000/api/auth/login \
  -H "Content-Type: application/json" \
  -d '{
    "email": "joao@example.com",
    "senha": "Senha123!@#"
  }' \
  -c cookies.txt
```

### Criar Atividade
```bash
curl -X POST http://127.0.0.1:5000/api/atividades \
  -H "Content-Type: application/json" \
  -d '{
    "tipo": "corrida",
    "duracao": 30,
    "distancia": 5.5,
    "intensidade": "alta",
    "data_atividade": "2025-11-27T15:30:00"
  }' \
  -b cookies.txt
```

---

## 🐛 Troubleshooting

### "Cannot connect to API"
- Verifique se o servidor está rodando: `python backend/server.py`
- Confira se está na porta 5000
- Verifique o CORS em `backend/config.py`

### "Database locked"
- Feche o servidor
- Delete `fittrack.db`
- Reinicie

### "Module not found"
- Execute: `pip install -r requirements.txt`

### Sessão expirada
- Faça login novamente
- Aumente `PERMANENT_SESSION_LIFETIME` em `backend/config.py`

---

## 📚 Estrutura de Pastas

```
FitTrack/
├── backend/
│   ├── models/
│   │   └── models.py         # Models: Usuario, Atividade
│   ├── routes/
│   │   ├── auth.py           # Autenticação
│   │   └── atividades.py     # Atividades
│   ├── config.py             # Configuração
│   └── server.py             # Servidor principal
├── js/
│   ├── api/
│   │   └── APIClient.js      # Cliente HTTP
│   ├── controllers/
│   │   └── Controllers.js    # Lógica
│   └── utils/
│       └── Utilidades.js     # Funções auxiliares
├── [páginas HTML]
├── style.css                 # Estilos
├── requirements.txt          # Dependências
└── README.md                 # Documentação
```

---

## 🎯 Funcionalidades Implementadas

- ✅ Registro e login de usuários
- ✅ Perfil com dados de saúde (peso, altura, idade)
- ✅ Cálculo de IMC automático
- ✅ Registro de atividades com cálculo de calorias
- ✅ Histórico completo com edição e exclusão
- ✅ Estatísticas gerais
- ✅ Validações no frontend e backend
- ✅ Senhas com hash seguro
- ✅ Sessões do usuário

---

## 🚀 Próximas Melhorias

- [ ] Autenticação com JWT
- [ ] Suporte a múltiplos idiomas
- [ ] Gráficos de progresso
- [ ] Integração com wearables
- [ ] App mobile (React Native)
- [ ] Recuperação de senha por email
- [ ] Sistema de pontos/badges

---

## 📞 Suporte

Para dúvidas ou problemas, verifique:
1. Se todas as dependências foram instaladas
2. Se o servidor está rodando
3. Se você está usando a URL correta do frontend
4. Os logs no console do navegador (F12)

---

**Desenvolvido com ❤️ para aprendizado**
