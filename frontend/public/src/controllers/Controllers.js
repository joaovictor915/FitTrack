/**
 * Auth Controller - Gerencia lógica de autenticação
 */
class AuthController {
    constructor(api) {
        this.api = api;
        this.usuarioAtual = null;
    }

    async inicializar() {
        try {
            this.usuarioAtual = await this.api.obterUsuarioAtual();
            this.atualizarUIAutenticado(true);
            return true;
        } catch (error) {
            this.atualizarUIAutenticado(false);
            return false;
        }
    }

    async registrar(nome, email, senha) {
        try {
            const resultado = await this.api.registrar(nome, email, senha);
            this.usuarioAtual = resultado.usuario;
            this.atualizarUIAutenticado(true);
            return resultado;
        } catch (error) {
            throw error;
        }
    }

    async login(email, senha) {
        try {
            console.log(`[AuthController] Iniciando login para: ${email}`);
            const resultado = await this.api.login(email, senha);
            console.log(`[AuthController] Login bem-sucedido, resultado:`, resultado);
            
            if (!resultado?.usuario) {
                throw new Error('Resposta inválida do servidor');
            }
            
            this.usuarioAtual = resultado.usuario;
            this.atualizarUIAutenticado(true);
            console.log(`[AuthController] UI atualizada, usuário:`, this.usuarioAtual);
            return resultado;
        } catch (error) {
            console.error(`[AuthController] Erro ao fazer login:`, error);
            throw error;
        }
    }

    async logout() {
        try {
            await this.api.logout();
            this.usuarioAtual = null;
            this.atualizarUIAutenticado(false);
            localStorage.removeItem('usuarioId');
        } catch (error) {
            throw error;
        }
    }

    async atualizarPerfil(dados) {
        try {
            const resultado = await this.api.atualizarPerfil(dados);
            this.usuarioAtual = resultado.usuario;
            return resultado;
        } catch (error) {
            throw error;
        }
    }

    estaAutenticado() {
        return this.usuarioAtual !== null;
    }

    atualizarUIAutenticado(autenticado) {
        if (autenticado) {
            document.body.classList.add('autenticado');
            document.body.classList.remove('nao-autenticado');
        } else {
            document.body.classList.remove('autenticado');
            document.body.classList.add('nao-autenticado');
        }
    }
}

/**
 * Atividades Controller - Gerencia lógica de atividades
 */
class AtividadesController {
    constructor(api) {
        this.api = api;
        this.atividades = [];
        this.paginaAtual = 1;
        this.porPagina = 10;
        this.estatisticas = null;
    }

    async listar(filtros = {}) {
        try {
            const resultado = await this.api.listarAtividades({
                pagina: this.paginaAtual,
                por_pagina: this.porPagina,
                ...filtros
            });
            this.atividades = resultado.atividades;
            return resultado;
        } catch (error) {
            throw error;
        }
    }

    async obter(id) {
        try {
            return await this.api.obterAtividade(id);
        } catch (error) {
            throw error;
        }
    }

    async criar(dados) {
        try {
            const resultado = await this.api.criarAtividade(dados);
            await this.listar();
            await this.atualizarEstatisticas();
            return resultado;
        } catch (error) {
            throw error;
        }
    }

    async atualizar(id, dados) {
        try {
            const resultado = await this.api.atualizarAtividade(id, dados);
            await this.listar();
            await this.atualizarEstatisticas();
            return resultado;
        } catch (error) {
            throw error;
        }
    }

    async deletar(id) {
        try {
            const resultado = await this.api.deletarAtividade(id);
            await this.listar();
            await this.atualizarEstatisticas();
            return resultado;
        } catch (error) {
            throw error;
        }
    }

    async atualizarEstatisticas() {
        try {
            this.estatisticas = await this.api.obterEstatisticas();
            return this.estatisticas;
        } catch (error) {
            console.error('Erro ao buscar estatísticas:', error);
            return null;
        }
    }

    async proxima() {
        this.paginaAtual += 1;
        return this.listar();
    }

    async anterior() {
        if (this.paginaAtual > 1) {
            this.paginaAtual -= 1;
            return this.listar();
        }
        return null;
    }
}

// Instâncias globais dos controllers - criadas ao carregar o script
// Nota: As páginas protected devem chamar authController.inicializar() 
// As páginas públicas (login, cadastro) não precisam inicializar
const authController = new AuthController(api);
const atividadesController = new AtividadesController(api);

