/**
 * API Client - Gerencia todas as chamadas à API
 */
class APIClient {
    constructor(baseURL = 'http://127.0.0.1:5000/api') {
        this.baseURL = baseURL;
        this.token = localStorage.getItem('token');
    }

    /**
     * Faz uma requisição HTTP genérica
     */
    async requisicao(endpoint, opcoes = {}) {
        const url = `${this.baseURL}${endpoint}`;
        
        const config = {
            headers: {
                'Content-Type': 'application/json',
                ...opcoes.headers
            },
            credentials: 'include',
            ...opcoes
        };

        try {
            console.log(`[APIClient] ${config.method || 'GET'} ${url}`);
            console.log(`[APIClient] Config:`, config);
            
            const resposta = await fetch(url, config);
            
            console.log(`[APIClient] Status: ${resposta.status}`);
            console.log(`[APIClient] Headers resposta:`, Array.from(resposta.headers.entries()));
            
            let dados;
            const contentType = resposta.headers.get('content-type');
            
            if (contentType?.includes('application/json')) {
                dados = await resposta.json();
            } else {
                dados = await resposta.text();
            }
            
            console.log(`[APIClient] Dados:`, dados);
            
            if (!resposta.ok) {
                const mensagem = typeof dados === 'object' ? dados.mensagem : dados;
                console.error(`[APIClient] Erro na resposta:`, mensagem);
                throw new Error(mensagem || `Erro ${resposta.status}`);
            }

            return dados;
        } catch (error) {
            console.error(`[APIClient] Exceção em ${endpoint}:`, error);
            console.error(`[APIClient] Tipo de erro:`, error.constructor.name);
            console.error(`[APIClient] Stack:`, error.stack);
            
            // Mensagem mais clara para o usuário
            if (error.message === 'Failed to fetch' || error.name === 'TypeError') {
                const mensagemErro = 'Não foi possível conectar ao servidor. Verifique se o backend está rodando em http://127.0.0.1:5000';
                console.error(`[APIClient] ${mensagemErro}`);
                throw new Error(mensagemErro);
            }
            
            throw error;
        }
    }

    // ==================== AUTENTICAÇÃO ====================

    async registrar(nome, email, senha) {
        return this.requisicao('/auth/registrar', {
            method: 'POST',
            body: JSON.stringify({ nome, email, senha })
        });
    }

    async login(email, senha) {
        return this.requisicao('/auth/login', {
            method: 'POST',
            body: JSON.stringify({ email, senha })
        });
    }

    async logout() {
        return this.requisicao('/auth/logout', {
            method: 'POST'
        });
    }

    async obterUsuarioAtual() {
        return this.requisicao('/auth/usuario-atual');
    }

    async atualizarPerfil(dados) {
        return this.requisicao('/auth/atualizar-perfil', {
            method: 'PUT',
            body: JSON.stringify(dados)
        });
    }

    // ==================== ATIVIDADES ====================

    async listarAtividades(filtros = {}) {
        let endpoint = '/atividades?';
        if (filtros.tipo) endpoint += `tipo=${filtros.tipo}&`;
        if (filtros.pagina) endpoint += `pagina=${filtros.pagina}&`;
        if (filtros.por_pagina) endpoint += `por_pagina=${filtros.por_pagina}`;
        
        return this.requisicao(endpoint);
    }

    async obterAtividade(id) {
        return this.requisicao(`/atividades/${id}`);
    }

    async criarAtividade(dados) {
        return this.requisicao('/atividades', {
            method: 'POST',
            body: JSON.stringify(dados)
        });
    }

    async atualizarAtividade(id, dados) {
        return this.requisicao(`/atividades/${id}`, {
            method: 'PUT',
            body: JSON.stringify(dados)
        });
    }

    async deletarAtividade(id) {
        return this.requisicao(`/atividades/${id}`, {
            method: 'DELETE'
        });
    }

    async obterEstatisticas() {
        return this.requisicao('/atividades/resumo/stats');
    }
}

// Instância global
const api = new APIClient();
