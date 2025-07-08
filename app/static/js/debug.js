/**
 * Utilidades de depuração para Mercado Pago
 * Este arquivo contém funções para ajudar a diagnosticar problemas
 * com a integração do Mercado Pago
 */

console.log('Debug utilities loaded');

// Função para testar a conectividade com o Mercado Pago
function testMercadoPagoConnectivity() {
    console.log("Testando conectividade com Mercado Pago...");
    
    const startTime = performance.now();
    
    // Tenta carregar recursos do Mercado Pago para verificar conectividade
    fetch('https://sdk.mercadopago.com/js/v2', { 
        method: 'HEAD',
        mode: 'no-cors',
        cache: 'no-cache'
    })
    .then(() => {
        const endTime = performance.now();
        const duration = Math.round(endTime - startTime);
        console.log(`✅ Conectividade com Mercado Pago OK (${duration}ms)`);
        return true;
    })
    .catch(error => {
        console.error(`❌ Erro de conectividade com Mercado Pago: ${error.message}`);
        return false;
    });
}

// Função para diagnosticar problemas comuns
function diagnosePaymentIssues(publicKey) {
    const issues = [];
    
    // Verificar chave pública
    if (!publicKey || publicKey.length < 10) {
        issues.push("Chave pública do Mercado Pago ausente ou inválida");
    }
    
    // Verificar se estamos em HTTPS (produção) ou HTTP (local)
    const isHTTPS = window.location.protocol === 'https:';
    if (!isHTTPS && window.location.hostname !== 'localhost' && window.location.hostname !== '127.0.0.1') {
        issues.push("Conexão não segura (HTTP). O Mercado Pago requer HTTPS em ambiente de produção.");
    }
    
    // Verificar navegador
    const userAgent = navigator.userAgent.toLowerCase();
    if (userAgent.indexOf('msie') !== -1 || userAgent.indexOf('trident') !== -1) {
        issues.push("Navegador Internet Explorer detectado. O Mercado Pago pode não funcionar corretamente.");
    }
    
    // Verificar cookies
    if (!navigator.cookieEnabled) {
        issues.push("Cookies desativados. O Mercado Pago requer cookies para funcionar.");
    }
    
    // Exibir resultados
    console.log("=== Diagnóstico de Pagamento ===");
    
    if (issues.length === 0) {
        console.log("✅ Nenhum problema encontrado");
    } else {
        console.log("❌ Problemas encontrados:");
        issues.forEach(issue => {
            console.log(`  - ${issue}`);
        });
    }
    
    // Informações do ambiente
    console.log("=== Informações do Ambiente ===");
    console.log(`Navegador: ${navigator.userAgent}`);
    console.log(`Protocolo: ${window.location.protocol}`);
    console.log(`Host: ${window.location.host}`);
    console.log(`Cookies Habilitados: ${navigator.cookieEnabled}`);
    
    return issues;
}

// Função para registrar eventos do Mercado Pago
function setupMercadoPagoLogging() {
    // Verificar se o SDK do Mercado Pago está carregado
    if (typeof MercadoPago === 'undefined') {
        console.error("SDK do Mercado Pago não está carregado");
        return;
    }
    
    console.log("Configurando logging para eventos do Mercado Pago");
    
    // Registrar tempo de inicialização
    window.mpInitStartTime = performance.now();
    
    // Interceptar eventos comuns do checkout
    document.addEventListener('submit', function(event) {
        if (event.target.closest('.cho-container, #wallet_container')) {
            console.log("Formulário de pagamento enviado:", event);
        }
    });
    
    // Registrar navegação de página
    window.addEventListener('beforeunload', function() {
        console.log("Saindo da página de pagamento");
    });
    
    // Monitorar carregamento de recursos
    const originalFetch = window.fetch;
    window.fetch = function() {
        const url = arguments[0];
        if (typeof url === 'string' && url.includes('mercadopago')) {
            console.log(`Fetch para Mercado Pago: ${url}`);
            const startTime = performance.now();
            
            return originalFetch.apply(this, arguments)
                .then(response => {
                    const duration = Math.round(performance.now() - startTime);
                    console.log(`Resposta de ${url} recebida em ${duration}ms`);
                    return response;
                })
                .catch(error => {
                    console.error(`Erro em fetch para ${url}:`, error);
                    throw error;
                });
        }
        return originalFetch.apply(this, arguments);
    };
}

// Exportar funções
window.MercadoPagoDebug = {
    testConnectivity: testMercadoPagoConnectivity,
    diagnose: diagnosePaymentIssues,
    setupLogging: setupMercadoPagoLogging
};
