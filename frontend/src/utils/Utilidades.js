/**
 * Utilitários e funções auxiliares
 */
class Utilidades {
    /**
     * Formata data para exibição
     */
    static formatarData(dataStr) {
        if (!dataStr) return '';
        const data = new Date(dataStr);
        return data.toLocaleDateString('pt-BR', {
            year: 'numeric',
            month: '2-digit',
            day: '2-digit',
            hour: '2-digit',
            minute: '2-digit'
        });
    }

    /**
     * Formata apenas a data sem hora
     */
    static formatarDataCurta(dataStr) {
        if (!dataStr) return '';
        const data = new Date(dataStr);
        return data.toLocaleDateString('pt-BR');
    }

    /**
     * Formata número com 2 casas decimais
     */
    static formatarNumero(valor, casas = 2) {
        if (valor === null || valor === undefined) return '0';
        return parseFloat(valor).toFixed(casas);
    }

    /**
     * Formata tipo de atividade para exibição
     */
    static formatarTipoAtividade(tipo) {
        const mapa = {
            'corrida': '🏃 Corrida',
            'caminhada': '🚶 Caminhada',
            'ciclismo': '🚴 Ciclismo',
            'musculacao': '💪 Musculação',
            'natacao': '🏊 Natação',
            'artesmarciais': '🥋 Artes Marciais',
            'yoga': '🧘 Yoga'
        };
        return mapa[tipo] || tipo;
    }

    /**
     * Formata intensidade para exibição
     */
    static formatarIntensidade(intensidade) {
        const mapa = {
            'baixa': '🟢 Baixa',
            'moderada': '🟡 Moderada',
            'alta': '🔴 Alta'
        };
        return mapa[intensidade] || intensidade;
    }

    /**
     * Exibe mensagem de sucesso
     */
    static mostrarSucesso(mensagem) {
        alert(`✅ ${mensagem}`);
    }

    /**
     * Exibe mensagem de erro
     */
    static mostrarErro(mensagem) {
        console.error(`[Utilidades] Erro: ${mensagem}`);
        alert(`❌ Erro: ${mensagem}`);
    }

    /**
     * Exibe mensagem de confirmação
     */
    static confirmar(mensagem) {
        return confirm(`⚠️ ${mensagem}`);
    }

    /**
     * Valida email
     */
    static validarEmail(email) {
        const regex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
        return regex.test(email);
    }

    /**
     * Valida força de senha
     */
    static validarSenha(senha) {
        if (senha.length < 8) return { valido: false, msg: 'Mín. 8 caracteres' };
        if (!/[A-Z]/.test(senha)) return { valido: false, msg: 'Precisa de maiúsculas' };
        if (!/[a-z]/.test(senha)) return { valido: false, msg: 'Precisa de minúsculas' };
        if (!/\d/.test(senha)) return { valido: false, msg: 'Precisa de números' };
        if (!/[!@#$%^&*()_+\-=[\]{}|;:,.<>?]/.test(senha)) {
            return { valido: false, msg: 'Precisa de caracteres especiais' };
        }
        return { valido: true, msg: 'Senha forte' };
    }

    /**
     * Calcula IMC
     */
    static calcularIMC(peso, altura) {
        if (!peso || !altura) return null;
        const alturaM = altura / 100;
        return (peso / (alturaM * alturaM)).toFixed(1);
    }

    /**
     * Classifica IMC
     */
    static classificarIMC(imc) {
        if (imc < 18.5) return 'Abaixo do peso';
        if (imc < 25) return 'Peso normal';
        if (imc < 30) return 'Sobrepeso';
        if (imc < 35) return 'Obesidade grau I';
        if (imc < 40) return 'Obesidade grau II';
        return 'Obesidade grau III';
    }
}

// Instância global
const util = Utilidades;
