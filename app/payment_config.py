"""
Configurações para integração com o Mercado Pago
"""

# Credenciais do Mercado Pago (substitua por suas credenciais reais quando for para produção)
MERCADO_PAGO_PUBLIC_KEY = "TEST-8acebd18-a6ad-402b-a3a3-8de7897ea41a"  # Este é um exemplo de chave de teste
MERCADO_PAGO_ACCESS_TOKEN = "TEST-5920810751127991-042911-4a84c6d818fcf2fd6b05a2a9b46c132c-1556006293"  # Este é um exemplo de token de teste

# Configurações gerais
MERCADO_PAGO_BACK_URL = {
    "success": "/payment/success",
    "failure": "/payment/failure",
    "pending": "/payment/pending"
}

# Mensagens
PAYMENT_MESSAGES = {
    "success": "Pagamento processado com sucesso!",
    "pending": "Pagamento em processamento.",
    "failure": "Houve um problema com o pagamento."
}
