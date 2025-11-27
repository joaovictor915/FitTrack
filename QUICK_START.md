# ⚡ QUICK START - FitTrack

## 1️⃣ Terminal 1 - Instalar e Iniciar Backend

```powershell
# Crie pasta de ambiente virtual (opcional mas recomendado)
python -m venv venv

# Ative o ambiente
.\venv\Scripts\Activate.ps1

# Instale dependências
pip install -r requirements.txt

# Inicie o servidor
python backend/server.py
```

**Resultado esperado:**
```
╔════════════════════════════════════════╗
║         FitTrack API Server            ║
║       Iniciando em modo development    ║
╚════════════════════════════════════════╝

🚀 Servidor rodando em http://127.0.0.1:5000
```

---

## 2️⃣ Terminal 2 (Opcional) - Testar API

```powershell
# Em outro terminal, enquanto o servidor está rodando
python testar_api.py
```

---

## 3️⃣ Browser - Abrir Frontend

**Opção A: Com Live Server (VS Code)**
1. Instale a extensão "Live Server" 
2. Clique direito em `login.html`
3. "Open with Live Server"

**Opção B: URL Direta**
- Abra `http://127.0.0.1:5500/login.html`

---

## 🧪 Dados de Teste

### Criar Conta
- **Nome:** João Silva
- **Email:** joao@example.com  
- **Senha:** JoaoSenha123!@#

### Dados de Perfil
- **Idade:** 25 anos
- **Peso:** 75 kg
- **Altura:** 180 cm

### Atividade de Teste
- **Tipo:** Corrida
- **Duração:** 30 minutos
- **Distância:** 5 km
- **Intensidade:** Moderada

---

## 🎯 Fluxo de Uso

1. **Cadastre-se** em login.html → "Crie sua conta"
2. **Faça login** com os dados que acabou de criar
3. **Atualize perfil** em "Meu Perfil"
4. **Registre atividade** em "Registrar Atividade"
5. **Veja histórico** em "Histórico"
6. **Edite ou delete** atividades no histórico

---

## 📊 Pontos-Chave

✅ **Backend funciona em:** `http://127.0.0.1:5000`
✅ **Frontend funciona em:** `http://127.0.0.1:5500`
✅ **Dados salvam em:** `fittrack.db`
✅ **API Docs:** `http://127.0.0.1:5000/`

---

## 🔧 Se algo der errado

### Erro: "Cannot connect to API"
```powershell
# Verifique se o servidor está rodando
# Se não estiver, execute em Terminal 1:
python backend/server.py
```

### Erro: "Module not found"
```powershell
pip install -r requirements.txt
```

### Limpar banco de dados
```powershell
# Feche o servidor
# Delete o arquivo: fittrack.db
# Reinicie o servidor (vai recriar o DB vazio)
```

---

## 📚 Mais Informações

- **Documentação Completa:** `README.md`
- **Guia Detalhado:** `GUIA_USO.md`
- **Implementação:** `IMPLEMENTACAO.md`
- **Testes:** `testar_api.py`

---

**Pronto! O app está funcionando 🚀**
